=========
Changelog
=========

v0.2.2
======

Fix misplaced ``Person.contact`` property definition.

v0.2.1
======

Fixed an error caused by messed-up order in contact method type definition.

v0.2.0
======

Breaking.

Updates contact method types to conform to spec:

- ``Contact`` becomes ``Address``
- ``ContactMethod``, ``Phone`` are added

v0.1.18
=======

Fixes a possible crash of ``bibxml`` serializer
on some 3GPP documents.

v0.1.17
=======

Updates regarding the ``bibxml`` serializer:

- When deciding whether to output ``<referencegroup>``
  as root element, rely on presence of “includes”-type relations
  alone, rather than also require absence of titles.
- Fix an issue with serializing Internet Drafts to XML

v0.1.16
=======

- Allow multiple ``BibliographicItem.version`` entries

v0.1.15
=======

- Make ``BibliographicItem.docid`` a list (and required property)

v0.1.14
=======

- Corrected a problem with abstract conversion (``bibxml`` serializer)

v0.1.11
=======

- Fixed CodeCov badge syntax in README/PyPI description.

v0.1.10
=======

- ``bibxml`` serializer now takes abstract’s ``format`` into account.
  For abstracts with ``application/x-jats-xml`` format
  (typically, coming from Crossref DOI data),
  paragraphs are now extracted as ``<t>`` sub-elements.

v0.1.9
======

- Added ``prefix`` and ``addition`` fields to ``PersonName`` model.
- ``bibxml`` serializer now attempts to fill in ``fullname`` attribute
  on an ``<author>`` even if ``PersonName.completename`` is absent
  (formatting a string using whatever parts of the name *are* available).

Anchors and identifier scope
----------------------------

- This starts a switch to ``anchor`` attribute values formatted
  based on primary identifiers,
  rather than using identifiers with ``scope`` property set to ``anchor``
  (which will be phased out).

  So far this is only implemented for Internet Drafts
  (see ``serializers.bibxml.anchor.format_internet_draft_anchor()``,
  which ``get_suitable_anchor()`` now delegates to
  if a ``docid`` with ``type`` matching “internet-draft” is detected
  on the item.

v0.1.8
======

- Added ``BibliographicItem.version`` field and the corresponding ``VersionInfo`` class.
  It follows LutaML models
  in that ``draft`` is expected to be either a string or not defined,
  not an array of strings like the RNC grammar suggests. This may be subject to change.

v0.1.7
======

- Fixed re-imports.

v0.1.6
======

- Added re-imports for models classes in ``relaton.models``
  for convenience.
- Added changelog.
