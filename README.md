# camelCasing Package

This package converts Pascal Case and snake_case strings into its camelCase
equivalent.


## Basic Use

Its functionality can be used in at least two ways:


(1) Individually:

```
# recode a single string
to_camel_case(s='TheQuickBrownFox', user_acronyms=None)
```

or (2) in list comprehensions:

```
# get camelCase replacements for an arbitrary dataframe
[to_camel_case(s=s, user_acronyms=None) for s in df.columns]
```

## User Defined Acronyms

One of the tricky problems facing camel case text generation is the problem
of acronyms. This package allows for user defined acronyms that the program
should look for and account for when creating its camelCase equivalent.

Consider the following example:

```
s7 = 'UefiDbx_UefiDbxKeyStatus'
assert to_camel_case(s7, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'UEFIDbxUEFIDbxKeyStatus', 'failed'
```

This functionality lets you have control over the acronyms that you want to keep and maintain.
