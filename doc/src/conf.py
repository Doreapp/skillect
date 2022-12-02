"""
Configuration of sphinx
"""

import datetime

extensions = [
    "sphinx_rtd_theme", # Read the docs theme
    "sphinxmermaid", # Enable mermaid graphs in doc
]
html_theme = "sphinx_rtd_theme"

# Project values
project = "Skillect"
copyright = f"{datetime.date.today().strftime('%Y')}, Antoine Mandin"
author = "Antoine Mandin"

# Link to Github repo
html_context = {
    "display_github": True,
    "github_user": "Doreapp",
    "github_repo": "skillect",
    "github_version": "main",
    "conf_py_path": "/doc/src/",
}

# Page title (in tab)
html_title = "Documentation"
