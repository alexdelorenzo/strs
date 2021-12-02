# 🧵 Easy string tools for the shell
 `strs` comes with more than 30 tools that make working with [strings](https://en.wikipedia.org/wiki/String_(computer_science)) in the [shell](https://linuxcommand.org/lc3_lts0010.php) easier. 

Because [string manipulation](https://en.wikichip.org/wiki/string_manipulation) in shells can be [hard](https://shellmagic.xyz/#string-manipulation), `strs` brings common string [convenience methods](https://wiki.c2.com/?ConvenienceMethods) to shells like [Bash](https://www.gnu.org/software/bash/).

```bash
$ str capitalize "hey there! :fire:" | str to-emoji
Hey there! 🔥

$ str repeat 2 ⭐ | str join 🌙
⭐ 🌙 ⭐
```

# Installation
## Prerequisites
 - A [Unix shell](https://en.wikipedia.org/wiki/Unix_shell) like Bash, or PowerShell or Command Prompt on Windows
 - Python 3.10+
 - `requirements.txt`

## PyPI
```bash
python3 -m pip install strs
```

# Examples
## Practical example
If you're using [Debian](https://www.debian.org/), you might want to share your [apt sources](https://wiki.debian.org/SourcesList) file between your machines that run Debian [`testing`](https://wiki.debian.org/DebianTesting) and [`stable`](https://wiki.debian.org/DebianStable).

Using `strs`, you can take your apt sources from `testing` and point them to `stable` on the fly, and send them to your `stable` machine:
```bash
$ str replace testing stable < sources.list | ssh hostname "cat > /etc/apt/sources.list"
```

The same can be done with [`sed`](https://en.wikipedia.org/wiki/Sed), but you would need to know [`sed`'s regex syntax](https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html), if the `sed` you have [comes with the `-i` feature flag](https://unix.stackexchange.com/questions/401905/bsd-sed-vs-gnu-sed-and-i), and [if you have GNU `sed` or BSD `sed`](https://riptutorial.com/sed/topic/9436/bsd-macos-sed-vs--gnu-sed-vs--the-posix-sed-specification).

`strs`, on the other hand, has a uniform interface and set of features across platforms, shells and operating systems, including Windows.

## String manipulation in the shell
`strs` provides string tools that are similar to [those that are built into Bash](https://tldp.org/LDP/abs/html/string-manipulation.html), and it provides commands for things that Bash doesn't have [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar) for, as well. 

The following examples of Bash code only work with Bash, whereas `strs` will work the same no matter if you're using Bash, [zsh](https://www.zsh.org/), PowerShell or something else.

Here are some ways you can manipulate strings with both Bash and `strs`:
```bash
string='This is an example.'


## String length
# Bash
$ echo "${#string}"
19

# str
$ str length "$string"
19

# or, using pipes
$ echo $string | str length
19


## Strip
$ removeFront='This'
$ removeEnd='example.'

# Bash
$ echo "${string#$removeFront}"  # from front
 is an example.

$ echo "${string%$removeEnd}"  # from end
This is an

# str
$ str lstrip $removeFront "$string"
 is an example.

$ str rstrip $removeEnd "$string" 
This is an

$ str strip $removeFront$removeEnd "$string" 
 is an

# or, using pipes
$ echo $string | str lstrip $removeFront
 is an example.

$ echo $string | str rstrip $removeEnd
This is an

$ echo $string | str strip $removeFront$removeEnd
 is an

 
## Capitalization
$ echo "${string^}"  # capitalize first char
This is an example.

$ echo "${string^^}"  # capitalize all
THIS IS AN EXAMPLE.

$ echo "${string,,}"  # lower all
this is an example.

# vs
$ str capitalize "$string"
This is an example.

$ str upper "$string"
THIS IS AN EXAMPLE.

$ str lower "$string"
this is an example.

# or
$ echo $string | str capitalize
This is an example.

$ echo $string | str upper
THIS IS AN EXAMPLE.

$ echo $string | str lower
this is an example.


## Replace
$ old='an'
$ new='a'

$ echo "${string//$old/$new}"  # replace all
This is a example.

echo "${string/$old/$new}"  # replace first
This is a example.

# vs
$ str replace $old $new "$string"
This is a example.

$ str replace $old $new "$string" --count 1
This is a example.

$ str replace-first $old $new "$string"
This is a example.

# or
$ echo $string | str replace $old $new
$ echo $string | str replace $old $new --count 1
$ echo $string | str replace-first $old $new
```

## String manipulation tools
There are some string manipulation commands that `strs` comes with that don't have syntactic sugar in Bash:
```bash
string='This is an example.'
width=40
countChar='e'
find='e'
on='_'
remove='.'
part=' '
split=' '
strip='.'


# casefold
$ str casefold "$string"
this is an example.

# or
$ echo $string | str casefold
this is an example.


# center
$ str center $width "$string"
          This is an example.           

$ echo $string | str center $width
          This is an example.           


# count
$ str count $countChar "$string"
2

$ echo $string | str count $countChar
2


# find
$ str find $find "$string"
11

$ echo $string | str find $find
11

# index
$ str index $find "$string"
11

$ echo $string | str index $find
11


# join
$ str join $on $string
This_is_an_example.

$ echo $string | str join $on
This_is_an_example.


# partition
$ str partition "$part" "$string"
This
 
is an example.

$ echo $string | str partition "$part"
This
 
is an example.


# split
$ str split "$split" "$string"
This
is
an
example.

$ echo $string | str split "$split"
This
is
an
example.


# strip
$ str strip $strip "$string"
This is an example

$ echo $string | str strip $strip
This is an example


# swap case
$ str swapcase "$string"
tHIS IS AN EXAMPLE.

$ echo $string | str swapcase
tHIS IS AN EXAMPLE.


# to title case
$ str title "$string"
This Is An Example.

$ echo $string | str title
This Is An Example.


# zero fill
$ str zfill $width "$string"
000000000000000000000This is an example.

$ echo $string | str zfill $width
000000000000000000000This is an example.


# repeat
$ str repeat 3 "$string"
This is an example.
This is an example.
This is an example.

$ echo $string | str repeat 3
This is an example.
This is an example.
This is an example.


# ljust
$ str ljust $width "$string" --fillchar '*'
This is an example.*********************

$ echo $string | str ljust $width  --fillchar '*'
This is an example.*********************


# lstrip
$ str lstrip T "$string"
his is an example.

$ echo $string | str lstrip T
his is an example. 


# rfind
$ str rfind $find "$string"
17

$ echo $string | str rfind $find
17


# rindex
$ str rindex $find "$string"
17

$ echo $string | str rindex $find
17


# rjust
$ str rjust $width "$string"
                     This is an example.

$ echo $string | str rjust $width
                     This is an example.


# rstrip
$ str rstrip $remove "$string"
This is an example

$ echo $string | str rstrip $remove
This is an example


# rpartition
$ str rpartition "$part" "$string"
This is an
 
example.

$ echo $string | str rpartition "$part"
This is an
 
example.


# rsplit
$ str rsplit $split "$string"
This
is
an
example.

$ echo $string | str rsplit $split
This
is
an
example.
```

## More string tools
`strs` comes with tools for dealing with UTF-8, ASCII and emojis, and it has tools that aren't found in Python or common shells like Bash.

```bash
$ str to-ascii "It is 20° Celsius outside."
It is 20deg Celsius outside.

$ str to-ascii "Ǎ Ě Ǐ Ǒ Ǔ Č Ď Ǧ Ȟ ǰ Ǩ Ľ Ň Ř Š Ť Ž"
A E I O U C D G H j K L N R S T Z

$ str substring 3 "Hey there! 🔥"
Hey

# you can use negative indices like you can in Python
$ str substring -3 "Hey there! 🔥" --start 4
there

# or you can use Python's slice syntax directly
$ str slice 4:-3 "Hey there! 🔥"
there

$ str contains 🔥 "Hey there! 🔥"; echo $?
0

$ str has-emoji "Hey there! 🔥"; echo $?
0

$ str from-emoji "Hey there! 🔥"
Hey there! :fire:

$ sudo dmesg | str nth 50
[73627.811739] Filesystems sync: 0.02 seconds

$ str sbob "squidward likes krabby patties"
sQuIdWaRd LiKeS kRaBbY pAtTiEs
```

## String validation tools
`strs` also brings [Python's string validation methods](https://docs.python.org/3/library/stdtypes.html#str) to the shell.

Here's an example of how you'd use them, followed by a list of validation tools that come with `strs`:
```bash
string='This is an example.'


if str startswith T "$string" && str endswith . "$string"; then
  printf "Starts with T and ends with .\n"

elif str contains example "$string"; then
  printf "Contains 'example'\n"

elif !str isalnum "$string"; then
  printf "Isn't alphanumeric\n"

fi


# starts with
$ str startswith T "$string"; echo $?
0

$ echo $string | str startswith T; echo $?
0

# ends with
$ str endswith . "$string"; echo $?
0

$ echo $string | str endswith .; echo $?
0

# is alphanumeric
$ str isalnum "$string"; echo $?
0

$ echo $string | str isalnum; echo $?
0

# is alphabetic
$ str isalpha "$string"; echo $?
1

$ echo $string | str isalpha; echo $?
1

# is ASCII
$ str isascii "$string"; echo $?
0

$ echo $string | str isascii; echo $?
0

# is decimal
$ str isdecimal "$string"; echo $?
1

$ echo $string | str isdecimal; echo $?
1

# is digit
$ str isdigit "$string"; echo $?
1

$ echo $string | str isdigit; echo $?
1

# is valid Python identifier
$ str isidentifier "$string"; echo $?
1

$ echo $string | str isidentifier; echo $?
1

# is lower case
$ str islower "$string"; echo $?
1

$ echo $string | str islower; echo $?
1

# # is numeric
$ str isnumeric "$string"; echo $?
1

$ echo $string | str isnumeric; echo $?
1

# is printable
$ str isprintable "$string"; echo $?
0

$ echo $string | str isprintable; echo $?
0

# is space character
$ str isspace "$string"; echo $?
1

$ echo $string | str isspace; echo $?
1

# is title case
$ str istitle "$string"; echo $?
1

$ echo $string | str istitle; echo $?
1

# is upper case
$ str isupper "$string"; echo $?
1

$ echo $string | str isupper; echo $?
1
```
