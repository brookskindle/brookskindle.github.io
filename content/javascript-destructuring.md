Title: Write readable code with object destructuring
Date: 2019-11-15
Category: programming
Tags: javascript


When I started writing Python, I quickly fell in love with [keyword and
keyword-only
arguments](https://treyhunner.com/2018/04/keyword-arguments-in-python/#Keyword-only_arguments_without_positional_arguments)
because I realized they could make my code much more readable and robust. When
I started writing Javascript, I was disappointed that there was no such thing.
Until I read about object destructuring.

## What is object destructuring?
Object destructuring, at it's core, allows you to initialize variables from
existing objects. Suppose you have the following object
```js
const player = {
  username: 'SpoopyTuna',
  email: 'spoopytuna@mail.com',
}
```

If you wanted to extract the username and email fields into separate variables,
you could write
```jq
const username = player.username
const email = player.email
```

But with destructuring, this can be combined into a single line
```js
const { username, email } = player
```

This is great, and can make parts of your code more concise by condensing
variable initialization, but the real power of destructuring is that it allows
functions to have pseudo-named parameters.

## Pseudo-what?
As a somewhat contrived example, imagine a greeting function that takes a name
and returns a string to greet that person.
```js
function greet (name) {
  console.log(`Greetings, ${name}!`)
}
```

It can be invoked relatively simply
```js
> greet('brooks')
Greetings, brooks!
```

Most functions are more complex than that, however. An expanded example of the
above function might be:
```js
function greet (name,
                welcomeMessage = 'Greetings',
                endingPunctuation = '!',
                capitalizeName = false) {
  if (capitalizeName) {
    name = name[0].toUpperCase() + name.substr(1, name.length - 1)
  }
  console.log(`${welcomeMessage}, ${name}${endingPunctuation}`)
}
```

The tradeoff for complexity is usually readability. In this case, it is the
function call that becomes less readable.
```js
greet('brooks', 'Welcome', '!!!', true)
```
Do you know what the output of the above line is? What if I hadn't given you
the function definition beforehand?

Without looking at the definition, it is much harder to reason about what each
additional parameter does. To make matters worse, a call signature becomes even
more convoluted if you need to to use the default value for of middle
parameter, but provide a value for a later parameter.
```js
> greet('brooks', undefined, undefined, true)
```
How's that for readability?

## The alternative to positional arguments
With object destructuring, you can clean up your function signatures to make
them much easier to call and to work with.

Simply wrap the arguments you wish to be optional inside a set of curly braces
```js
{ welcomeMessage = 'Greetings',
  endingPunctuation = '!',
  capitalizeName = false }
```

and add a default value of an empty object in case the optional parameters are
omitted when calling the function.
```js
  capitalizeName = false } = {}
```

Put together, the modified greet function looks like this:
```js
function greet (name, {
                welcomeMessage = 'Greetings',
                endingPunctuation = '!',
                capitalizeName = false } = {}) {
  if (capitalizeName) {
    name = name[0].toUpperCase() + name.substr(1, name.length - 1)
  }
  console.log(`${welcomeMessage}, ${name}${endingPunctuation}`)
}
```

Now, finally, calling our function can be readable!
```js
> greet('brooks')
Greetings, brooks!
> greet('brooks', { endingPunctuation: '?' })
Greetings, brooks?
> greet('brooks', { welcomeMessage: 'Hello there', capitalizeName: true })
Hello there, Brooks!
```
