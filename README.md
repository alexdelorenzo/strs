# 🧵 Easy string tools for the shell
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
echo "${#string}"

# str
str length "$string"

# or, using pipes
echo $string | str length

## Strip from rear
export remove='example.'

# Bash
echo "${string%$remove}"

# str
str rstrip $remove "$string"

# or, using pipes
echo $string | str rstrip $remove

## Strip from front
export remove='This'
# Bash
echo "${string#$remove}"

# vs
str lstrip $remove "$string"

# or, using pipes
echo $string | str lstrip $remove

## Replace all
export replace='an'
export with='a'

echo "${string//$replace/$with}"

# vs
str replace $replace $with "$string"

# or, using pipes
echo $string | str replace $replace $with

## Replace first character
echo "${string/$replace/$with}"

# vs
str replace $replace $with --count 1 "$string"

# or, using pipes
echo $string | str replace $replace $with --count 1

## Capitalization
echo "${string^}"  # capitalize first char
echo "${string^^}" # capitalize all
echo "${string,,}" # lower all

# vs
str capitalize "$string"  # capitalize first char
str upper "$string"  # capitalize all
str lower "$string"  # lower all

# or
echo $string | str capitalize
echo $string | str upper
echo $string | str lower
```

## Practical example
If you use a Debian-based Linux distribution, when you want to upgrade your system to its next release, you just need to change a few names in a file.

```bash
str replace focal impish < sources.list > sources.list
```

Here are some string manipulation commands that come with `strs` but not with Bash:
```bash
#!/usr/bin/env bash
export string='This is an example.'

# casefold
str casefold "$string"

# or
echo $string | str casefold

# center
export width=20
str center $width "$string"

# or
echo $string | str center $width

# count
export countChar='e'

str count $countChar "$string"

# or
echo $string | str count $countChar

# ends with
export dot='.'

str endswith $dot "$string"

# or
echo $string | str endswith $dot

# find
export find='e'

str find $find "$string"

# or
echo $string | str find $find

# index
str index $find "$string"

# or
echo $string | str index $find

# join
export on='\n'

str join $on "$string"

# or
echo $string | str join $on

# ljust
export width=20

str ljust $width "$string"

# or
echo $string | str ljust $width

# lstrip
export remove='.'

str lstrip $remove "$string"

# or
echo $string | str lstrip $remove

# partition
export part=' '

str partition "$part" "$string"
# or
echo $string | str partition "$part"

# rfind
export find='e'

str rfind $find "$string"

# or
echo $string | str rfind $find

# rindex
str rindex $find "$string"

# or
echo $string | str rindex $find

# rjust
export width=20

str rjust $width "$string"

# or
echo $string | str rjust $width

# rstrip
export remove='.'

str rstrip $remove "$string"
# or
echo $string | str rstrip $remove

# rpartition
export part=' '

str rpartition "$part" "$string"

# or
echo $string | str rpartition "$part"

# rsplit
export split=' '

str rsplit $split "$string"

# or
echo $string | str rsplit $split

# split
export split=' '

str split $split "$string"

# or
echo $string | str split $split

# strip
export strip='.'

str strip $strip "$string"

# or
echo $string | str split $strip

# swap case
str swapcase "$string"

# or
echo $string | str swapcase

# starts with
export t='T'

str startswith $t "$string"

# or
echo $string | str startswith $t

# to title case
str title "$string"

# or
echo $string | str title

# zero fill
export width=20

str zfill $width "$string"

# or
echo $string | str zfill $width
```

`strs` also brings Python's string validation methods to the shell:
```bash
#!/usr/bin/env bash
export string='This is an example.'

# is alphanumeric
str isalnum "$string"
echo $string | str isalnum

# is alphabetic
str isalpha "$string"
echo $string | str isalpha

# is ASCII
str isascii "$string"
echo $string | str isascii

# is decimal
str isdecimal "$string"
echo $string | str isdecimal

# is digit
str isdigit "$string"
echo $string | str isdigit

# is valid Python identifier
str isidentifier "$string"
echo $string | str isidentifier

# is lower case
str islower "$string"
echo $string | str islower

# is numeric
str isnumeric "$string"
echo $string | str isnumeric

# is printable
str isprintable "$string"
echo $string | str isprintable

# is space character
str isspace "$string"
echo $string | str isspace

# is title case
str istitle "$string"
echo $string | str istitle

# is upper case
str isupper "$string"
echo $string | str isupper
```
