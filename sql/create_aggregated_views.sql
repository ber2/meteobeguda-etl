create unique index meteobeguda on meteobeguda_events
("date", "timestamp");

drop view if exists meteobeguda_daily;

create view meteobeguda_daily as
select
  "date",
  avg(temperature) as temperature_avg,
  min(temperature) as temperature_min,
  max(temperature) as temperature_max,
  avg(humidity) as humidity_avg,
  avg(windspeed) as windspeed_avg,
  max(windspeed_max) as windspeed_max,
  avg(pressure) as pressure_avg,
  sum(rain) as rain_total
from meteobeguda_events
group by 1;

drop view if exists meteobeguda_monthly;

create view meteobeguda_monthly as
select
  strftime('%Y-%m-01', "date") as "month",
  avg(temperature_avg) as temperature_avg,
  min(temperature_min) as temperature_min,
  max(temperature_max) as temperature_max,
  avg(humidity_avg) as humidity_avg,
  avg(windspeed_avg) as windspeed_avg,
  max(windspeed_max) as windspeed_max,
  sum(rain_total) as rain_total
from meteobeguda_daily
group by 1;

drop view if exists meteobeguda_yearly;

create view meteobeguda_yearly as
select
  strftime('%Y', "month") as "year",
  avg(temperature_avg) as temperature_avg,
  min(temperature_min) as temperature_min,
  max(temperature_max) as temperature_max,
  avg(humidity_avg) as humidity_avg,
  avg(windspeed_avg) as windspeed_avg,
  max(windspeed_max) as windspeed_max,
  sum(rain_total) as rain_total
from meteobeguda_monthly
group by 1;

