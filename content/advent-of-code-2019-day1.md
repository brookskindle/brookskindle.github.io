Title: Breaking my Advent of Code 2019, day 1 solution
Date: 2019-12-04
Category: programming
Tags: python

The [Advent of Code 2019 challenge](https://adventofcode.com/2019) is open.
These are my solutions to the problems presented on day 1.

## Part one
Asks us to figure out how much fuel is required to lift a given spacecraft
module if we know its' mass.

```python
import math
import sys

def calculate_fuel_cost(mass):
    return math.floor(mass / 3) - 2


def test_calculate_fuel_cost():
    assert calculate_fuel_cost(12) == 2
    assert calculate_fuel_cost(14) == 2
    assert calculate_fuel_cost(1969) == 654
    assert calculate_fuel_cost(100756) == 33583


def get_module_masses():
    with open("aoc-day1-input.txt") as mass_file:
        masses = [int(line) for line in mass_file]
    return masses


def main():
    masses = get_module_masses()
    fuel_costs = [calculate_fuel_cost(mass) for mass in masses]

    print(sum(fuel_costs))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_calculate_fuel_cost()
    else:
        main()
```


## Part two
Asks us to make our fuel equation more accurate, to account for the additional
mass incurred by the fuel itself. In this case, only the fuel calculation
function needs to be updated (and corresponding tests). Everything else can
stay the same.

```python
def calculate_fuel_cost(mass):
    cost = math.floor(mass / 3) - 2
    if cost < 0:
        return 0  # No fuel required for small masses

    # Fuel also weighs an amount. Recurse to determine how much additional
    # fuel is needed just to lift the fuel off the ground.
    return cost + calculate_fuel_cost(cost)


def test_calculate_fuel_cost():
    assert calculate_fuel_cost(12) == 2
    assert calculate_fuel_cost(14) == 2
    assert calculate_fuel_cost(1969) == 966
    assert calculate_fuel_cost(100756) == 50346
```

## Breaking the code
Let's do a thought experiment. Could my implementation ever fail to give the
correct answer? For this problem, I was given an input of `100` lines with a
maximum mass of `149238`. Ignoring malformed input data, what if we had to
operate on ridiculously gigantic inputs?

The second solution involves using recursion to find a more accurate mass
calculation.

```python
return cost + calculate_fuel_cost(cost)
```

Python limits the number of recursive calls that can be made
```python
>>> import sys
>>> sys.getrecursionlimit()
1000
```
and unlike some languages, does not [optimize tail
recursion](https://www.geeksforgeeks.org/tail-call-elimination/).

What does that mean for us? If we're given a sufficiently large enough input
mass, it's possible the program will run out of recursive calls before it can
calculate the final fuel cost.

## An abnormally large mass
If we use a sufficiently large enough input, can we break it? Below I've
outlined the results of several calls to `calculate_fuel_cost`, with varying
masses.

mass|recursive calls made
---|---
100,000|9
1e10|19
1e20|40
1e30|61
1e40|82
1e300|627
1e308|644
`int(1e308) * int(1e100)`|854
`int(1e308) * int(1e167)`|994
`int(1e308) * int(1e170)`|1000

Conclusion: yes, after an abnormally large value was passed to the function, I
succeeded in breaking it.

```python
>>> calculate_fuel_cost(int(1e308) * int(1e168))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "day1-pt2.py", line 13, in calculate_fuel_cost
    return cost + calculate_fuel_cost(cost, i+1)
  File "day1-pt2.py", line 13, in calculate_fuel_cost
    return cost + calculate_fuel_cost(cost, i+1)
  File "day1-pt2.py", line 13, in calculate_fuel_cost
    return cost + calculate_fuel_cost(cost, i+1)
  [Previous line repeated 993 more times]
  File "day1-pt2.py", line 8, in calculate_fuel_cost
    print(f"Recursive calls made: {i}")
RecursionError: maximum recursion depth exceeded while calling a Python object
```

That's one massive mass.

---

Interestingly, after `1e308`, python started converting scientific notation to
the infinity value, `inf`, and attempts to pass in a slightly larger value than
that resulted in an `OverflowError` because `math.floor` was unequipped to
handle such large numbers (or consciously refused to).
```python
>>> calculate_fuel_cost(int(1e308) * 6)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "day1-pt2.py", line 5, in calculate_fuel_cost
    cost = math.floor(mass / 3) - 2
OverflowError: integer division result too large for a float
```

In the name of science, I replaced the function call with integer division

```python
cost = (mass // 3) - 2
```

to continue the experiment. The show must go on!

## A (very) large file
The other potential problem with my solution is that I read and store every
input value into an array prior to processing, instead of streaming the input
and keeping a running tally of the total fuel cost.
```python
def get_module_masses():
    with open("aoc-day1-input.txt") as mass_file:
        masses = [int(line) for line in mass_file]
    return masses
```

Effectively, my solution is an offline algorithm, not an [online
algorithm](https://www.geeksforgeeks.org/online-algorithm/), so the more input
it has to process, the more memory the program will take up. At some point, our
program will run out of memory, given enough input.

...so let's do it!

There's a couple of options to take here.

1. Create a ridiculously huge file filled with numbers, and then run the
   program like normal. This would take forever and I don't want to bother with
   writing a tens-of-gigabytes sized file to disk just for the sake of this
   program.

1. Modify the code to read numbers from stdin instead of a file. This is
   arguably the most sane solution because many command line programs have the
   option to use stdin for input, instead of a file.

1. Make the input file a named pipe (FIFO) and supply the file with an infinite
   amount of random numbers through `/dev/urandom`.

I hardly ever get to work with named pipes, so let's use the last option.
First, I'll create the file.

```console
$ mkfifo aoc-day1-input.txt
$ ls aoc-day1-input.txt
prw-r--r-- 1 brooks brooks 0 Dec  4 22:56 aoc-day1-input.txt
```

Then in a new terminal, use `/dev/urandom` to supply it with an
endless supply of numbers.

```console
$ cat /dev/urandom | tr -dc '1-9' | fold -w 2 > aoc-day1-input.txt
```

Finally, I'll run the program and watch the memory usage slowly increase

```console
$ python day1.py
```

time|system memory usage|image
---|---|---
0 minutes|900mb|![]({static}/images/memory-balloon-initial.png)
1 minute|1.5gb|![]({static}/images/memory-balloon-1min.png)
5 minutes|2.8gb|![]({static}/images/memory-balloon-5min.png)

I stopped the program before I ran out of memory, but you get the picture.

---

There you have it - it's a good thing to keep in mind that even a program that
seems simple and straightforward can have problems if exposed to the right (or
wrong) conditions.
