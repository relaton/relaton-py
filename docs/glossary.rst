========
Glossary
========

.. glossary::

   bibliographic item
       Document metadata for purposes of referencing or citing.
       Corresponds to :class:`~relaton.models.bibdata.BibliographicItem` instance.

   citation
       Sometimes not quite correctly used as a synonym for :term:`bibliographic item`.

   docid
   document identifier
       Identifier of a document.

       A document can have multiple identifiers (e.g., a DOI, an ISBN, etc.),
       and sometimes a single identifier can be shared by multiple documents
       (however, such an ambiguous identifier
       should not be :term:`primary <primary document identifier>`,
       or it should be reported as a data integrity issue).

       Identifiers are listed
       under :data:`BibliographicItem.docid <relaton.models.bibdata.BibliographicItem.docid>`,
       and each identifier is a :class:`relaton.models.bibdata.DocID` instance in Python.

   primary document identifier
       Main characteristics of a primary identifier:

       - Its ``id`` can be used to unambiguously reference the document.
       - A primary identifier is expected to be
         universally unique to this document.

       This service displays primary identifiers without identifier types,
       as types tend to be self-explanatory.

       The :data:`~relaton.models.bibdata.DocID.id` value of a primary identifier
       uses format more or less similar to NIST’s PubID
       (possibly the only strongly standardized identifier format).
       It always starts with a prefix that denotes schema/document family.

       In Python, such identifiers have their :data:`~relaton.models.bibdata.DocID.primary`
       attribute set to ``True``.

   docid.id
       Refers to :data:`relaton.models.bibdata.DocID.id`.

   document identifier type
   docid.type
       The ``type`` component of :term:`document identifier`,
       contained in ``docid[*].type`` field of bibliographic item’s Relaton representation
       (field :data:`~relaton.models.bibdata.DocID.type` in Python).

       Document identifier type in Relaton is a somewhat murky concept.
       In case of a :term:`primary document identifier`, its type tends to be used
       to reference a namespace or registry
       (e.g., DOI, ISBN),
       and in other cases used to reference a publishing organization
       (e.g., IETF, IANA).

       Examples: ``IETF``, ``IEEE``, ``DOI``.
