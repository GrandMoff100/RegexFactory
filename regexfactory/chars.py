r"""
Regex Characters
*******************

Common regex special characters, such as :code:`\d`, :code:`.`, ...
More information about special characters in python regex available
`here <https://docs.python.org/3/library/re.html#regular-expression-syntax>`__
"""

from .patterns import RegexPattern

#: (Dot.) In the default mode, this matches any character except a newline. If the :data:`re.DOTALL` flag has been specified, this matches any character including a newline.
ANY = RegexPattern(r".")

#: (Caret.) Matches the start of the string, and in  :data:`re.MULTILINE` mode also matches immediately after each newline.
ANCHOR_START = RegexPattern(r"^")

#: Matches the end of the string or just before the newline at the end of the string, and in :data:`re.MULTILINE` mode also matches before a newline. foo matches both :code:`foo` and :code:`foobar`, while the regular expression :code:`foo$` matches only :code:`foo`. More interestingly, searching for :code:`foo.$` in :code:`foo1\nfoo2\n` matches :code:`foo2` normally, but :code:`foo1` in  :data:`re.MULTILINE` mode; searching for a single $ in :code:`foo\n` will find two (empty) matches: one just before the newline, and one at the end of the string.
ANCHOR_END = RegexPattern(r"$")

#: Matches Unicode whitespace characters (which includes :code:`[ \t\n\r\f\v]`, and also many other characters, for example the non-breaking spaces mandated by typography rules in many languages). If the :data:`re.ASCII` flag is used, only :code:`[ \t\n\r\f\v]` is matched.
WHITESPACE = RegexPattern(r"\s")

#: Matches any character which is not a whitespace character. This is the opposite of \s. If the :data:`re.ASCII` flag is used this becomes the equivalent of :code:`[^ \t\n\r\f\v]`.
NOTWHITESPACE = RegexPattern(r"\S")

#: Matches Unicode word characters; this includes most characters that can be part of a word in any language, as well as numbers and the underscore. If the :data:`re.ASCII` flag is used, only :code:`[a-zA-Z0-9_]` is matched.
WORD = RegexPattern(r"\w")

#: Matches any character which is not a word character. This is the opposite of \w. If the :data:`re.ASCII` flag is used this becomes the equivalent of :code:`[^a-zA-Z0-9_]`. If the  :data:`re.LOCALE` flag is used, matches characters which are neither alphanumeric in the current locale nor the underscore.
NOTWORD = RegexPattern(r"\W")

#: Matches any Unicode decimal digit (that is, any character in Unicode character category [Nd]). This includes :code:`[0-9]`, and also many other digit characters. If the :data:`re.ASCII` flag is used only :code:`[0-9]` is matched.
DIGIT = RegexPattern(r"\d")

#: Matches any character which is not a decimal digit. This is the opposite of \d. If the :data:`re.ASCII` flag is used this becomes the equivalent of :code:`[^0-9]`.
NOTDIGIT = RegexPattern(r"\D")
