Title: Making modern presentations with markdown
Date: 2018-07-18 18:00
Category: programming
Tags: markdown, presentations

This month I have the pleasure of co-teaching the Jump Start Live course for
the Ada Developers Academy - a short course designed to reinforce basic
programming concepts to students prior to the start of the full program. Part
of the course material is available online in markdown format, but the lecture
slides we use in class are Google Docs presentations. In my opinion, this is
miles above the age-old powerpoint presentation ecosystem, but given my curious
nature and the fact that the rest of the course material is in markdown, I
wanted to know: **could presentations also be written in markdown?**

Yes, in fact.

After several hours of searching on the internet, I've landed on a couple of
options for creating presentations in markdown. This isn't an exhaustive list
by any stretch of the imagination - it is simply what I think will be useful
for my own purposes.

## [remark](https://github.com/gnab/remark)
remark (not to be confused with [remark.js](https://remark.js.org/), a markdown
processor) is a web-based presentation framework that is markdown-driven. It's
quick to get started, you just need one HTML boilerplate file and you can begin
writing markdown within it.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Title</title>
    <meta charset="utf-8">
    <style>
      @import url(https://fonts.googleapis.com/css?family=Yanone+Kaffeesatz);
      @import url(https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic);
      @import url(https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,700,400italic);

      body { font-family: 'Droid Serif'; }
      h1, h2, h3 {
        font-family: 'Yanone Kaffeesatz';
        font-weight: normal;
      }
      .remark-code, .remark-inline-code { font-family: 'Ubuntu Mono'; }
    </style>
  </head>
  <body>
    <textarea id="source">
# My markdown presentation
> Created using remark

---

# Slide 2
    </textarea>
    <script src="https://remarkjs.com/downloads/remark-latest.min.js">
    </script>
    <script>
      var slideshow = remark.create();
    </script>
  </body>
</html>
```

## [reveal.js](https://github.com/hakimel/reveal.js)
reveal.js is another web-based presentation framework. Normally you have to
write the presentation in HTML, but it supports markdown as well. I've also had
success just creating a markdown document

```md
# My markdown presentation
> Created using reveal.js

# Slide 2
```

and then using `pandoc` to create the HTML presentation
```
pandoc -s input.md -o output.html -t revealjs -V revealjs-url=https://lab.hakim.se/reveal-js
```

## The verdict
It mostly boils down to preference and which one you like better.

There are some feature differences between the two, but both offer support for
speaker notes and a cloned presentation mode, which are important to me.

Initially I was drawn to reveal.js because of its looks, but the vanilla
settings don't allow for much text to fit on a single slide and thus seems more
suited for big picture ideas without going too deeply into detail.

The default settings for remark focus more on presenting the slide content in a
no way, which for me is important.

## Parting thoughts
Since markdown is the common language used, I *should* be able to transition
from one framework to the next, but I see two things that make doing so more
difficult:

* You can fit less content on a reveal.js slide by default than you can in a
  remark slide, so converting a remark presentation to a reveal.js presentation
  will probably cut off a bit of the content on each slide.

* `pandoc` [has a different
  syntax](http://pandoc.org/MANUAL.html#speaker-notes) for speaker notes [than
  remark does](https://remarkjs.com/#15), so converting presentations with
  speaker notes would become notably more difficult. If pandoc supported remark
  as an output format, this would be a non-issue.
