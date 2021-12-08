# 🧵 Easy string tools for the shell
 `strs` has more than 30 tools that make working with [strings](https://en.wikipedia.org/wiki/String_(computer_science)) in the [shell](https://linuxcommand.org/lc3_lts0010.php) easier. 

`strs` brings common string [convenience methods](https://wiki.c2.com/?ConvenienceMethods) to shells like [Bash](https://www.gnu.org/software/bash/), because [string manipulation](https://en.wikichip.org/wiki/string_manipulation) in shells can be [hard](https://shellmagic.xyz/#string-manipulation).

```bash
$ str capitalize "hey there! :fire:" | str to-emoji
Hey there! 🔥

$ str repeat 2 ⭐ | str join 🌙
⭐ 🌙 ⭐
```

# Usage
## Practical example
If you're on [Debian](https://www.debian.org/), you can use `strs` to take your [apt sources](https://wiki.debian.org/SourcesList) from Debian [`testing`](https://wiki.debian.org/DebianTesting), point them to Debian [`stable`](https://wiki.debian.org/DebianStable) on the fly, and then send them to a `stable` machine:
```bash
$ str replace testing stable < sources.list | ssh host "cat > /etc/apt/sources.list"
```

To do the same with [`sed`](https://en.wikipedia.org/wiki/Sed), you'd need to know [`sed`'s regex syntax](https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html), if your `sed` [comes with the `-i` feature flag](https://unix.stackexchange.com/questions/401905/bsd-sed-vs-gnu-sed-and-i), and [if it's GNU `sed` or BSD `sed`](https://riptutorial.com/sed/topic/9436/bsd-macos-sed-vs--gnu-sed-vs--the-posix-sed-specification).

`strs`, on the other hand, has a uniform interface and set of features across platforms, shells and operating systems, including Windows.

## String manipulation in the shell
`strs` has string tools that are similar to [those that are built into Bash](https://tldp.org/LDP/abs/html/string-manipulation.html), and it has commands for features that Bash doesn't have [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar) for, as well. 

The following examples of Bash code only work with Bash, whereas `strs` commands will work if you're using Bash, [zsh](https://www.zsh.org/), PowerShell or something else.

### String length
#### Bash
```bash
string='This is an example.'

$ echo "${#string}"
19
```

#### `strs`
```bash
$ str length "$string"
19
```

Or, using pipes:
```bash
$ echo $string | str length
19
```

### Strip
#### Bash
```bash
front='This'
end='example.'

$ echo "${string#$front}"  # from front
 is an example.

$ echo "${string%$end}"  # from end
This is an
```

##### `strs`
```bash
$ str lstrip $front "$string"
 is an example.

$ str rstrip $end "$string"
This is an

$ str strip $front$end "$string"
 is an
```

Or, using pipes:
```bash
$ echo $string | str lstrip $front
 is an example.

$ echo $string | str rstrip $end
This is an

$ echo $string | str strip $front$end
 is an
```

### Capitalization
#### Bash
```bash
$ echo "${string^}"  # capitalize first char
This is an example.

$ echo "${string^^}"  # capitalize all
THIS IS AN EXAMPLE.

$ echo "${string,,}"  # lower all
this is an example.
```

#### `strs`
```bash
$ str capitalize "$string"
This is an example.

$ str upper "$string"
THIS IS AN EXAMPLE.

$ str lower "$string"
this is an example.
```

Or:
```bash
$ echo $string | str capitalize
This is an example.

$ echo $string | str upper
THIS IS AN EXAMPLE.

$ echo $string | str lower
this is an example.
```

### Replace
#### Bash
```bash
old='an'
new='a'

$ echo "${string//$old/$new}"  # replace all
This is a example.

$ echo "${string/$old/$new}"  # replace first
This is a example.
```

#### `strs`
```bash
$ str replace $old $new "$string"
This is a example.

$ str replace $old $new "$string" --count 1
This is a example.

$ str replace-first $old $new "$string"
This is a example.
```

Or:
```bash
$ echo $string | str replace $old $new
$ echo $string | str replace $old $new --count 1
$ echo $string | str replace-first $old $new
```

## String manipulation tools
`strs` has string manipulation commands that don't have syntactic sugar in Bash.

### [Casefold](https://docs.python.org/3/library/stdtypes.html#str.casefold)
```bash
string='This is an example.'

$ str casefold "$string"
this is an example.
```

```bash
$ echo $string | str casefold
this is an example.
```

### Center
```bash
width=40

$ str center $width "$string"
          This is an example.           
```

```bash
$ echo $string | str center $width
          This is an example.           
```

### Count
```bash
countChar='e'

$ str count $countChar "$string"
2
```

```bash
$ echo $string | str count $countChar
2
```

### Find
```bash
find='e'

$ str find $find "$string"
11
```

```bash
$ echo $string | str find $find
11
```

### Index
```bash
$ str index $find "$string"
11
```

```bash
$ echo $string | str index $find
11
```

### Join
```bash
on='_'

$ str join $on $string
This_is_an_example.
```

```bash
$ str split ' ' "$string" | str join $on
This_is_an_example.
```

### Partition
```bash
part=' '

$ str partition "$part" "$string"
This

is an example.
```

```bash
$ echo $string | str partition "$part"
[...]
```

### Split
```bash
split=' '

$ str split "$split" "$string"
This
is
an
example.
```

```bash
$ echo $string | str split "$split"
[...]
```

### Strip
```bash
strip='.'

$ str strip $strip "$string"
This is an example
```

```bash
$ echo $string | str strip $strip
This is an example
```

### Swap case
```bash
$ str swapcase "$string"
tHIS IS AN EXAMPLE.
```

```bash
$ echo $string | str swapcase
tHIS IS AN EXAMPLE.
```

### To title case
```bash
$ str title "$string"
This Is An Example.
```

```bash
$ echo $string | str title
This Is An Example.
```

### Zero fill
```bash
$ str zfill $width "$string"
000000000000000000000This is an example.
```

```bash
$ echo $string | str zfill $width
000000000000000000000This is an example.
```

### Repeat
```bash
$ str repeat 3 "$string"
This is an example.
This is an example.
This is an example.
```

```bash
$ echo $string | str repeat 3
[...]
```

### Left justify
```bash
$ str ljust $width "$string" --fillchar '*'
This is an example.*********************
```

```bash
$ echo $string | str ljust $width --fillchar '*'
This is an example.*********************
```

### Left strip
```bash
$ str lstrip T "$string"
his is an example.
```

```bash
$ echo $string | str lstrip T
his is an example. 
```

### Right find
```bash
$ str rfind $find "$string"
17
```

```bash
$ echo $string | str rfind $find
17
```

### Right index
```bash
$ str rindex $find "$string"
17
```

```bash
$ echo $string | str rindex $find
17
```

### Right justify
```bash
$ str rjust $width "$string"
                     This is an example.
```

```bash
$ echo $string | str rjust $width
                     This is an example.
```

### Right strip
```bash
$ str rstrip $remove "$string"
This is an example
```

```bash
$ echo $string | str rstrip $remove
This is an example
```

### Right partition
```bash
$ str rpartition "$part" "$string"
This is an

example.
```

```bash
$ echo $string | str rpartition "$part"
[...]
```

### Right split
```bash
$ str rsplit "$split" "$string"
This
is
an
example.
```

```bash
$ echo $string | str rsplit "$split"
[...]
```

## More string tools
`strs` has tools that deal with UTF-8, ASCII and emojis, and it has tools that aren't found in Python or common shells.

### To ASCII
```bash
$ str to-ascii "It is 20° Celsius outside."
It is 20deg Celsius outside.
```

```bash
$ str to-ascii "Ǎ Ě Ǐ Ǒ Ǔ Č Ď Ǧ Ȟ ǰ Ǩ Ľ Ň Ř Š Ť Ž"
A E I O U C D G H j K L N R S T Z
```

### Substring
```bash
$ str substring 3 "Hey there! 🔥"
Hey
```

You can use negative indices like you can in Python:
```bash
$ str substring -3 "Hey there! 🔥" --start 4
there
```

### Slice
You can use Python's slice syntax directly, too.
```bash
$ str slice 4:-3 "Hey there! 🔥"
there
```

### Contains
```bash
$ str contains 🔥 "Hey there! 🔥"; echo $?
0
```

### Emojis
```bash
$ str has-emoji "Hey there! 🔥"; echo $?
0
```

```bash
$ str from-emoji "Hey there! 🔥"
Hey there! :fire:
```

### Get columns
```bash
$ str col 2 'hello world'
world
```

```bash
$ echo -e 'hello\tworld' | str col 2
world
```

### Return nth lines
```bash
$ sudo dmesg | str nth 50
[73627.811739] Filesystems sync: 0.02 seconds
```

### [tYpE lIkE tHiS](https://www.dailydot.com/unclick/mocking-spongebob-meme/)
```bash
$ str sbob "squidward likes krabby patties"
sQuIdWaRd LiKeS kRaBbY pAtTiEs
```

## String validation tools
`strs` also brings [Python's string validation methods](https://docs.python.org/3/library/stdtypes.html#str) to the shell.

Here's an example of how you'd use them in a [conditional statement](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html#Conditional-Constructs), followed by examples of other validation tools:
```bash
string='This is an example.'


if str startswith T "$string" && str endswith . "$string"; then
  printf "Starts with T and ends with .\n"

elif str contains example "$string"; then
  printf "Contains 'example'\n"

elif !str isalnum "$string"; then
  printf "Isn't alphanumeric\n"

fi
```

### Starts with
```bash
$ str startswith T "$string"; echo $?
0
```

```bash
$ echo $string | str startswith T; echo $?
0
```

### Ends with
```bash
$ str endswith . "$string"; echo $?
0
```

```bash
$ echo $string | str endswith .; echo $?
0
```

### Is alphanumeric
```bash
$ str isalnum "$string"; echo $?
0
```

```bash
$ echo $string | str isalnum; echo $?
0
```

### Is alphabetic
```bash
$ str isalpha "$string"; echo $?
1
```

```bash
$ echo $string | str isalpha; echo $?
1
```

### Is ASCII
```bash
$ str isascii "$string"; echo $?
0
```

```bash
$ echo $string | str isascii; echo $?
0
```

### Is decimal
```bash
$ str isdecimal "$string"; echo $?
1
```

```bash
$ echo $string | str isdecimal; echo $?
1
```

### Is digit
```bash
$ str isdigit "$string"; echo $?
1
```

```bash
$ echo $string | str isdigit; echo $?
1
```

### Is valid Python identifier
```bash
$ str isidentifier "$string"; echo $?
1
```

```bash
$ echo $string | str isidentifier; echo $?
1
```

### Is lower case
```bash
$ str islower "$string"; echo $?
1
```

```bash
$ echo $string | str islower; echo $?
1
```

### Is numeric
```bash
$ str isnumeric "$string"; echo $?
1
```

```bash
$ echo $string | str isnumeric; echo $?
1
```

### Is printable
```bash
$ str isprintable "$string"; echo $?
0
```

```bash
$ echo $string | str isprintable; echo $?
0
```

### Is space character
```bash
$ str isspace "$string"; echo $?
1
```

```bash
$ echo $string | str isspace; echo $?
1
```

### Is title case
```bash
$ str istitle "$string"; echo $?
1
```

```bash
$ echo $string | str istitle; echo $?
1
```

### Is upper case
```bash
$ str isupper "$string"; echo $?
1
```

```bash
$ echo $string | str isupper; echo $?
1
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
