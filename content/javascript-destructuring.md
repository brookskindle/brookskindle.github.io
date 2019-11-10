Title: Write cleaner code with object destructuring
Date: 2019-11-08
Category: programming
Tags: javascript


When I switched from writing C to Python, I quickly fell in love with [keyword
and keyword-only
arguments](https://treyhunner.com/2018/04/keyword-arguments-in-python/#Keyword-only_arguments_without_positional_arguments)
because I realized they could make my code much more readable and robust. When
I moved from Python to Javascript, I was disappointed that there was no such
thing, until I read about object destructuring.

Object destructuring, at it's core, allows you to initialize variables from
existing objects. Suppose you have the following object
```js
const player = {
  username: 'SpoopyTuna',
  email: 'spoopytuna@mail.com',
}
```

If you wanted to extract the username and email fields into separate variables,
you would traditionally write
```jq
const username = player.username
const email = player.email
```

Using destructuring, this could be combined into a single line
```js
const { username, email } = player
```

This is great, and can make parts of your code more concise by condensing
variable initialization, but the real power of destructuring is in function
signatures to provide pseudo-named parameters.

Imagine you have a function
