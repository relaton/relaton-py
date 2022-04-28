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
from typing import List

sys.path.insert(0, os.path.abspath('..'))

import relaton


# -- Project information -----------------------------------------------------

project = 'Relaton Python'
copyright = '2022'
author = 'Ribose'

release = f"v{relaton.__version__}"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# sys.path.append(os.path.abspath("./_ext"))
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.linkcode',
    'sphinx.ext.todo',
]

todo_include_todos = True

viewcode_follow_imported_members = True

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []

extlinks = {
    'issue': (
        'https://github.com/relaton/relaton-py/issues/%s',
        'GitHub issue #%s',
    ),
    'github': (
        'https://github.com/relaton/relaton-py/blob/main/%s',
        '%s on GitHub',
    ),
}

html_css_files = [
    'custom-haiku.css',
]
html_js_files = [
]

autodoc_member_order = 'bysource'

autodoc_class_signature = 'separated'


primary_domain = 'py'


intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    # 'django': ('https://docs.djangoproject.com/en/stable', 'https://docs.djangoproject.com/en/stable/_objects/'),
    # 'simplejson': ('https://simplejson.readthedocs.io/en/stable/', 'https://simplejson.readthedocs.io/en/stable/objects.inv'),
    # 'requests': ('https://docs.python-requests.org/en/stable/', 'https://docs.python-requests.org/en/stable/objects.inv'),
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'haiku'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
