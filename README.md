# URL Shortener backend in AWS Lambda

[![Build Status](https://travis-ci.com/NikStoyanov/urlshortapi.svg?branch=master)](https://travis-ci.com/NikStoyanov/urlshortapi)

This package implements a bijective function which performs a one-to-one
correspondence to define a URL shortener.

```
a('abcd') = 1234
```

Which produces:

```
b(1234) = 'abcd'
```
