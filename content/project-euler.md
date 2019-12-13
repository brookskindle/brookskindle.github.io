Title: Project Euler Problem 22
Date: 2019-12-12
Category: programming
Tags: python

This is a short post, showcasing my solution to [problem 22 on Project
Euler](https://projecteuler.net/problem=22). I worked on this problem over
lunch with a few co-workers, and they found the solution useful. If you find
this article, I hope it is useful to you as well.

The prompt for this exercise is simple: given a file containing names,
calculate the total score for all names in the file. The score for a given name
can be calculated by taking sum of each character's alphabetical value (`A` is
1, `B` is 2, and so on) and multiplying it by its' position in the list,
assuming the list is alphabetically sorted from `A` to `Z`.

```python
def get_sorted_names():
    with open("names.txt") as fd:
        names = fd.read().split(",")

    # Remove the surrounding quotes from each name
    names = [name.strip('"') for name in names]

    return sorted(names)


def calculate_name_score(name):
    total = 0
    for char in name.upper():
        total += ord(char) - 64
    return total


def calculate_list_score(names):
    total = 0
    for i, name in enumerate(names):
        total += calculate_name_score(name) * (i + 1)
    return total


def main():
    names = get_sorted_names()
    score = calculate_list_score(names)

    print(f"{score:,}")


if __name__ == "__main__":
    main()
```

It requires python 3.6 or greater to run, but that requirement can be removed
if you change the f-string in the `main` function to an older `.format` style
string.
