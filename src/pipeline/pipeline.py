import argparse
import logging
import os
import sys
from timeit import default_timer as timer

import anticrlf
import util
from db.model import ModelHelper, SightingTable, TechniqueTable
from objects.sighting import SightingSchema
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_batch_inserts import enable_batch_inserting

CONTAINER_ENV_MARKER = "IN_CONTAINER"
LOG_FILE = "pipeline.log"

log_formatter = anticrlf.LogFormatter("%(asctime)s - %(levelname)-8s - %(filename)s:%(funcName)s - %(message)s")

logging.basicConfig(datefmt="%d-%b-%y %H:%M:%S")

logger = logging.getLogger(__name__)

# if running in container, log to stdout and use docker logging facilities
if CONTAINER_ENV_MARKER in os.environ:
    consoleHandler = logging.StreamHandler(sys.stdout)  # set streamhandler to stdout
    consoleHandler.setFormatter(log_formatter)
    logger.addHandler(consoleHandler)
else:
    fileHandler = logging.FileHandler(LOG_FILE, encoding="utf8")
    fileHandler.setFormatter(log_formatter)
    logger.addHandler(fileHandler)

# set log level regardless of handler
logger.setLevel(logging.ERROR)

base = declarative_base()

sighting_count = 0
technique_count = 0

total_sightings_found = 0
db_ingest_count = 0
db_ingest_batch_size = os.getenv("db_ingest_batch_size", 1000)
db_ingest_elapsed_time = 0


def get_argparse():  # pragma: no covers
    desc = "Sightings Pipeline"
    argparser = argparse.ArgumentParser(description=desc)
    argparser.add_argument("-i", type=str, help="Path to processed sighting data.")
    return argparser


def db_session():  # pragma: no cover
    try:
        db_hostname = os.environ["sighting_db_hostname_str"]
        if db_hostname is None:
            db_hostname = "127.0.0.1"
        db_protocol = "postgresql+psycopg2://sightings:sightings"
        db_address = f"{db_hostname}:5432/sightings"
        db_url = f"{db_protocol}@{db_address}"
        db = create_engine(
            db_url,
            executemany_mode="values",
            executemany_values_page_size=db_ingest_batch_size,
            executemany_batch_page_size=500,
        )
        SightingTable.__table__.create(bind=db, checkfirst=True)
        TechniqueTable.__table__.create(bind=db, checkfirst=True)
        base.metadata.create_all(db)
        _session = sessionmaker(bind=db)
        session = _session()
        enable_batch_inserting(session)
        return session, db
    except exc.DatabaseError as err:
        logger.error("{}: {}".format(__file__, err))
        exit(-1)


def db_add_sighting(session, obj_model, cid=None):  # pragma: no cover
    try:
        global technique_count
        global sighting_count
        sighting_table = ModelHelper.convert_model_to_sighting_table(obj_model)
        if cid:
            sighting_table.cid = cid
        session.add(sighting_table)
        sighting_count += 1
        sighting_pid = sighting_count
        for technique_obj in obj_model.techniques:
            session.add(ModelHelper.convert_model_to_technique_table(technique_obj, sighting_pid))
            technique_count += 1
    except exc.IntegrityError as err:
        session.rollback()
        logger.error("{}:{}".format(__file__, err))


def process_sighting(session, sighting_data_dir):  # pragma: no covers
    global db_ingest_elapsed_time
    print("Inserting Sightings into database...")

    # TODO: Release version
    # files = util.get_data_files(base_dir=sighting_data_dir)

    # Temp. iteration with CID for Mary / Analytics
    for subdir, dirs, files in os.walk(sighting_data_dir):
        dirname = subdir.split(os.path.sep)[-1]
        if len(dirname) == 0:
            continue
        for file in files:
            if file.endswith(".json"):
                fq_file = os.path.join(subdir, file)
                with open(fq_file) as f:
                    logger.debug("{}".format(fq_file))
                    data = "".join(line.rstrip() for line in f)
                    if data:
                        obj = util.load_data_str(data)
                        if obj:
                            # Array of Sighting models
                            last_sighting_from_file = False
                            if isinstance(obj, list):
                                for idx, elem in enumerate(obj):
                                    schema = SightingSchema()
                                    obj_model = schema.load(elem)
                                    db_batched_insert_sightings(session, obj_model, cid=dirname)
                                    # maintain state through enumeration, and flag when we are ready to commit at end of file
                                    if idx == (len(obj) - 1):
                                        last_sighting_from_file = True
                                    db_batched_commit_sightings(session, last_sighting_from_file)
                                    update_completion_estimate()
                            else:
                                # Single Sighting model
                                schema = SightingSchema()
                                obj_model = schema.load(obj)
                                # if we retrieve 1 sighting from a file, its always the last
                                last_sighting_from_file = True
                                db_batched_insert_sightings(session, obj_model, cid=dirname)
                                db_batched_commit_sightings(session, last_sighting_from_file)
                                update_completion_estimate()
                        else:
                            logger.error("{}: {} - {}".format(__file__, file, "error {}".format(file)))
                    else:
                        logger.warning("{}: {}".format(__file__, "skip {}".format(file)))


