===========
Development
===========

Setup
=====

Create a virtual Python environment
and ``pip install -r requirements_dev.txt`` within it.

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
