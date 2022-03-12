Introduction
***************

RegexFactory is a very very lightweight Python library that allows you to intuitively and dynamically generate regular expressions (RegEx).
Regular expressions are strings of text used to find and extract information from other strings and text documents.
See this quick example.

.. execute_code::
   :hide_headers:

   from regexfactory import Amount, Optional, Or, Range, Set

   pattern = Optional("#") + Or(
      Amount(Set(Range("0", "9"), Range("a", "f")), 6),
      Amount(Set(Range("0", "9"), Range("A", "F")), 6),
   )

   sentence = """
   My favorite color is #000000. I also like 5fb8a0. My second favorite color is #FF21FF.
   """

   matches = pattern.findall(sentence)

   print(pattern)  # Prints the generated pattern object as a string
   print(matches)  # Print the identified matches found in tbe sentence variable string.


You can see the clear components of the pattern. The optional "#" in the front. Then accept uppercase codes as well as lowercase codes, with characters between the hex alphabet of 0-9 and a-f. 
In your projects you can even apply logic to build conditional patterns that a script could generate based on API responses or something similar.

To understand what each of these classes does see the next pages of the documentation! :)