def db_batched_insert_sightings(session, obj_model, cid):  # pragma: no covers
    global db_ingest_elapsed_time
    global start_time

    if sighting_count % db_ingest_batch_size == 0:
        start_time = timer()

    db_add_sighting(session, obj_model, cid)

    if sighting_count % db_ingest_batch_size == 0:
        end_time = timer()
        db_ingest_elapsed_time += end_time - start_time


def db_batched_commit_sightings(session, last_sightings_from_file):  # pragma: no covers
    try:
        global db_ingest_batch_size
        global db_ingest_elapsed_time

        if sighting_count % db_ingest_batch_size == 0 or last_sightings_from_file:
            start_time = timer()
            session.commit()
            end_time = timer()
            db_ingest_elapsed_time += end_time - start_time
    except exc.IntegrityError as err:
        session.rollback()
        logger.error("{}:{}".format(__file__, err))


def db_execute_procedure(db, name):  # pragma: no covers
    try:
        with db.begin() as conn:
            conn.execute("CALL {}();".format(name))
    except exc.SQLAlchemyError as err:
        logger.error("{}:{}".format(__file__, err))


def update_completion_estimate():  # pragma: no covers
    global db_ingest_count
    global db_ingest_batch_size
    global db_ingest_elapsed_time
    if sighting_count % db_ingest_batch_size == 0:

        db_ingest_count += 1

        db_ingest_average_time = db_ingest_elapsed_time / db_ingest_count

        remaining_sightings = total_sightings_found - sighting_count
        remaining_batches = remaining_sightings / db_ingest_batch_size
        estimated_minutes = (remaining_batches * db_ingest_average_time) / 60

        util.print_overtop(
            "Estimate {} min. to insert {:,} remaining Sightings".format(
                round(estimated_minutes, 2), remaining_sightings
            )
        )


def count_sightings(sighting_data_dir):  # pragma: no covers
    global total_sightings_found

    print("Counting Sightings...")
    sightings_counted = "{:,} Sightings counted"

    for subdir, dirs, files in os.walk(sighting_data_dir):
        dirname = subdir.split(os.path.sep)[-1]
        if len(dirname) == 0:
            continue
        for file in files:
            if not file.endswith(".json"):
                continue
            sightings_file_path = os.path.join(subdir, file)
            with open(sightings_file_path) as sightings_file:
                logger.debug("{}".format(sightings_file_path))
                sightings_json = "".join(line.rstrip() for line in sightings_file)
                if sightings_json:
                    sightings_object = util.load_data_str(sightings_json)
                    if sightings_object:
                        if isinstance(sightings_object, list):
                            # Array of Sighting models
                            total_sightings_found += len(sightings_object)
                            util.print_overtop(sightings_counted.format(total_sightings_found))
                        else:
                            # Single Sighting model
                            total_sightings_found += 1
                            util.print_overtop(sightings_counted.format(total_sightings_found))
                    else:
                        logger.error("{}: {} - {}".format(__file__, file, "error {}".format(file)))
                else:
                    logger.warning("{}: {}".format(__file__, "skip {}".format(file)))

    util.print_overtop(sightings_counted.format(total_sightings_found), end="\n")


def main(argv):  # pragma: no cover
    parser = get_argparse()
    args = parser.parse_args()
    if args.i is None:
        print("pipeline.py -i <processed_data_dir>")
        sys.exit(0)
    processed_data_dir = args.i

    session, db = db_session()
    if session:
        start_process = timer()
        count_sightings(processed_data_dir)
        process_sighting(session, processed_data_dir)
        db_execute_procedure(db, "flattened_sightings")
        end_process = timer()
        util.print_overtop("Process complete in {} hours".format(round((end_process - start_process) / 60 / 60, 2)))
        session.close()


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
