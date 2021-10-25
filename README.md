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