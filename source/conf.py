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


breathe_default_members = ('members', 'protected-members', 'private-members', 'undoc-members')

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

import os
import glob
import pathlib
import shutil
import yaml
import subprocess
import jinja2

PACKAGE_INDEX_TEMPLATE = """
{{ package_name }}
==================

.. toctree::
    :maxdepth: 2
    :glob:

    *
"""

def generate_breathe(search_path, output_path):
    search_path = pathlib.Path(search_path)
    output_path = pathlib.Path(output_path)

    packages = search_path.rglob("**/riptide-docs.y[a]ml")
    projects = {}

    for path in packages:
        package_name = path.parent.name 
        package_path = path.parent
        package_output = output_path / package_name

        projects[package_name] = str(package_output / "xml")

        # Delete Output Folder
        if package_output.exists():
            shutil.rmtree(package_output)

        # Create Empty Folder
        package_output.mkdir(parents=True)

        settings = []
        with path.open() as settings_file:
            settings = yaml.load(settings_file, Loader=yaml.FullLoader)

        sources = ""
        for source in settings["sources"]:
            sources += str((package_path / source).resolve().absolute()) + " "

        os.environ["DOXYGEN_PROJECT_NAME"] = package_name
        os.environ["DOXYGEN_INPUT"] = sources
        os.environ["DOXYGEN_ROOT"] = str(package_path.resolve().absolute())
        os.environ["DOXYGEN_OUTPUT"] = str(package_output)

        # Generate Doxygen XML
        subprocess.run(["doxygen", "Doxyfile"])

        # Generate Sphinx Output
        subprocess.run([
            "breathe-apidoc",
            "-o", str(package_output.absolute()),
            "-p", str(package_name),
            "-m",
            "-g", "class,interface,struct,union,file,namespace,group",
            str((package_output / "xml").absolute())])

        template = jinja2.Template(PACKAGE_INDEX_TEMPLATE)
        
        with (package_output / "index.rst").open('w') as index_out:
            index_out.write(template.render(package_name=package_name))

    return projects


breathe_projects = generate_breathe("../../src", "packages")