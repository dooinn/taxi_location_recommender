use chicago_taxi;


#create a table - only aemrican united trips history
create table american_united_trips as
select * from trips
where company_id = 4;



with AnnualEarnings as (
	select taxi_id, sum(trip_total) as annual_total_earnings
	from american_united_trips
	group by taxi_id
) select round(avg(annual_total_earnings),2) as avg_annual_earnings from AnnualEarnings;




# Daily Average Turnaround per taxi?
with RankedTrips as (
    select taxi_id,trip_start_timestamp,trip_end_timestamp,
        lead(trip_start_timestamp) over (partition by taxi_id order by trip_start_timestamp) as next_pickup_time,
        date(trip_start_timestamp) as pickup_date
    from american_united_trips
),
TurnaroundTimes AS (
    select taxi_id,pickup_date,
        timestampdiff(minute, trip_end_timestamp, next_pickup_time) as turnaround_time
    from RankedTrips
    where next_pickup_time is not null
),
TaxiAVGTR as (
select taxi_id,pickup_date,
    avg(turnaround_time) as average_turnaround_time
from TurnaroundTimes
group by taxi_id, pickup_date
order by taxi_id, pickup_date
)
select taxi_id, round(avg(average_turnaround_time),2) as daily_avg_turnaround from TaxiAVGTR
group by taxi_id;


# Top 10 pickup location?
select location.address, count(*) as total from american_united_trips
left join location
on american_united_trips.pickup_location = location.location_coordinates
group by address
order by total desc
limit 10;


# Payment method - Credit Card vs Cash
select 
	payment_type, 
    round(avg(trip_total),2) as avg_fare, 
	round(avg(trip_miles),2), count(*) as count 
from american_united_trips
group by payment_type;


# Daily earnings per taxi?

with EaringDate as (
SELECT taxi_id, trip_total, date(trip_start_timestamp) AS pickup_date 
FROM american_united_trips
),
DailyTotal as (
select taxi_id,pickup_date, sum(trip_total) as daily_total from EaringDate
group by taxi_id, pickup_date
)
select taxi_id, avg(daily_total)
from DailyTotal 
group by taxi_id;


# Highest depand hours?
select 
	hour(trip_start_timestamp) as trip_start_hour, 
    count(*) as total 
from trips
group by trip_start_hour
order by total desc;


# which hours highest demand by location?
with HourlyDemand as (
  select pickup_location, extract(hour from trip_start_timestamp) as trip_hour, 
    count(*) as total
  from american_united_trips
  group by pickup_location, extract(hour from trip_start_timestamp)
),
RankedDemand AS (
  select pickup_location, trip_hour, total,
    rank() over (partition by pickup_location order by total desc) as rank_demand
  from HourlyDemand
),
HighDemand as (
select pickup_location, trip_hour as highest_demand_hour, total
from RankedDemand
where rank_demand = 1
) select address, highest_demand_hour, total from HighDemand
left join location
on HighDemand.pickup_location = location.location_coordinates;



select * from american_united_trips;

