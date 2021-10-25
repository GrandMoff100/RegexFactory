# RegexFactory

Dynamically construct python regex patterns.

## Examples

### Matching Initials
Say you want a regex pattern to match the initials of someones name.

```python
import re
from regexfactory import Amount, Range


pattern = Amount(Range("A", "Z"), 2, 3)

matches = re.findall(
    str(pattern),
    "My initials are BDP. Valorie's are VO"
)

print(matches)
```

```
['BDP', 'VO']
```

### Matching Hex Strings

Or how matching both uppercase and lowercase hex strings in a sentence.

```python
import re
from regexfactory import *

pattern = Optional("#") + Or(
    Amount(
        Set(
            Range("0", "9"),
            Range("a", "f")
        ),
        6
    ),
    Amount(
        Set(
            Range("0", "9"),
            Range("A", "F")
        ),
        6
    ),
    
)

sentence = """
My favorite color is #000000. I also like 5fb8a0. My second favorite color is #FF21FF.
"""

matches = re.findall(
    str(pattern),
    sentence
)
print(matches)
```

```
['#000000', '5fb8a0', '#FF21FF']
```

### Matching URLs

Or what if you want to match urls in html content?

```python
from regexfactory import *
import re


protocol = Amount(Range("a", "z"), 1, ormore=True)
host = Amount(Set(WORD, DIGIT, '.'), 1, ormore=True)
port = Optional(Group(RegexPattern(":") + Amount(DIGIT, 1, ormore=True)))
path = Amount(Group(RegexPattern('/') + Group(Amount(NotSet('/', '#', '?', '&', WHITESPACE), 0, ormore=True))), 0, ormore=True)
patt = protocol + RegexPattern("://") + host + port + path



sentence = "This is a cool url, https://github.com/GrandMoff100/RegexFactory/ "
print(patt)

print(re.search(str(patt), sentence))
```

```
[a-z]{1,}://[\w\d.]{1,}(:\d{1,})?(/([^/#?&\s]{0,})){0,}
<re.Match object; span=(15, 51), match='https://github.com/GrandMoff100/RegexFactory/'>
```

## The Pitch

This library is really good at allowing you to intuitively understand how to construct a regex expression.
It helps you identify what exactly your regular expression is, and can help you debug it.
This is library is also very helpful for generating regex expressions on the fly if you find use for it.
You can also extend this library by subclassing `RegexPattern` and add your own support for different regex flavors.

There you have it. This library is intuitive, extensible, modular, and dynamic.
Why not use it?