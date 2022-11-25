"""
Configuration of sphinx
"""

import sphinx_rtd_theme
import datetime

# Use Read the docs theme
extensions = [
    'sphinx_rtd_theme',
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
