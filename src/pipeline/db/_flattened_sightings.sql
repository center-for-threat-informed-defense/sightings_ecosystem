create
or replace procedure flattened_sightings() language plpgsql as $$ begin --
drop view if exists flattened_sightings CASCADE;

create VIEW flattened_sightings as
select
    sighting_pid,
    technique_pid,
    technique_id,
    sighting_type,
    detection_type,
    public.sighting.start_time
from
    public.sighting
    join public.technique on public.sighting.sighting_pid = public.technique.sighting_id
where
    (
        TO_DATE('2019-04-01', 'YYYY-MM-DD') < public.sighting.start_time
    )
    and (public.sighting.start_time < now());

end;

$$
