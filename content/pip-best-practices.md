Title: Pin your versions. Or don't.
Date: 2018-06-25
Category: programming
Tags: python, pip
Status: draft

Suppose you're starting a new project at work that will use the `requests`
library. Should you be explicit and pin the versions of all your installed
libraries (equivalent to the output of `pip freeze`)
```pip
certifi==2018.4.16
chardet==3.0.4
idna==2.7
pkg-resources==0.0.0
requests==2.19.1
urllib3==1.23
```

or should you just list the top-most dependencies by name, omitting versions
altogether?
```pip
requests
```

The answer to that depends on what kind of environment you expect your project
to be ran in. In short, if the project is an application, you should pin your
versions. If the project is a library or module, pin versions as little as
possible. To understand why, you need to understand the differences between
modules and applications.

An application is a complete system. Its purpose is to provide functionality to
the end-user. It is composed of multiple modules, and exists independent of
other applications. Communication between applications happens via a defined
interface. Communication to a different application likely happens along a
well-desined communication standard such as REST or ftp.

Applications are designed to be used as a complete system, as as such need to
make sure that new installations will still work regardless of the change in
environment

A module, on the other hand, is only part of the complete system. Modules are
meant to be used in applications, and therefore must be as flexible as possible
so as to not introduce conflicts with other modules when they get used. A
python module that requires `requests==2.19.1`, for example, cannot be used
with another python module that requires a different version (for eg:
`requests==2.18.1`). However, if two modules only require that `requests` be
installed, regardless of the version, then they will have no problem being used
together.
