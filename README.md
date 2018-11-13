# Logs Analysis

Answers the following questions about the traffic of a fictional newspaper website:
+ What are the most popular three articles of all time?
+ Who are the most popular article authors of all time?
+ On which days did more than 1% of requests lead to errors?

![Example Output](./logs.txt)

## Dependencies
This code requires the following software to run:
+ [Python 3](https://www.python.org/downloads/)
+ [psycopg2](https://pypi.org/project/psycopg2/)
+ [VirtualBox](https://www.virtualbox.org/)
+ [Vagrant](https://www.vagrantup.com/)
+ [PostgreSQL](https://www.postgresql.org/)

## Database info

### Setup
To setup the database:
```
$ cd /vagrant
$ wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
$ unzip newsdata.zip
$ psql -d news -f newsdata.sql
```

### Structure
The database includes three tables:

+ The authors table includes information about the authors of articles `\d authors`
+ The articles table includes the articles themselves `\d articles`
+ The log table includes one entry for each time a user has accessed the site `\log`

### Views
In order for the Python code to run, create the following views in the news database.

For question 1 and 2:
```
create view views as
select authors.name, articles.title, articles.slug, count(articles.slug) as views 
from articles, log, authors
where '/article/' || articles.slug = log.path 
and articles.author = authors.id 
group by authors.name, articles.title, articles.slug, log.path 
order by views desc;
```

For question 3:
```
create view daily_errors as
select date_trunc('day', time) as day, count(*)
from log
where status = '404 NOT FOUND'
group by day
order by day desc;

create view daily_traffic as
select date_trunc('day', time) as day, count(*)
from log
group by day
order by day desc;

create view error_rates as 
select daily_errors.day, daily_errors.count as errors, daily_traffic.count as traffic, (daily_errors.count/daily_traffic.count::decimal)*100 as error_rate 
from daily_errors, daily_traffic 
where daily_errors.day = daily_traffic.day
order by daily_errors.day desc;
```

## Style Guide
The [Pep8](https://www.python.org/dev/peps/pep-0008/) style guide was used. To check the code's adherence to this standard you can run [pycodestyle](https://pypi.org/project/pycodestyle/) on Linux with `$ pycodestyle logs.py`






