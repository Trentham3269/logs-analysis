#!/usr/bin/python3

import psycopg2

# Connection string
dbname = "news"


# Three most popular articles of all time
def get_articles():
    sql = "select title, views from views fetch first 3 rows only;"
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute(sql)
    articles = c.fetchall()
    db.close()
    print("The three most popular articles...")
    for a in articles:
        print('Title: {0}, Article views: {1}'.format(a[0], a[1]))

get_articles()

# Most popular authors of all time
def get_authors():
    sql = "select name, sum(views) as total from views group by name order by total desc;"
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute(sql)
    authors = c.fetchall()
    db.close()
    print("The most popular authors...")
    for a in authors:
        print('Author: {0}, Total views: {1}'.format(a[0], a[1]))

get_authors()

# Days in which more than 1% of requests were errors
def get_errors():
    sql = "select date(day), round(error_rate,2) from error_rates where error_rate > 1"
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute(sql)
    errors = c.fetchall()
    db.close()
    print("Big error days...")
    for e in errors:
        print('Date: {0}, Error rate: {1}%'.format(e[0], e[1]))

get_errors()
