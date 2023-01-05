=========
Changelog
=========


v0.2.24
=======

- Remove ``RFC Publisher`` organization from serialized output

v0.2.23
=======

- Upgrade GHA actions versions
- Remove dates from XML output for IANA entries
- Update docs

v0.2.22
=======

- Update Contributor model structure
- Update Role model structure
- Update Copyright.owner to accept either Organization(s) or Person(s)
- Minor fixes (including styling)

v0.2.21
=======

- XML serializer now outputs <format> for all bibliographic items instead of target attribute
- Fix: get fullname prefix from name and not name.given

v0.2.20
=======

Update models structure to reflect changes in source data format.

v0.2.19
=======

``bibxml_string`` serializer is removed.

v0.2.18
=======

Changed output format for ``IANA`` entries

v0.2.16
=======

``bibxml`` serializer now omits DOCTYPE again.

v0.2.15
=======

``bibxml`` serializer now formats RFC anchors appropriately.

v0.2.11
=======

``bibxml`` serializer now uses a consistent order of ``<seriesInfo>`` elements.

v0.2.10
=======

``bibxml_string`` serializer now attempts to return a canonicalized representation
with XML declaration and DOCTYPE.

v0.2.9
======

Adds ``BibitemLocality`` support.

v0.2.8
======

``bibxml`` serializer:

- Ensures returned ``anchor`` attribute satisfies XML schema
  (by replacing or dropping non-conforming characters).
- No longer formats Internet Draft anchors in a special way.

v0.2.7
======

The ``bibxml_string`` serializer now complies with own documentation
and pretty-prints the resulting XML string.

v0.2.6
======

The ``bibxml`` serializer will now prioritize PDF links
for ``<reference target>`` attribute value.

v0.2.5
======

The ``bibxml`` serializer:

- Fixed an issue where ``<reference>`` would be output instead of ``<referencegroup>``.
- Missing bibliographic item title no longer causes serializer to fail.
  However, it has to supply a default title, since the xml2rfc spec
  requires ``<title>`` to be provided.

v0.2.4
======

Fixed property definition order on ``contacts.Phone``.

v0.2.3
======

A default ``None`` for ``contacts.Phone.type`` is now supplied.

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
