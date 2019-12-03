class: center, middle

# Go
Pointers, structs, and interfaces

(oh my)

---

# Pointers

A variable whose value is, not a normal value, but the memory address of
another variable

--

<hr>

Value in memory - `42`

--

Assigned to a variable - `x = 42`

--

At location - `address of x? // 0x1234`

--

<hr>

Working with pointers
* Address of operator - `&`
* Dereference operator - `*`

---

# Pointers

```go
package main

import (
    "fmt"
)

func main() {
    var a int = 42
    var b *int = &a

    *b++

    fmt.Printf("value of a: %d, address of a: %p\n", a, &a)
    fmt.Printf("value of b: %p, address of b: %p\n", b, &b)
    fmt.Printf("value of b: %d, address of b: %p\n", b, &b)
    fmt.Println("&a == b", &a == b)
    fmt.Println("a == *b", a == *b)
}
```

--

```console
$ go run pointers.go
value of a: 43, address of a: 0xc000092010
value of b: 0xc000092010, address of b: 0xc000094018
value of b: 824634318864, address of b: 0xc000094018
&a == b true
a == *b true
```

---

# Array of integers
```go
package main

import "fmt"

func main() {
    numbers := [...]int{11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    for i := 0; i < len(numbers); i++ {
        fmt.Printf("%d\t%p\n", numbers[i], &numbers[i])
    }
}
```

--

```console
$ go run allocation.go
11      0xc000094000
10      0xc000094008
9       0xc000094010
8       0xc000094018
7       0xc000094020
6       0xc000094028
5       0xc000094030
4       0xc000094038
3       0xc000094040
2       0xc000094048
1       0xc000094050
0       0xc000094058
```

---

# Array of integers cont.
```go
package main

import "fmt"

func main() {
*   numbers := [...]int8{11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    for i := 0; i < len(numbers); i++ {
        fmt.Printf("%d\t%p\n", numbers[i], &numbers[i])
    }
}
```

```console
$ go run allocation.go
11      0xc000092010
10      0xc000092011
9       0xc000092012
8       0xc000092013
7       0xc000092014
6       0xc000092015
5       0xc000092016
4       0xc000092017
3       0xc000092018
2       0xc000092019
1       0xc00009201a
0       0xc00009201b
```

???

Was the previous slide's example running on 32 or 64 bit architecture?

---

# Structs

```go
type item struct {
    name string
    price int
}

func NewItem(name string, price int) *item {
    i := item{name: name, price: price}
    return &i
}

func main() {
    fmt.Println(item{"Red Scarf", 25})
    fmt.Println(item{name: "Grey Shoes", price: 25})
    fmt.Println(item{})

    var purchase *item = NewItem("Green Sweater", 50)
    purchase.price = 10
    fmt.Println(purchase)
}
```

???

* Can create structs with no values (zeroes for values)
    * Ensure proper struct creation with a "constructor" function

---

# Structs

```go
type item struct {
    name string
    price int
}

*func NewItem(name string, price int) *item {
*   i := item{name: name, price: price}
*   return &i
*}

func main() {
    fmt.Println(item{"Red Scarf", 25})
    fmt.Println(item{name: "Grey Shoes", price: 25})
    fmt.Println(item{})

    var purchase *item = NewItem("Green Sweater", 50)
    purchase.price = 10
    fmt.Println(purchase)
}
```

???

* Can create structs with no values (zeroes for values)
    * Ensure proper struct creation with a "constructor" function

---

# Should I return a pointer or a value?
```go
func NewItem(name string, price int) *item {
    i := item{name: name, price: price}
    return &i
}
```

```go
func NewItem(name string, price int) item {
    i := item{name: name, price: price}
    return i
}
```

???

Which is better?

* Go recommends pass values, rather than pointers.
    * Except in the case of large structs, or small structs that might grow

--

Go recommends: https://github.com/golang/go/wiki/CodeReviewComments#pass-values

---

# Structs example
Let's update the contents of a struct

