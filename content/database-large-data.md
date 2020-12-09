Title: Using a database | large data
Date: 2019-11-05
Category: programming
Tags: python, data

> This is part of a series of articles on [how to work with large
data]({filename}/analyzing-large-datasets.md)

The first method I want to explore when working with large data, since we
cannot use RAM, is to use a database for our dataset. Databases are a staple of
data processing and analysis, and are extremely memory and cpu efficient.

Where do we begin?

Most popular traditional databases support inserting rows from a csv file. In
order to insert our data into the database, we must first create a database and
table. I'm going to use [PostgreSQL](https://www.postgresql.org/) for this
task, though other options such as [MySQL](https://www.mysql.com) and
[SQLite](https://www.sqlite.org/index.html) would work as well.

Let's take one more peek at our data to figure out what columns we need for the
table.
```
$ head -5 Checkouts_by_Title.csv | column -s, -t
UsageClass  CheckoutType  MaterialType  CheckoutYear  CheckoutMonth  Checkouts  Title                                                                                                                                   Creator       Subjects                                   Publisher                           PublicationYear
Physical    Horizon       BOOK          2016          3              1          "The Aleutian islands: their people and natural history (with keys for the identification of the birds and plants) by Henry B. Collins   jr.           Austin H. Clark [and] Egbert H. Walker."  "Collins                             Henry B. (Henry Bascom)   1899-1987"                       "Aleuts                             Natural history Alaska Aleutian Islands   Aleutian Islands Alaska"  "Smithsonian institution  "  1945.
Physical    Horizon       SOUNDDISC     2016          3              9          Reality [sound recording] / David Bowie.                                                                                                "Bowie         David"                                    Rock music 2001 2010                "ISO/Columbia             "                                 p2003.
Physical    Horizon       BOOK          2016          3              1          Thresholds / Nina Kiriki Hoffman.                                                                                                       "Hoffman       Nina Kiriki"                              "Moving Household Juvenile fiction   Friendship Fiction        Extraterrestrial beings Fiction   Science fiction Juvenile fiction   Fantasy Fiction                           Oregon Juvenile fiction"  "Viking                   "  2010.
Digital     Freegal       SONG          2016          3              1          On Green Dolphin Street                                                                                                                 Nancy Wilson
```

Let's create a database
```console
$ createdb checkouts
```

and then a table.

```sql
CREATE TABLE checkouts
(
    usage_class TEXT,
    checkout_type TEXT,
    material_type TEXT,
    checkout_year INTEGER,
    checkout_month INTEGER,
    checkouts INTEGER,
    title TEXT,
    creator TEXT,
    subjects TEXT,
    publisher TEXT,
    publication_year TEXT,
)
CREATE INDEX year_idx ON checkouts (checkout_year)
```

I intentionally created an index for the `checkout_year` column because one of
the questions we want to know the answer to is "how many items were checked out
last year?" Creating an index on a column that you know will be filtered on
will make your query drastically more performant.

Now we can use the `\copy` command to insert our csv file into the newly
created table. This will take some time, depending on your computer. On mine,
it took slightly over five minutes to complete.
```console
$ time psql checkouts -c "\copy checkouts FROM './Checkouts_by_Title.csv' DELIMITER ',' CSV HEADER"
COPY 34677950

real    5m13.032s
user    0m14.329s
sys     1m23.068s
```

Alternatively, if you aren't comfortable writing SQL or prefer to stay in
python, the same thing can be achieved using
[sqlalchemy](https://www.sqlalchemy.org/) and pandas'
[to_sql](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html)
method, though we'd need to iterate over the csv file in chunks in order to do
so.

```python
import sqlalchemy as sa
engine = sa.create_engine("postgresql://brooks:@/checkouts")
for partial_df in pd.read_csv("./Checkouts_by_Title.csv", chunksize=100_000):
    partial_df.to_sql("checkouts", engine, if_exists="append", index=False)
```

That's amazing! The incredible amount of flexibility that pandas
and the python ecosystem provides is why I love working with them.

Regardless, now that the data is all inserted, let's move on to the analysis.

## How many items were checked out last year?
Can be answered with the following query
```sql
WITH checkouts_last_year AS (
    SELECT checkouts
    FROM checkouts
    WHERE checkout_year = 2018
)

SELECT sum(checkouts) AS total_checkouts
FROM checkouts_last_year
```

**Answer**
```sql
total_checkouts
-----------------
         9149176
(1 row)
```

With the `checkout_year` index, this query took less than 2 seconds. Without
the index we created on the table, it took 36.

## How popular is digital material compared to physical material?
and is that increasing or decreasing?
```sql
SELECT
    checkout_year, usage_class, SUM(checkouts)
FROM checkouts
GROUP BY usage_class, checkout_year
ORDER BY usage_class, checkout_year
```

**Answer**
```
 checkout_year | usage_class |   sum
---------------+-------------+---------
          2005 | Digital     |    3959
          2006 | Digital     |   16839
          2007 | Digital     |   34620
          2008 | Digital     |   63945
          2009 | Digital     |   99329
          2010 | Digital     |  183920
          2011 | Digital     |  536937
          2012 | Digital     |  863922
          2013 | Digital     | 1192836
          2014 | Digital     | 1719202
          2015 | Digital     | 2212553
          2016 | Digital     | 2452733
          2017 | Digital     | 2752214
          2018 | Digital     | 3046521
          2019 | Digital     | 2538416
          2005 | Physical    | 3794726
          2006 | Physical    | 6582479
          2007 | Physical    | 7092007
          2008 | Physical    | 8374541
          2009 | Physical    | 9035838
          2010 | Physical    | 8425046
          2011 | Physical    | 7784795
          2012 | Physical    | 7299124
          2013 | Physical    | 7864260
          2014 | Physical    | 7416879
          2015 | Physical    | 6871626
          2016 | Physical    | 6568318
          2017 | Physical    | 6479434
          2018 | Physical    | 6102655
          2019 | Physical    | 4385334
(30 rows)
```
Currently, physical material is around twice as popular, but you can see that
over time digital material is rapidly gaining ground. If we were to plot these
on a graph, we could forecast the year that digital material becomes more
popular.

> Also note that 2019 has less total checkouts than the past several years,
> which at first glance would seem worrying, but it is October right now, so
> we're only seeing partial data for 2019.

## What subjects are most often checked out?
Ah, this is a challenge. Can you see why? Our data currently resides in one
large table.
```
                  Table "public.checkouts"
      Column      |  Type   | Collation | Nullable | Default
------------------+---------+-----------+----------+---------
 usage_class      | text    |           |          |
 checkout_type    | text    |           |          |
 material_type    | text    |           |          |
 checkout_year    | integer |           |          |
 checkout_month   | integer |           |          |
 checkouts        | integer |           |          |
 title            | text    |           |          |
 creator          | text    |           |          |
 subjects         | text    |           |          |
 publisher        | text    |           |          |
 publication_year | text    |           |          |
Indexes:
    "year_idx" btree (checkout_year)
```
The previous questions were easily answered because it involved summing up
whole columns from rows, based on another column. But take a look at the
`subjects` column.

```sql
SELECT subjects FROM checkouts LIMIT 1
```
```
                     subjects
---------------------------------------------------
 Music for meditation, New Age music, Zither music
(1 row)

```
Each row contains a comma-separated list of subjects. In a normalized database,
there would be a second table with a list of subjects which we could easily
query for the answer, but not so in this case. Luckily, postgres has a bunch of
nifty functions built-in that allow us to accomplish the same thing.

Starting off, we have the `string_to_array` function, which allows us to access
each subject individually.

```sql
SELECT string_to_array(subjects, ',') FROM checkouts LIMIT 1
```

```
                                string_to_array
--------------------------------------------------------------------------------
 {Aleuts," Natural history Alaska Aleutian Islands"," Aleutian Islands Alaska"}
(1 row)
```

This is useful, but even more so when combined with the `unnest` function,
which breaks up an array into multiple rows.
```sql
SELECT unnest(string_to_array(subjects, ',')) FROM checkouts LIMIT 3
```

```
                  unnest
------------------------------------------
 Aleuts
  Natural history Alaska Aleutian Islands
  Aleutian Islands Alaska
(3 rows)
```
> Note I had to change from `LIMIT 1` to `LIMIT 3` to accommodate that there
> are now more rows

Even better, we can simply add other columns, and they take on the values of
the original row
```sql
SELECT
    checkout_year,
    checkout_month,
    checkouts,
    unnest(string_to_array(subjects, ','))
FROM checkouts
LIMIT 3
```

```
 checkout_year | checkout_month | checkouts |                  unnest
---------------+----------------+-----------+------------------------------------------
          2016 |              3 |         1 | Aleuts
          2016 |              3 |         1 |  Natural history Alaska Aleutian Islands
          2016 |              3 |         1 |  Aleutian Islands Alaska
(3 rows)
```

Now we're cooking with fire! Finally, we can trim any leading or trailing
whitespaces, group the subject count by year (rather than by book, as is the
case without a group by), and clean up the column names for ease of use.

```sql
WITH subject_popularity AS (
    SELECT
        checkout_year AS year,
        checkout_month AS month,
        checkouts AS checkouts,
        TRIM(unnest(string_to_array(subjects, ','))) AS subject
    FROM checkouts
)

SELECT
    MAX(year) AS year,
    SUM(checkouts) AS checkouts,
    MAX(subject) AS subject
FROM subject_popularity
GROUP BY subject, year
ORDER BY year DESC, checkouts DESC
LIMIT 10
```

The only problem? This is a computationally expensive question. On my computer,
the query took about 15 minutes to complete. The database has to take each row
and expand it out by the number of subjects contained within in order to group
them appropriately. How many rows would that be? We can estimate it.
```sql
WITH top_checkouts AS (
    SELECT * from checkouts limit 10000
)

SELECT
    AVG(array_length(string_to_array(subjects, ','), 1))
FROM top_checkouts
```

```
        avg
--------------------
 3.8237366619689954
(1 row)
```

This, multiplied by the 35m rows is about 133m. 133 million rows are needed to
calculate the number of checkouts per subject per year, as specified by
```sql
GROUP BY subject, year
```
in the previous query. No wonder it takes so long!

**Side note**, if you want to visualize the bottlenecks of a query, there are
various sites that take query plans and turn them in to charts. I've found
[this site](http://tatiyants.com/pev) to be extremely useful in visualizing
what part of my query took the longest.

There's one more trick up our sleeve that we can do to make this data faster to
access, and that is by putting it in a materialized view. In summary,
materialized views allow you to cache the results of a query and allows you to
periodically refresh the data. Creating the view will initially take as long as
running the original query, but future queries will be much faster against it.

```sql
CREATE MATERIALIZED VIEW yearly_subject_popularity AS
<original query>
```

Finally we can answer the original question. What subjects are most popular?

```sql
SELECT * FROM yearly_subject_popularity ORDER BY year DESC, checkouts DESC
LIMIT 10;
```
```
 year | checkouts |                  subject
------+-----------+-------------------------------------------
 2019 |   1348448 | Fiction
 2019 |    854448 | Video recordings for the hearing impaired
 2019 |    807154 | Nonfiction
 2019 |    684857 | Feature films
 2019 |    603138 | Fiction films
 2019 |    524205 | Literature
 2019 |    334981 | Thriller
 2019 |    323856 | Mystery
 2019 |    319389 | Romance
 2019 |    318219 | Fantasy
(10 rows)
```

## Conclusion

Databases are a great place to store lots of data, because that's what they're
meant to do. They have an incredible amount of power, if you know how to use
them correctly. For this type of exercise, it was not bad. Ingesting the csv
file into a database table was a breeze, as was answering more straightforward
questions about the data.

Answering the popular subjects question was much more difficult. The way the
data was formatted in one big table with no normalization meant that the
solution I came up with was inefficient, and took longer than it would have,
had the data been more properly formatted.

But then that's part of the challenge, isn't it? We'll rarely have clean data
handed to us in the real world; making the best out of what what is given is an
essential skill to have.

I leveled up my database foo in the process of answering this question. For
someone who is not a DBA, the largest obstacle I had to overcome was
understanding best way to approach the problem. Knowing beforehand what
questions I needed to answer helped immensely, as each question presents a new
challenge - but that's true for any problem.

If I had to do re-do this exercise, I would definitely reach for a database as
part of my solution toolbox again. In the future, I want to explore a better
way of normalizing the data as it gets ingested, so the more tricky analysis
questions are easier to answer.
