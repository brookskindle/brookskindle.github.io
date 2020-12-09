Title: Pin your versions. Or don't.
Date: 2018-06-25
Category: programming
Tags: python

Here's a hypothetical situation. Suppose you're starting a new project and you
want to use the `requests` library. Installing `requests` also installs the
libraries that it depends on. Should you be explicit and pin the versions of
all installed libraries (equivalent to the output of `pip freeze`)
```pip
certifi==2018.4.16
chardet==3.0.4
idna==2.7
requests==2.19.1
urllib3==1.23
```

or should you just list the top-most dependencies by name, omitting versions
altogether?
```pip
requests
```

The answer depends on if your project is an application or a library, because
needs differ from one type to the next.

## Applications
An application is a complete system. Its purpose is to provide functionality to
the end-user. It is composed of multiple libraries and exists independent of
other applications. If it has to interact with other applications, that
communication happens via a well-defined API interface such as XML-RPC, SOAP,
or REST. API endpoints should be versioned so that developers who interact with
your application (or vice-versa) can be assurred that API behaviour is
well-defined and won't change unless the version changes. A good example of
this is [GitHub's API](https://developer.github.com/v3/?) - they have good
documentation as well as a consistent versioning scheme that users can rely on.

As an application builder, library versions you use are just an implementation
detail because the end user will never need to know about it. From an
application deployment perspective, **it is more important to be explicit about
which versions of libraries you need than it is to update libraries to the
latest version every time the application is deployed.** This is as true in a
continuous deployment environment as it is in any other deployment environment.

> Caveat: just because a package version works doesn't mean it should never be
> updated. As a best practice, applications that pin library versions should
> have a plan for checking and updating outdated dependencies on a regular
> basis.

## Libraries
Libraries, on the other hand, are not a complete system. They are meant to be
used in applications, and therefore must be as flexible as possible so as to
not introduce conflicts with other libraries being used. A python library that
requires `requests==2.19.1`, for example, cannot be used with another python
library that requires a different version (for eg: `requests==2.18.1`).
However, if two libraries only require that `requests` be installed, regardless
of the version, then they will have no problem being used together.

As the developer of a library, **you should not pin the versions of libraries
you depend on unless absolutely necessary.** If you depend on functionality of
a library that doesn't exist in some earlier versions, specify the earliest
version of that library as being the minimum required version (eg:
`requests>="2.18"`).

> Caveat: new versions of libraries you depend on may cause incompatibilities
> with your libraries. Since version pinning isn't recommended, responsiveness
> is important when users bring up the issue of version incompatibilities.

## Exceptions
Obviously there are exceptions to every rule.

* The more platforms/environments your application has to run on (for example,
  `vim` has to be able to run on lots of platforms), the harder it will be to
  pin exact versions.
* If you have an application that can also be used as a library, then the
  library part should be split out into its own project, and the application
  should depend on a specific version of the library.

## tl;dr
If you're building an application, pin specific versions for all the libraries
you depend on. If you're building a library, be as permissive as possible.
