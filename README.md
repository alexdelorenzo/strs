# Easy string manipulation tools for the shell
 `strs` makes working with strings in the shell a better experience.

[String manipulation in POSIX-compliant shells](https://shellmagic.xyz/#string-manipulation) can be both confusing and cumbersome. `strs` brings string manipulation convenience methods from Python to shells like Bash.

```bash
export string='This is an example.'

# length
## Bash
echo ${#string}

## strs
strs length $string
# or
echo $string | strs length

# strip from rear
export remove='example.'
## Bash
echo ${string%remove}

## strs
strs rstrip $remove $string
echo $string | strs rstrip $remove


# strip from front
export remove='This'
## Bash
echo ${string#remove}

# vs
strs lstrip $remove $string
echo $string | strs lstrip $remove

## replace all
export replace='an'
export with='a'

echo ${string//replace/with}

# vs
strs replace $replace $with $string
echo $string | strs replace $replace $with

## replace first
echo ${string/replace/with}
# vs
strs replace $replace $with --count 1 $string
echo $string | strs replace $replace $with --count 1


```
