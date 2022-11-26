# Documentation

This folder stores the documentation for developers and curious ones.

It uses python package [`sphinx`](https://www.sphinx-doc.org) with the theme of read-the-docs [`sphinx-rtd-theme`](https://sphinx-rtd-theme.readthedocs.io/).

## Development

Source code is under [`src/`](src/) directory.

During development, it is recommended to use `docker`. For native development see [Native Development](#native-development).

* Build the HTML files using `make docker_html`. Files are generated under [`html`](html/).
* Optionally serve the generated files with a local server using `make docker_serve` and open [`localhost:8000`](http://localhost:8000/) to preview the documentation.

### Native development

1. (Optional but recommended) Create a virtual environment: `virtualenv venv && source venv/bin/activate`
2. Install the dependencies: `pip install -r requirements.txt`
3. Build the HTML files: `make html`
4. (Optional) Serve the html files: `make serve`. \
    And open [`localhost:8000`](http://localhost:8000/).

### Helpful documentation

Sphinx documentation supports reStructuredText format. Here are some helper about the format:
- [📖 Official reStructuredText documentation] https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
- [📃 A cheatsheet about rst syntax]
