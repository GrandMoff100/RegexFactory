from regexfactory import (
    Amount,
    Range,
    Optional,
    Group,
    RegexPattern,
    DIGIT,
    NotSet,
    WHITESPACE,
    WORD,
    Set
)
import re

protocol = Amount(Range("a", "z"), 1, or_more=True)
host = Amount(Set(WORD, DIGIT, '.'), 1, or_more=True)
port = Optional(Group(RegexPattern(":") + Amount(DIGIT, 1, or_more=True)))
path = Amount(Group(RegexPattern('/') + Group(Amount(NotSet('/', '#', '?', '&', WHITESPACE), 0, or_more=True))), 0, or_more=True)
patt = protocol + RegexPattern("://") + host + port + path


sentence = "This is a cool url, https://github.com/GrandMoff100/RegexFactory/ "

print(patt)
print(re.search(str(patt), sentence))
