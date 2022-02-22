create
or replace procedure sighting_export() language plpgsql as $$ begin --
drop view if exists generalized_sightings CASCADE;

create VIEW generalized_sightings as
select
    sighting_pid,
    technique_pid,
    technique_id,
    sighting_type,
    detection_type,
    date_trunc('month', public.flattened_sightings.start_time) as date
from
    public.flattened_sightings;

end;

$$
