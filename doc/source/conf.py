# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

from sphinx_pyproject import SphinxConfig

# workaround for https://github.com/sphinx-doc/sphinx/issues/13231
os.environ.pop("SOURCE_DATE_EPOCH", None)

sys.path.insert(0, os.path.abspath(os.path.join(*["..", "..", "src"])))

config = SphinxConfig(os.path.join(*["..", "..", "pyproject.toml"]), globalns=globals())

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project
copyright
author
version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions
templates_path
exclude_patterns

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme
html_theme_options
html_static_path
