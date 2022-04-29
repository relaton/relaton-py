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

    from relaton.serializers.bibxml_string import serialize

    with open('some_file.xml', 'w', encoding='utf-8') as f:
        data = serialize(item)
        f.write(data)
