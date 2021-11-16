# Easy string manipulation tools for the shell
 `strs` makes working with strings in the shell easier.

[String manipulation in POSIX-compliant shells](https://shellmagic.xyz/#string-manipulation) can be both confusing and cumbersome. `strs` brings string convenience methods from Python to shells like Bash.

# Examples
`strs` provides commands for string manipulation actions that are built into Bash, and it provides commands for things that Bash doesn't do, as well.

Here are some ways you can manipulate strings with both Bash and `strs`:
```bash
#!/usr/bin/env bash
export string='This is an example.'

## String length
# Bash
echo ${#string}

# strs
strs length $string

# or, using pipes
echo $string | strs length

## Strip from rear
export remove='example.'

# Bash
echo ${string%remove}

# strs
strs rstrip $remove $string

# or, using pipes
echo $string | strs rstrip $remove

## Strip from front
export remove='This'
# Bash
echo ${string#remove}

# vs
strs lstrip $remove $string

# or, using pipes
echo $string | strs lstrip $remove

## Replace all
export replace='an'
export with='a'

echo ${string//replace/with}

# vs
strs replace $replace $with $string

# or, using pipes
echo $string | strs replace $replace $with

## Replace first character
echo ${string/replace/with}

# vs
strs replace $replace $with --count 1 $string

# or, using pipes
echo $string | strs replace $replace $with --count 1

## Capitalization
echo ${string^}  # capitalize first char
echo ${string^^} # capitalize all
echo ${string,,} # lower all

# vs
strs capitalize $string  # capitalize first char
strs upper $string  # capitalize all
strs lower $string  # lower all

# or
echo $string | strs capitalize $string
echo $string | strs upper
echo $string | strs lower
```

Here are some string manipulation commands that come with `strs` but not with Bash:
```bash
#!/usr/bin/env bash
export string='This is an example.'

# casefold
strs casefold $string
# or
echo $string | strs casefold

# center
strs center $string
# or
echo $string | strs center

# count
export countChar='e'
strs count $countChar $string
# or
echo $string | strs count $countChar

# ends with
export dot='.'

strs endswith $dot $string
# or
echo $string | strs endswith $dot

# find
export find='e'

strs find $find $string
# or
echo $string | strs find $find

# index
strs index $find $string
# or
echo $string | strs index $find

# join
export on='\n'

strs join $on $string
# or
echo $string | strs join $on

# ljust
export width=20

strs ljust $width $string
# or
echo $string | strs ljust $width

# lstrip
export remove='.'

strs lstrip $remove $string
# or
echo $string | strs lstrip $remove

# partition
export part=' '

strs partition $part $string
# or
echo $string | strs partition $part

# rfind
export find='e'

strs rfind $find $string
# or
echo $string | strs rfind $find

# rindex
strs rindex $find $string
# or
echo $string | strs rindex $find

# rjust
export width=20

strs rjust $width $string
# or
echo $string | strs rjust $width

# rstrip
export remove='.'

strs rstrip $remove $string
# or
echo $string | strs rstrip $remove

# rpartition
export part=' '

strs rpartition $part $string
# or
echo $string | strs rpartition $part

# rsplit
export split=' '

strs rsplit $split $string
# or
echo $string | strs rsplit $split

# split
export split=' '

strs split $split $string
# or
echo $string | strs split $split

# strip
export strip='.'

strs strip $strip $string
# or
echo $string | strs split $strip

# swap case
strs swapcase $string
# or
echo $string | strs swapcase

# starts with
export t='T'

strs startswith $t $string
# or
echo $string | strs startswith $t

# to title case
strs title $string
# or
echo $string | strs title

# zero fill
export width=20

strs zfill $width $string
# or
echo $string | strs zfill $width
```

`strs` also brings Python's string validation methods to the shell:
```bash
#!/usr/bin/env bash
export string='This is an example.'

# is alphanumeric
strs isalnum $string
echo $string | strs isalnum

# is alphabetic
strs isalpha $string
echo $string | strs isalpha

# is ASCII
strs isascii $string
echo $string | strs isascii

# is decimal
strs isdecimal $string
echo $string | strs isdecimal

# is digit
strs isdigit $string
echo $string | strs isdigit

# is valid Python identifier
strs isidentifier $string
echo $string | strs isidentifier

# is lower case
strs islower $string
echo $string | strs islower

# is numeric
strs isnumeric $string
echo $string | strs isnumeric

# is printable
strs isprintable $string
echo $string | strs isprintable

# is space character
strs isspace $string
echo $string | strs isspace

# is title case
strs istitle $string
echo $string | strs istitle

# is upper case
strs isupper $string
echo $string | strs isupper
```