```go
type item struct {
    name string
    price int
}

func NewItem(name string, price int) item {
    i := item{name: name, price: price}
    return i
}

*func discountBy(i item, amount int) {
*   i.price -= amount
*}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
    discountBy(cardigan, 70)

    fmt.Println(cardigan.price)
}
```

--

```console
$ go run items.go
90
```

???

The output is 90? I expected the price to be reduced.

---

# Structs example with pointers
Let's update the contents of a struct

```go
type item struct {
    name string
    price int
}

func NewItem(name string, price int) item {
    i := item{name: name, price: price}
    return i
}

*func discountBy(i *item, amount int) {
    i.price -= amount
}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
*   discountBy(&cardigan, 70)

    fmt.Println(cardigan.price)
}
```

```console
$ go run items.go
*20
```

???

What are some other ways we can do the same thing?
* Return a new `item` object from discountBy
* Make it a method on the class instead of a stand-alone method
    * But Go doesn't have classes, they have interfaces

---

# Methods

```go
type item struct {
    name string
    price int
}

func NewItem(name string, price int) item {
    i := item{name: name, price: price}
    return i
}

*func (i item) discountBy(amount int) {
*   i.price -= amount
*}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
*   cardigan.discountBy(70)

    fmt.Println(cardigan.price)
}
```

???

* `(i item)` is called a receiver.

--

```console
$ go run items.go
90
```

???

* Same problem as last time. We pass the receiver by value.
    * Original price isn't updated
    * We can pass a receiver pointer, instead.

---

# Methods

```go
type item struct {
    name string
    price int
}

func NewItem(name string, price int) item {
    i := item{name: name, price: price}
    return i
}

*func (i *item) discountBy(amount int) {
    i.price -= amount
}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
    cardigan.discountBy(70)

    fmt.Println(cardigan.price)
}
```

```console
$ go run items.go
*20
```

???

Use receiver pointers if
* you need to modify a value instead of returning
* if your object is large (prevent copy overhead)

---

# Interfaces

```go
*type limitedQuantityItem struct {
    name string
    price int
*   quantity int
}

func (i *limitedQuantityItem) discountBy(amount int) {
    i.price -= amount
}

*func updateDiscount(i *item) {
*   // fetch discount price from an API
*   i.discountBy(discount)
*}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
    var sweater limitedQuantityItem = NewLimitedQuantityItem("Sweater", 45)
*   updateDiscount(&cardigan)
*   updateDiscount(&sweater)
}
```

--

```console
$ go run items.go
# command-line-arguments
./item.go:41:20: cannot use &sweater (type *limitedQuantityItem) as type *item
    in argument to updateDiscount
```

???

How can a function accept multiple types?
* IE, polymorphism

---

# Interfaces

```go
type limitedQuantityItem struct {
    name string
    price int
    quantity int
}

func (i *limitedQuantityItem) discountBy(amount int) {
    i.price -= amount
}

*func updateDiscount(i *item) {
    // fetch discount price from an API
    i.discountBy(discount)
}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
    var sweater limitedQuantityItem = NewLimitedQuantityItem("Sweater", 45)
    updateDiscount(&cardigan)
*   updateDiscount(&sweater)
}
```

```console
$ go run items.go
# command-line-arguments
./item.go:41:20: cannot use &sweater (type *limitedQuantityItem) as type *item
    in argument to updateDiscount
```

---

# Interfaces

```go
*type itemInterface interface {
*   discountBy(int)
*}

*func updateDiscount(i itemInterface) {
    // fetch discount price from an API
    i.DiscountBy(40)
}

func main() {
    var cardigan item = NewItem("Cardigan", 90)
    var sweater limitedQuantityItem = NewLimitedQuantityItem("Sweater", 45, 10)
    updateDiscount(&cardigan)
    updateDiscount(&sweater)

    fmt.Println(cardigan.price)
    fmt.Println(sweater.price)
}
```

```console
$ go run items.go
50
5
```

---

class: center, middle

# Bye
