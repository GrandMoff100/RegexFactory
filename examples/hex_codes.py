import re

from regexfactory import Amount, Optional, Or, Range, Set

pattern = Optional("#") + Or(
    Amount(Set(Range("0", "9"), Range("a", "f")), 6),
    Amount(Set(Range("0", "9"), Range("A", "F")), 6),
)

sentence = """
My favorite color is #000000. I also like 5fb8a0. My second favorite color is #FF21FF.
"""

matches = re.findall(str(pattern), sentence)

print(pattern)  # Prints the generated pattern object as a string
print(matches)  # Print the identified matches found in tbe sentence variable string.
