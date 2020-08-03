# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import re
from time import time
import pdb
from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx.directives import directives
#from mock import MagicMock
sys.path.insert(0, os.path.abspath('../'))
# sys.path.insert(0, os.path.abspath('../..'))

# for localext

# if 'PYTHONPATH' not in os.environ.keys():
#     os.environ['PYTHONPATH'] =  os.path.abspath('../')
# else:
#     os.environ['PYTHONPATH'] += ':'+os.path.abspath('../')

sys.setrecursionlimit(1500)
sys.path.insert(0, os.path.abspath('./'))
from local_directives import RoadmapDirective, RoadmapNode

#import sphinx_bootstrap_theme
#import guzzle_sphinx_theme
# import contextlib
# import os
# import sys
# from types import FunctionType, MethodType, ModuleType

from sphinx.util import logging


# -- Project information -----------------------------------------------------

project = u'Autopilot'
copyright = u'2019, Jonny Saunders'
author = u'Jonny Saunders'

# The short X.Y version
version = u'0.3'
# The full version, including alpha/beta/rc tags
release = u'0.3.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

try_theme = "rtd"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.graphviz',
    'sphinx.ext.autosummary',
    #'sphinx_automodapi.automodapi',
    'autodocsumm',   # https://github.com/Chilipp/autodocsumm
    #'sphinxcontrib.fulltoc',
    #'localext.fulltoc'
    'sphinx_sass',
    'local_directives'
]

if try_theme == 'rtd':
    extensions.append('sphinx_rtd_theme')

# Napoleon settings
# see http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True

autoclass_content = "both"
autodoc_member_order = "bysource"
#autodoc_default_flags = ['members']
#autodoc_mock_imports = ['tables', 'PySide', 'pyo', 'jack', 'pyqtgraph']
autodata_content = "both"

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    # 'exclude-members': '__doc__',
    'undoc-members': False,
    'show-inheritance': True,
    'autosummary': True
}

# testing something from sklearn
add_module_names = False

#automodsumm_writereprocessed = True
# numpydoc_show_class_members = False
# automodsumm_inherited_members = False
# automodsumm_writereprocessed = False
# automodapi_toctreedirnm = 'api'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

autosummary_generate = True

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'sphinx_rtd_theme'
html_style = 'css/autopilot_theme.css'
html_logo = 'autopilot_logo.svg'
# elif try_theme == 'bootstrap':
#     html_theme = 'bootstrap'
#     html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
# else:
#     html_theme = 'bootstrap'
#     html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

#html_theme = "basicstrap"
#
# html_theme = "sphinx_rtd_theme"
# html_theme_path = ["_themes", ]
#



# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
if html_theme == 'sphinx_rtd_theme':
    html_theme_options = {
        'canonical_url': 'rpilot.readthedocs.io',
        'collapse_navigation': False # keep expanding toc
    }

elif html_theme == 'bootstrap':
    html_theme_options = {
        'navbar_title': "Autopilot",
        'navbar_site_name': 'Autopilot Docs',
        'globaltoc_depth': 3,
        'navbar_class': "navbar navbar-inverse",
        'bootswatch_theme': "readable",
        'navbar_pagenav': True,

    }


#
# html_sidebars = {
#     '**': ['localtoc.html', 'relations.html']
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# configure sass compilation
sass_configs = [
    {'entry':'styles/main.scss',
     'output': '_static/css/autopilot_sass.css'}
]

# relative to html_static_path
html_css_files = [
    'css/autopilot_sass.css',
    'css/autopilot_theme.css'
]

html_baseurl = 'http://rpilot.readthedocs.io/'

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'autopilotdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': '',

    # Latex figure (float) alignment
    #
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'autopilot.tex', u'Autopilot Documentation',
     u'Jonny Saunders', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'autopilot', u'autopilot Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'autopilot', u'autopilot Documentation',
     author, 'autopilot', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'PySide2': ('https://doc.qt.io/qtforpython/PySide2/', None),
                       'tables': ('https://pytables.readthedocs.io/en/latest/', None),
                       'pandas': ('http://pandas.pydata.org/pandas-docs/stable/', None),
                       'zmq': ('https://pyzmq.readthedocs.io/en/latest/', None),
                       'tornado': ('https://www.tornadoweb.org/en/stable/', None),
                       'pyqtgraph': ('https://pyqtgraph.readthedocs.io/en/latest/', None),
                       'numpy': ('https://numpy.readthedocs.io/en/latest/', None),
                       'npyscreen': ('https://npyscreen.readthedocs.io/', None),
                       'jack': ('https://jackclient-python.readthedocs.io/en/0.4.5/', None),
                       'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

