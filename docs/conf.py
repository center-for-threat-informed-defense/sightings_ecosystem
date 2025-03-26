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
from slugify import slugify

# -- Project information -----------------------------------------------------

project = "Sightings Ecosystem"
slug = slugify(project)
googleanalytics_id = (
    "G-KWJLCFZG0V"  # find google analytics id from old analytics_id variable
)

author = "Center for Threat-Informed Defense"
copyright_years = "2024"
prs_numbers = "CT0103"

# The full version, including alpha/beta/rc tags
version = "v2.0.0"
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_wagtail_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

rst_prolog = f"""
.. |copyright_years| replace:: {copyright_years}
.. |prs_numbers| replace:: {prs_numbers}
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_wagtail_theme"
html_static_path = ["_static"]
html_extra_path = ["extra"]
html_favicon = "_static/favicon.ico"
html_logo = "_static/ctid_logo_white.png"
html_css_files = [
    "css/ctid.css",
    "css/sightings.css",
]
html_js_files = [
    "js/ctid.js",
]
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False
html_use_smartypants = False
html_context = {
    "copyright_years": copyright_years,
    "prs_numbers": prs_numbers,
}

footer_links = [
    ["Top ATT&CK Techniques", "https://ctid.mitre.org/projects/top-attack-techniques/"],
    ["ATT&CK Workbench", "https://ctid.mitre.org/projects/attck-workbench/"],
    ["CTI Blueprints", "https://ctid.mitre.org/projects/cti-blueprints/"],
]

html_theme_options = {
    "logo": "ctid_logo_white.png",
    "logo_alt": "The Center for Threat-Informed Defense",
    "logo_width": 250,
    "project_name": "Sightings Ecosystem",
    "footer_links": ",".join(
        [f"{link[0]}|{link[1]}?utm_source={slug}" for link in footer_links]
    ),
}
