===============
Getting started
===============

::

    pip install relaton

Using data models
=================

Constructing items (in this case, from YAML):

::

    import yaml
    from relaton.models.bibdata import BibliographicItem

    with open('some_file.yaml', 'r', encoding='utf-8') as f:
        raw_data = f.read()
        data = yaml.loads(raw_data)
        item = BibliographicItem(**data)
        # Will throw if there are validation errors.

Using serializers
=================

::

    from relaton.serializers.abstract import create_abstract

    abstracts: List[GenericStringValue] = as_list(item.abstract or [])
    abstract = create_abstract(abstracts)
