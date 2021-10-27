import re
from regexfactory import Amount, Range


pattern = Amount(Range("A", "Z"), 2, 3)

matches = re.findall(
    str(pattern),
    "My initials are BDP. Valorie's are VO"
)

print(matches)
