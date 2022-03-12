# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys

sys.path.insert(0, os.path.abspath("../"))
sys.path.append(os.path.abspath("extensions"))

from regexfactory import __version__

# -- Project information -----------------------------------------------------
project = "RegexFactory"
copyright = "2021, Nate Larsen"
author = "Nate Larsen"

# The full version, including alpha/beta/rc tags
release = __version__
branch = (
    "master"
    if __version__.endswith("a")
    or __version__.endswith("b")
    or __version__.endswith("rc")
    else "v" + __version__
)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = ["sphinx.ext.autodoc", "sphinx_execute_code", "sphinx.ext.intersphinx"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {"members": None, "annotation": None}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

html_favicon = "./images/favicon.png"

autodoc_default_options = {
    "members": None,
    "exclude-members": "regex, Extension",
    "undoc-members": True,
    "member-order": "bysource",
    "special-members": "__add__, __mul__",
}

autodoc_type_aliases = {"ValidPatternType": "regexfactory.pattern.ValidPatternType"}

intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3",
        None,
    ),
}