primary_domain = "py"

highlight_language = "py"

def fix_html_links(app, exception):
    print('fixing html links...')
    start = time()
    base_dir = os.getcwd()
    # walk directories, prepending '/' to all links in html files
    for root, dirs, files in os.walk(base_dir):
        #pdb.set_trace()
        html_files = [f for f in files if f.endswith('.html')]
        for hf in html_files:
            fullfile = os.path.join(root, hf)
            with open(fullfile) as hfile:
                txt = hfile.read()
            # prepend / to links, we have a few flavors...
            # js <script> imports use src
            txt = re.sub(r'(<script type="text/javascript".{0,100}src=")', r'\1/', txt)
            # stylesheets
            txt = re.sub(r'(<link rel="stylesheet" href=")', r'\1/', txt)
            # general links
            txt = re.sub(r'(<link rel=.{0,50}title=.{0,50}href=")(?!http)', r'\1/', txt)
            # and finally and <a> links that aren't # links on that page or ../ links
            txt = re.sub(r'(<a.*href=")(?!#)(?!\.+/)', r'\1/', txt)

            with open(fullfile, 'w') as hfile:
                hfile.write(txt)
    finish = time()
    print('finished fixing html in {} seconds'.format(finish-start))



def test_grouper(app, what, name, obj, section, parent):
    pdb.set_trace()

def css_class_role(name, rawtext, text, lineno, inliner, options={}, content={}):
    pdb.set_trace()
#
# class RoadmapNode(nodes.Element):
#     pass
#
# class RoadmapDirective(Directive):
#     """
#     http://www.xavierdupre.fr/blog/2015-06-07_nojs.html
#
#     """
#
#     # defines the parameter the directive expects
#     # directives.unchanged means you get the raw value from RST
#     required_arguments = 0
#     optional_arguments = 0
#     final_argument_whitespace = True
#     option_spec = {'conversation': directives.unchanged}
#     has_content = False
#     # add_index =
#
#     # def run(self):
#     #     super(RoadmapDirective, self).run()
#     #     s
#
#     def run(self):
#
#         # sett = self.state.document.settings
#         # language_code = sett.language_code
#         # env = self.state.document.settings.env
#
#         # gives you access to the parameter stored
#         # in the main configuration file (conf.py)
#         # config = env.config
#
#         # gives you access to the options of the directive
#         # options = self.options
#
#         # we create a section
#         # idb = nodes.make_id("todo-" + options["conversation"])
#         # section = nodes.section(ids=[idb])
#
#         # we create a title and we add it to section
#         # section += nodes.title(options["title"])
#
#         # we create the content of the blog post
#         # because it contains any kind of RST
#         # we parse parse it with function nested_parse
#         # par = nodes.paragraph()
#         # self.state.nested_parse(content, self.content_offset, par)
#
#         # we create a blogpost and we add the section
#         # node = self.__class__.roadmap_class()
#         # node += section
#         # node += par
#
#         # we return the result
#         section = nodes.section(ids=nodes.make_id('the-html-anchor'))
#         section += nodes.title('Text', 'Text')  # Just add the text twice
#         # section += nodes.any_other_element_that_can_be_in_a_section()
#         sections = [section]
#         return sections
#



def setup(app):
    # if try_theme == 'bootstrap':
    app.add_css_file("restyle.css")

    # app.add_node(RoadmapNode, html=(visit_roadmap_node, depart_roadmap_node))
    # app.add_directive('roadmap', RoadmapDirective)
    # app.add_directive('uml', UMLGenerateDirective)
    # app.add_role('cssclass', css_class_role)
    # app.add_node(RoadmapNode, html=(visit_roadmap_node, depart_roadmap_node))
    # app.add_directive('roadmap', RoadmapDirective)

    from autopilot import prefs

    prefs.add('AUDIOSERVER', 'docs')
    prefs.add('AGENT', 'docs')

    #app.connect('build-finished', fix_html_links)