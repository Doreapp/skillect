"""
Configuration of sphinx
"""

import sphinx_rtd_theme

extensions = [
    'sphinx_rtd_theme',
]

html_context = {
    "display_github": True,
    "github_user": "Doreapp",
    "github_repo": "skillect",
    "github_version": "main",
    "conf_py_path": "/doc/src/",
}

html_theme = "sphinx_rtd_theme"
