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
    conf_dir = pathlib.Path(__file__).parent.resolve()
    output_base = conf_dir / output_path if not pathlib.Path(output_path).is_absolute() else pathlib.Path(output_path)
    doxyfile_path = (conf_dir / "Doxyfile").resolve()

    potential_search_paths = [
        pathlib.Path(search_path),
        (conf_dir / search_path).resolve(),
        (conf_dir.parent.parent / "mercury_dev" / "src").resolve(),
    ]

    resolved_search_path = None
    for p in potential_search_paths:
        if p.exists() and list(p.rglob("**/riptide-docs.y[a]ml")):
            resolved_search_path = p
            break

    projects = {}

    if resolved_search_path is not None:
        packages = resolved_search_path.rglob("**/riptide-docs.y[a]ml")
        for path in packages:
            package_name = path.parent.name
            package_path = path.parent
            package_output = output_base / package_name

            projects[package_name] = str((package_output / "xml").resolve().absolute())

            # Delete Output Folder
            if package_output.exists():
                shutil.rmtree(package_output)

            # Create Empty Folder
            package_output.mkdir(parents=True)

            settings = []
            with path.open() as settings_file:
                settings = yaml.load(settings_file, Loader=yaml.FullLoader)

            sources = ""
            for source in settings.get("sources", []):
                sources += str((package_path / source).resolve().absolute()) + " "

            os.environ["DOXYGEN_PROJECT_NAME"] = package_name
            os.environ["DOXYGEN_INPUT"] = sources
            os.environ["DOXYGEN_ROOT"] = str(package_path.resolve().absolute())
            os.environ["DOXYGEN_OUTPUT"] = str(package_output.resolve().absolute())

            # Generate Doxygen XML
            subprocess.run(["doxygen", str(doxyfile_path)], check=True)

            # Clean up generated/keyword namespaces from Doxygen XML before breathe-apidoc
            index_xml_path = package_output / "xml" / "index.xml"
            if index_xml_path.exists():
                try:
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(index_xml_path)
                    root = tree.getroot()
                    CPP_KEYWORDS = {
                        "enum", "struct", "union", "class", "namespace", "template", "typename",
                        "const", "volatile", "static", "virtual", "explicit", "friend", "inline",
                        "mutable", "register", "auto", "bool", "char", "int", "float", "double",
                        "void", "short", "long", "signed", "unsigned", "true", "false", "default",
                        "case", "switch", "if", "else", "for", "do", "while", "break", "continue",
                        "goto", "return", "try", "catch", "throw", "new", "delete", "this", "operator"
                    }
                    for compound in list(root.findall("compound")):
                        cid = compound.get("refid", "")
                        cname = compound.findtext("name", "")
                        if compound.get("kind") == "namespace":
                            ns_file = package_output / "xml" / f"{cid}.xml"
                            is_generated = False
                            if ns_file.exists():
                                try:
                                    ns_tree = ET.parse(ns_file)
                                    loc = ns_tree.find(".//location")
                                    if loc is not None and loc.get("file") == "[generated]":
                                        is_generated = True
                                except Exception:
                                    pass
                            if cname in CPP_KEYWORDS or is_generated:
                                root.remove(compound)
                                if ns_file.exists():
                                    ns_file.unlink()
                    tree.write(index_xml_path)
                except Exception as e:
                    print(f"Warning cleaning xml: {e}")

            # Generate Sphinx Output
            subprocess.run([
                "breathe-apidoc",
                "-o", str(package_output.resolve().absolute()),
                "-p", str(package_name),
                "-m",
                "-g", "class,interface,struct,union,file,namespace,group",
                str((package_output / "xml").resolve().absolute())], check=True)

            template = jinja2.Template(PACKAGE_INDEX_TEMPLATE)

            with (package_output / "index.rst").open('w') as index_out:
                index_out.write(template.render(package_name=package_name))

    # Also register any existing packages in output_base that have an xml dir
    if output_base.exists():
        for pkg_dir in output_base.iterdir():
            if pkg_dir.is_dir() and (pkg_dir / "xml").exists():
                if pkg_dir.name not in projects:
                    projects[pkg_dir.name] = str((pkg_dir / "xml").resolve().absolute())

    return projects


breathe_projects = generate_breathe("../../src", "packages")