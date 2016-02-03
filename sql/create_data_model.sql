--we will create these tables :
--1. A url table that has an id and a  complete URL
--2. A count table that has a count of how many times have we seen the URL while parsing. so if a URL was referenced by two different URLS
--  the count will be 2.  id from table #1, id from table #2 and count of occurance
--3. A table of base URLS aka - websites , id , website
--4. A table showing url association. from_id (#1), to_id (#1)

-- donot drop the table. this is the resume feature
--added a resume restart functionality for loading
--TODO : how do we take care of removed/dead links?

create table if not exists url(
    id integer primary key autoincrement,
    complete_url text,
    processed integer(1) default 0,
    depth integer,
    unique (complete_url)
    );
create table if not exists url_base(
  id integer primary key autoincrement,
  base_url text,
  unique (base_url));


 create table if not exists url_association(
 id integer primary key autoincrement,
 from_id integer,
 to_id integer,
 active integer(1) default 1,
 foreign key (from_id) references url(id),
 foreign key (to_id) references url(id),
 unique (from_id, to_id));

drop table if exists url_popularity;

create table if not exists  url_popularity(
 url_id integer ,
 occurrence integer ,
 foreign key (url_id) references url(id));

