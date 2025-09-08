# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Riptide Docs'
copyright = '2025, Mason Erwine'
author = 'Mason Erwine'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.todo",
    "sphinxcontrib.katex",
    "breathe"
]

todo_include_todos = True

breathe_projects = {
    "riptide_slam": "../../riptide_release/src/riptide_slam/doxygen/xml"
}

breathe_default_project = "riptide_slam"

# breathe_default_members = ('members', 'protected-members', 'private-members', 'undoc-members')

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_theme_options = {
#     "style_nav_header_background": "white"
# }

html_logo="_static/logo.png"

html_static_path = ['_static']
