===========
Development
===========

Setup
=====

Docker
------

You can use the provided Dockerfile for running tests
and static typing & linting hints via containerized LSP service.

Shortcut to run tests::

    make docker-tests

Running PyLSP server::

    docker build -t relaton-py-lsp . && \
    docker container run \
      --interactive --rm --network=none \
      --workdir="$(pwd)" --volume="$(pwd):$(pwd):z" \
      relaton-py-lsp

Virtual environment
-------------------

Create a virtual Python 3.10 environment
and ``pip install -r requirements_dev.txt -r requirements.txt`` within it.

Expanding Relaton model coverage
================================

- Consult Relaton specs (LutaML models, RNC grammar),
  and available Relaton YAML bibliographic data sources
  for the kinds of data we deal with.

  Any new information you want
  to add to bibliographic item model must already exist in the LutaML spec.

- For consistency, any fields and types you define must use field names
  that correspond to those defined in LutaML.

- If specifications conflict
  (e.g., LutaML and RNC define different types of a property, which sometimes happens),
  file a consolidation issue and confirm with maintainers
  which specification should take precedence.

Process
=======

- Update documentation, describing what’s being added
  and any potential backwards compatibility issues.
  Ideally, do this even before you change the codebase.
- Always run mypy (preferably, configure your IDE to run it automatically)
  to check types.
- You’re welcome to run flake8, though in cases where default flake8 configuration
  obviously differs from project conventions it’s recommended to stick to the latter.

Marking new release
===================

Pick the next version. Follow semantic versioning guidelines:
post-v1, increment major version in case of backwards-incompatible changes.

1. Update the ``__version__`` string in ``relaton/__init__.py``
   to your chosen version.
2. Ensure you updated the documentation,
   including describing the new version in :doc:`changelog`.
3. Tag new release in Git as the same version and push tags::

       git tag -s "v0.0.0" -m "Short message"
       git push --follow-tags

4. The repository is set up to build and publish to PyPI
   automatically on matching tag push.
