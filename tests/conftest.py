from hypothesis import Verbosity, settings

from regexfactory import pattern

# Set default profile to use 500 examples
settings.register_profile("default", max_examples=500, verbosity=Verbosity.normal)

pattern._enable_desc = True
