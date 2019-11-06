Title: How to work with large data
Date: 2019-11-04
Category: programming
Tags: python, data, large data

Here's a question: how do you analyze data that is too big to fit into memory?

Those of you that have worked with `pandas` before are probably intimately
familiar with the following syntax, which reads csv file into a `DataFrame`
variable
```python
import pandas as pd
df = pd.read_csv('dataset.csv')
```
In smaller datasets, this is sufficient enough to load your data into memory
and allows you to focus on the more exciting parts of data analysis, such as:
cleaning, transforming, and, if you're lucky, actually analyzing the data you
spent forever tidying up. [What do you think data scientists do,
anyways?](https://www.infoworld.com/article/3228245/the-80-20-data-science-dilemma.html)

But what if the data doesn't completely fit into memory? This article explores
methods and tools that you can use when working with large data.

> I define large data as data that is too large to fit into RAM, but whose
> analysis can still be accomplished from one machine, without the use of large
> datacenters or a distributed compute network.

## The data
Today's dataset is the King Country Library System's list of [checkouts by
title](https://data.seattle.gov/Community/Checkouts-by-Title/tmmm-ytt6), dating
back to April of 2005. It is a large dataset consisting, at the time of this
writing, approximately 35 million rows. When downloaded, the csv file weighs in
at over 7 gigabytes.

```
$ ls -lh Checkouts_by_Title.csv
-rw-rw-r-- 1 brooks brooks 7.1G Oct 12 23:59 Checkouts_by_Title.csv
```

My desktop machine only has 8 gigabytes of RAM total
```
$ free -m
              total        used        free      shared  buff/cache   available
Mem:           7975        2457        3147         117        2370        5122
Swap:          2047           0        2047
```

not enough to load it all into memory.
