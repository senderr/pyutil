# pyutil - collection of vanilla python utilities

## Overview
- **pyutil.cache:** utility for caching functions / callables
- **pyutil.dict:** utilities for dicts
- **pyutil.enums:** utilities for enums
- **pyutil.hashing:** utilities for hashing objects
- **pyutil.io:** utilities for input/output
- **pyutil.misc:** miscellaneous utilities
- **pyutil.profiling:** utilities for profiling code


## Installation
`pip install git+ssh://git@github.com/senderr/pyutil.git`

## Caching
Use the `@pyutil.cache.cached` decorator to cache the result of a function with given arguments.

```
import requests
from pyutil.cache import cached

@cached("/cache", path_seperators=["url"])
def query_api(url, params={}):
      return requests.get(url, params=params).json()

query_api("google.com")
query_api("google.com", {"abc": 1})
query_api("twitter.com")

# Running the above code will save results to disk like so:
# /cache$ ls
# google.com twitter.com                                               # these are directories
# /cache$ cd google.com
# /cache/google.com$ ls
# 9bb39db2d9e6661b0d6ffe4cf690a03e h5u3idb2d9j4i31b0d6ffe448fj3483j    # these are files, one for the two distinct calls to query_api() with "google.com" as the url

# Future calls to query_api("google.com") will simply load the pickled file saved in /cache/google.com/9bb39db2d9e6661b0d6ffe4cf690a03e
```

## Enums
NameEnum is a base class for creating simple string enumerations:

```
from pyutil.enums import NameEnum

class Colour(NameEnum):
      red = "red"
      blue = "blue"
      green = "green"

# Access enum values:
# Colour.red

# Get all fields in the enum:
# Colour._values()

# Iterate through the enum:
# for c in Colour:
#     print(c)
```