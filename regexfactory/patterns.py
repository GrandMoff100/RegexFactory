"""The module for Regex pattern classes like these regex patterns, :code:`[^abc]`, :code:`(abc)`, or :code:`a|b`"""

from .pattern import RegexPattern
from typing import Tuple, Union


class Group(RegexPattern):
    """
    A group is a way of splitting a single large pattern up into smaller components.
    A capturing group is for extracting useful information from a specific part of the pattern matches.
    If you want to make a non-capturing group, pass :code:`noncapturing=True` to the init of a group object like, :code:`Group(mypattern, noncapuring=True)`  
    """

    def __init__(self, pattern: Union[str, RegexPattern], noncapturing=False):
        extension = ""
        if noncapturing:
            extension += '?:'
        super().__init__("(" + extension + str(pattern) + ")")


class Or(RegexPattern):
    """
    
    """

    def __init__(
        self,
        pattern: Union[str, RegexPattern],
        other_pattern: Union[str, RegexPattern]
    ):
        regex = Group(pattern, noncapturing=True) + RegexPattern("|") + Group(other_pattern, noncapturing=True)
        super().__init__(Group(regex, noncapturing=True))


class Range(RegexPattern):
    """
    
    """

    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        regex = f"[{start}-{end}]"
        super().__init__(regex)


class Set(RegexPattern):
    """
    
    """

    def __init__(self, *patterns: Tuple[Union[str, Range]]):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.end}"
            else:
                regex += str(p)
        super().__init__(f"[{regex}]")


class NotSet(RegexPattern):
    """
    
    """

    def __init__(self, *patterns: Tuple[Union[str, Range]]):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.end}"
            else:
                regex += str(p)
        super().__init__(f"[^{regex}]")


class Amount(RegexPattern):
    """
    
    """

    def __init__(
        self,
        pattern: Union[str, RegexPattern],
        i: int,
        j: int = None,
        ormore: bool = False,
        greedy=True,
    ):
        if j is not None:
            amount = f"{i},{j}"
        elif ormore:
            amount = f"{i},"
        else:
            amount = f"{i}"
        if not greedy:
            greedy = "?"
        else:
            greedy = ""
        super().__init__(pattern + "{" + amount + "}" + greedy)


class Optional(RegexPattern):
    """
    
    """

    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__(pattern + "?")


class Extension(RegexPattern):
    def __init__(self, pre: str, pattern: Union[str, RegexPattern]):
        super().__init__(f"(?{pre}{str(pattern)})")


class NamedGroup(Extension):
    """
    
    """

    def __init__(self, name: str, pattern: Union[str, RegexPattern]):
        super().__init__("P<{name}>", pattern)


class Comment(Extension):
    def __init__(self, content: str):
        super().__init__("#", content)


class Lookahead(Extension):
    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__("=", pattern)


class NegLookahead(Extension):
    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__('!', pattern)

