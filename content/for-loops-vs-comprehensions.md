Title: For loop and list comprehension performance
Date: 2018-04-27 9:00PM
Category: programming
Tags: python

For loops are the de facto default looping mechanism for python and is a
concept that almost all programmers are familiar with. However, if you've been
around the python block a few times you've probably seen (and maybe dabbled in)
list comprehensions from time to time. While there are scenarios where it makes
sense to use a for loop over a list comprehension and vice versa, I'll be
instead covering the difference in speed between the two.

# Setting the stage
I'm going to use the following trivial snippets of code when running the
comparisons:

for loop
```python
mylist = []
for i in range(n):
    mylist.append(n)
```

list comprehension
```python
mylist = [i for i in range(n)]
```

For varying values of `n`.

# timeit
The easiest way to measure the runtime of code snippets is by using the
[timeit](https://docs.python.org/3/library/timeit.html) module. I'll be using
ipython's built-in magic command for this.

To create a list of one-hundred thousand elements, it takes ~15 milliseconds
in a for loop
```python
In [1]: %%timeit
   ...: mylist = []
   ...: for i in range(100000):
   ...:     mylist.append(i)
   ...:
14.9 ms ± 206 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

but only ~6 milliseconds to do the same thing with a list comprehension.
```python
In [2]: %%timeit
   ...: mylist = [i for i in range(100000)]
   ...:
6.09 ms ± 53.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

In this example, the list comprehension is over **2.4x** faster than the for
loop equivalent.

---

If I instead iterate over one-thousand elements, the results are similar.
```python
In [10]: %%timeit
    ...: mylist = []
    ...: for i in range(1000):
    ...:     mylist.append(i)
    ...:
123 µs ± 568 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

```python
In [12]: %%timeit
    ...: mylist = [i for i in range(1000)]
    ...:
53.5 µs ± 709 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

A **2.3x** speed improvement when using a list comprehension.

For two pieces of code that produce the same result, it seems surprising that
there is such a performance difference. There must be something going on under
the hood that makes list comprehensions so much more performant.

# dis
Python has a really cool built-in module named
[dis](https://docs.python.org/3/library/dis.html) (short for disassemble). We
can use it to disassemble pieces of code into their opcode equivalent to see
what each line of code does.

Running this code
```python
import dis

dis.dis("""\
mylist = []
for i in range(1000):
    mylist.append(i)""")
```

gives as output:
```
  1           0 BUILD_LIST               0
              3 STORE_NAME               0 (mylist)

  2           6 SETUP_LOOP              33 (to 42)
              9 LOAD_NAME                1 (range)
             12 LOAD_CONST               0 (1000)
             15 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             18 GET_ITER
        >>   19 FOR_ITER                19 (to 41)
             22 STORE_NAME               2 (i)

  3          25 LOAD_NAME                0 (mylist)
             28 LOAD_ATTR                3 (append)
             31 LOAD_NAME                2 (i)
             34 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             37 POP_TOP
             38 JUMP_ABSOLUTE           19
        >>   41 POP_BLOCK
        >>   42 LOAD_CONST               1 (None)
             45 RETURN_VALUE
```
The left-most set of numbers (1, 2, and 3) represent the particular line being
disassembled, while the second set of numbers (0, 3, 6, 9, 12, 15, etc...)
represent the offset that the given opcode is from the start of the bytecode
sequence.

Compare that to disassembling a list comprehension

```python
import dis

dis.dis("mylist = [i for i in range(1000)]")
```

```
  1           0 LOAD_CONST               0 (<code object <listcomp> at 0x7f4d22d959c0, file "<dis>", line 1>)
              3 LOAD_CONST               1 ('<listcomp>')
              6 MAKE_FUNCTION            0
              9 LOAD_NAME                0 (range)
             12 LOAD_CONST               2 (1000)
             15 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             18 GET_ITER
             19 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             22 STORE_NAME               1 (mylist)
             25 LOAD_CONST               3 (None)
             28 RETURN_VALUE
```

The final opcode for a list comprehension is only at a bytecode offset of `28`,
whereas the for loop final offset was `45`. Although we haven't disassembled
the bytecode into machine instructions, we can still see that list
comprehensions take less operations than a for loop would for equivalent code.
