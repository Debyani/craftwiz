delete from url_popularity;
Insert or ignore into url_popularity select to_id, occurances from (select   to_id  , count(*)  as occurances
from url_association
where from_id <>to_id  group by to_id) A
;
