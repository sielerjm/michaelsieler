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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Michael Sieler'
copyright = '2023, Michael Sieler'
author = 'Michael Sieler'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #"sphinx_comments",
    #"sphinx_design",
    "sphinxcontrib.icon",
]

comments_config = {
    #"hypothesis": True
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Michael Sieler"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'sphinx_rtd_theme'
html_theme = "sphinx_book_theme"

html_theme_options = {
    "use_sidenotes": True,
    "logo_only": True,
    "show_toc_level": 2,
    "announcement": (
        "Now offering <b><a class='reference internal' href = 'https://michaelsieler.com/en/latest/Career/tutoring.html'>tutoring</a></b> and <b><a class='reference internal' href = 'https://michaelsieler.com/en/latest/Career/consulting.html'>consulting</a></b>." 
    ),

}



html_logo = 'Media/logo/MS_Logo_Clr-WhBG-200px.png'

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

# -- Favicon -----------------------------------------------------------------

html_favicon = 'favicon.ico'
