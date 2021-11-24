# 🧵 Easy string tools for the shell
 `strs` makes working with strings in the [shell](https://linuxcommand.org/lc3_lts0010.php) easier.

[String manipulation in POSIX-compliant shells](https://shellmagic.xyz/#string-manipulation) can be both confusing and cumbersome. `strs` brings string convenience methods from Python to shells like Bash.

```bash
$ str capitalize "hey there! :fire:" | str to-emoji 
Hey there! 🔥
```

# Installation
## Prerequisites
 - A Unix shell like Bash, or PowerShell or Command Prompt on Windows
 - Python 3.10+
 - `requirements.txt`

## PyPI
```bash
python3 -m pip install strs
```

# Examples
## Practical example
If you're using Debian, you might want to share your [apt sources](https://wiki.debian.org/SourcesList) file between your machines. You might run Debian `testing` on one machine, but Debian `stable` would suit the use case of another.

Using `strs`, you can take your apt sources from `testing` and point them to `stable` on the fly, and send them to your other your other machine:
```bash
$ str replace testing stable < sources.list | ssh hostname "cat > /etc/apt/sources.list"
```

You could do the same thing with `sed`, but that requires knowing `sed`'s regex syntax, whether or not the version of `sed` you have is [new enough to ship with the `-i` feature flag](https://unix.stackexchange.com/questions/401905/bsd-sed-vs-gnu-sed-and-i), and [the differences between GNU `sed` and BSD `sed`](https://riptutorial.com/sed/topic/9436/bsd-macos-sed-vs--gnu-sed-vs--the-posix-sed-specification).

`strs`, on the other hand, has a uniform interface and set of features across platforms, and across POSIX shells and on Windows. 

## Shell string manipulation
`strs` provides string tools that are similar to those that are built into Bash, and it provides commands for things that Bash doesn't have syntactic sugar for, as well. The following examples of Bash code only work with Bash, whereas `strs` will work the same no matter if you're using Bash, zsh or PowerShell.

Here are some ways you can manipulate strings with both Bash and `strs`:
```bash
#!/usr/bin/env bash
string='This is an example.'

## String length
# Bash
echo "${#string}"

# str
str length "$string"

# or, using pipes
echo $string | str length

## Strip
removeFront='This'
removeEnd='example.'

# Bash
echo "${string#$removeFront}"  # from front
echo "${string%$removeEnd}"  # from end

# str
str lstrip $removeFront "$string"  # front
str rstrip $removeEnd "$string"  # end

# or, using pipes
echo $string | str lstrip $removeFront
echo $string | str rstrip $removeEnd

## Replace
old='an'
new='a'

echo "${string//$old/$new}"  # replace all
echo "${string/$old/$new}"  # replace first

# vs
str replace $old $new "$string"  # all
str replace $old $new --count 1 "$string"  # first
str replace_first $old $new "$string"  # first

# or, using pipes
echo $string | str replace $old $new
echo $string | str replace $old $new --count 1
echo $string | str replace_first $old $new

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

## More string tools
There are some string manipulation commands that `strs` comes with that don't have syntactic sugar in Bash:
```bash
#!/usr/bin/env bash
string='This is an example.'
width=20
countChar='e'
dot='.'
find='e'
on='\n'
remove='.'
part=' '
split=' '
t='T'

# casefold
str casefold "$string"

# or
echo $string | str casefold

# center
str center $width "$string"
echo $string | str center $width

# count
str count $countChar "$string"
echo $string | str count $countChar

# ends with
str endswith $dot "$string"
echo $string | str endswith $dot

# find
str find $find "$string"
echo $string | str find $find

# index
str index $find "$string"
echo $string | str index $find

# join
str join $on "$string"
echo $string | str join $on

# ljust
str ljust $width "$string"
echo $string | str ljust $width

# lstrip
str lstrip $remove "$string"
echo $string | str lstrip $remove

# partition
str partition "$part" "$string"
echo $string | str partition "$part"

# rfind
str rfind $find "$string"
echo $string | str rfind $find

# rindex
str rindex $find "$string"
echo $string | str rindex $find

# rjust
str rjust $width "$string"
echo $string | str rjust $width

# rstrip
str rstrip $remove "$string"
echo $string | str rstrip $remove

# rpartition
str rpartition "$part" "$string"
echo $string | str rpartition "$part"

# rsplit
str rsplit $split "$string"
echo $string | str rsplit $split

# split
str split $split "$string"
echo $string | str split $split

# strip
str strip $strip "$string"
echo $string | str strip $strip

# swap case
str swapcase "$string"
echo $string | str swapcase

# starts with
str startswith $t "$string"
echo $string | str startswith $t

# to title case
str title "$string"
echo $string | str title

# zero fill
str zfill $width "$string"
echo $string | str zfill $width

# repeat
str repeat 3 "$string"
echo $string | str repeat 3
```

## String validation tools
`strs` also brings Python's string validation methods to the shell:
```bash
#!/usr/bin/env bash
string='This is an example.'

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
