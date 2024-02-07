use chicago_taxi;


#create a table - only aemrican united trips history
create table american_united_trips as
select * from trips
where company_id = 4;

with t1 as (
select taxi_id, count(*) as total_count, sum(trip_total) as annual_total_earnings
from american_united_trips
group by taxi_id
) select round(avg(annual_total_earnings),2) as avg_annual_earnings from t1;

