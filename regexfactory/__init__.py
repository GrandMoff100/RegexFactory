"""
API Reference
##############

The regexfactory module documentation!

.. automodule:: regexfactory.pattern

.. automodule:: regexfactory.patterns

.. automodule:: regexfactory.chars

"""

from .chars import ANY, ANCHOR_START, ANCHOR_END, WHITESPACE, NOTWHITESPACE, WORD, NOTWORD, DIGIT, NOTDIGIT
from .pattern import RegexPattern, escape, join
from .patterns import Or, Set, NotSet, Amount, Multi, Optional, Extension, NamedGroup, NamedReference, NumberedReference, Comment, IfAhead, IfNotAhead, IfBehind, IfNotBehind, Group, IfGroup


__version__ = "1.0.0"
