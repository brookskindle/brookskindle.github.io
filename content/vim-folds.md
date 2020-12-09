Title: Vim folds helped me write a markdown presentation
Date: 2019-11-27
Category: Programming
Tags: vim, markdown

Vim. For a program that was released in 1991, I am still amazed at the vast
amount of features that I both know, and have yet to learn.

One such example are folds. In vim, folds are a concept that allows you to
collapse parts of code based on rules, usually by indentation level.

Visually, when you fold code it goes from this

```go
package main

import (
    "fmt"
    "math"
)

func main() {
    fmt.Println(math.Pow(5, 2))
}
```

to this

```go
package main

+--  4 lines: import (---------------------------------

+--  3 lines: func main() {----------------------------
```

I think this is unnecessary to do for most files, but the larger your codebase
is, the more useful it is to be able to get a bird's eye view of what is going
on in a particular file (you could, for example, fold everything but functions,
classes, and methods to get a sense for what functionality the file contains)

[Since last year]({filename}/markdown-presentations.md) I've been fascinated by
the idea of creating presentations in markdown or some other markup language.
The advantage to this is that you can then version control your presentations,
as you do with your code. A couple of days ago, I created on a presentation for
work on the [basics of the Go language]({filename}/gotta-go-fast.md). I wrote
it entirely in markdown using the remark slideshow tool as the presentation
layer. In total, the presentation came to 800 lines of markdown.

What's the problem, then? As is my writing style, I tend to write things that
come to mind, and then go back later to add or edit content. Vim is a great
tool for this type of thinking, because a lot of its' functionality is aimed at
giving users the ability to make precise textual edits. However, the longer my
presentation grew, the more difficult it was to jump back and edit code from
previous slides.

Enter folds. By default, vim does not fold code, but this can be configured.
There are a couple of paths to take here, but most of them involve either
indentation or writing your own function to determine how to fold the code. I
was interested in neither. With few exception, markdown doesn't use indentation
to signify context change, like the body of a function would, and learning
to write my own indentation logic in vimscript seemed like too steep a learning
curve. There is one other option, however, which is to specify a custom fold
within the file. You can do so with `zf<motion>`.

![]({static}/images/custom-fold.gif)

Cool!

Now, since this is a one off fold, vim can't fold the rest of the file
automatically, but that's fine. I ended up making a macro to fold a single
slide, and then runing that macro over the rest of the file - automatically
folding each slide. The end result looks something like this

![]({static}/images/fold-macro.png)

That's much easier to work with than eight-hundred pages of un-folded markdown!
