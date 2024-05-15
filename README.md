# RegexFactory

Dynamically construct python regex patterns.

## Examples

### Matching Initials

Say you want a regex pattern to match the initials of someones name.

```python
from regexfactory import *

pattern = amount(Range("A", "Z"), 2, 3)

matches = pattern.findall("My initials are BDP. Valorie's are VO")

print(pattern.regex)
print(matches)
```

```
[A-Z]{2,3}
['BDP', 'VO']
```

### Matching Hex Strings

Or how matching both uppercase and lowercase hex strings in a sentence.

```python
from regexfactory import *

pattern = optional("#") + or_(
    (Range("0", "9") | Range("a", "f")) * 6,
    (Range("0", "9") | Range("A", "F")) * 6,
)

sentence = """
My favorite color is #000000. I also like 5fb8a0. My second favorite color is #FF21FF.
"""

print(pattern.regex)
matches = pattern.findall(sentence)
print(matches)
```

```
(?:#)?(?:[0-9a-f]{6}|[0-9A-F]{6})
['#000000', '5fb8a0', '#FF21FF']
```

### Matching URLs

Or what if you want to match urls in html content?

```python
from regexfactory import *

protocol = amount(Range("a", "z"), 1, or_more=True)
host = amount(WORD | DIGIT | r"\.", 1, or_more=True)
port = optional(":" + multi(DIGIT))
path = multi(
    "/" + multi(NotSet("/", "#", "?", "&", WHITESPACE), match_zero=True),
    match_zero=True,
)
patt = protocol + "://" + host + port + path


sentence = "This is a cool url, https://github.com/GrandMoff100/RegexFactory/ "
print(patt.regex)

print(patt.search(sentence))
```

```
[a-z]+://[\w\d\.]+(?::\d+)?(?:/[^/\#\?\&\s]*)*
<re.Match object; span=(20, 65), match='https://github.com/GrandMoff100/RegexFactory/'>
```

## The Pitch

This library is really good at allowing you to intuitively understand how to construct a regex expression.
It helps you identify what exactly your regular expression is, and can help you debug it.
This is library is also very helpful for generating regex expressions on the fly if you find uses for it.
You can also extend this library by subclassing `RegexPattern` and add your own support for different regex flavors.
Like generating regex expresison with Perl5 extensions.

There you have it. This library is intuitive, extensible, modular, and dynamic.
Why not use it?
