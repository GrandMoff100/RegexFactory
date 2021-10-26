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
