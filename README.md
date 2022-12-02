# camelCasing Package

This package converts Pascal Case and snake_case strings into its camelCase
equivalent.


## Installation


```
pip install camelCasing
```


## Basic Use

```
from camelCasing import camelCasing as cc
```

Its functionality can be used in at least two ways:


(1) Individually:

```
# recode a single string
cc.toCamelCase(s='TheQuickBrownFox', user_acronyms=None)
```

or (2) in list comprehensions:

```
# get camelCase replacements for an arbitrary dataframe
[cc.toCamelCase(s=s, user_acronyms=None) for s in df.columns]
```

## User Defined Acronyms

One of the tricky problems facing camel case text generation is the problem
of acronyms. This package allows for user defined acronyms that the program
should look for and account for when creating its camelCase equivalent.

Consider the following example:

```
s = 'UefiDbx_UefiDbxKeyStatus'
cc.toCamelCase(s=s, user_acronyms=['WMI', 'FRU', 'SKU', 'UEFI'])  # UEFIDbxUEFIDbxKeyStatus

s = 'iaasByMicrosoft'
cc.toCamelCase(s=s, user_acronyms=['IaaS'])  # IaaSByMicrosoft
```

This functionality lets you have control over the acronyms that you want to keep and maintain.
