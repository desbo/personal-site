create table if not exists posts (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  posted_on date
);