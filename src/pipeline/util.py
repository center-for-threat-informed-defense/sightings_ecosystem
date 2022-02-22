import json
import logging
import os


def get_data_files(base_dir=None):
    files = []
    files = [
        os.path.join(root, name) for root, dirs, files in os.walk(base_dir) for name in files if name.endswith(".json")
    ]
    return files


def load_data(file):
    data = None
    try:
        with open(file) as f:
            data = json.load(f)
    except Exception as e:
        logging.error("{}: {}".format(__file__, str(e)))
    finally:
        return data


def load_data_str(str):
    data = None
    try:
        data = json.loads(str)
    except Exception as e:
        logging.error("{}: {}".format(__file__, str(e)))
    finally:
        return data


def save_data(file, data):
    try:
        with open(file, "w") as f:
            f.write(obj_to_json(data))
    except Exception as e:
        logging.error("{}: {}".format(__file__, str(e)))


def obj_to_json(obj):
    jstr = None
    try:
        jstr = json.dumps(obj)
    except Exception as e:  # pragma: no cover
        logging.error("{}: {}".format(__file__, str(e)))
    finally:
        return jstr


def print_overtop(str, end=""):  # pragma: no cover
    """
    print overtop the current line
    useful for showing progress without spamming console
    """
    print("", end="\x1b[1K\r", flush=True)
    print(str, end=end, flush=True)
