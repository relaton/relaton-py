========
Glossary
========

.. glossary::

   bibliographic item
       Document metadata for purposes of referencing or citing.
       Corresponds to :class:`~relaton.models.bibdata.BibliographicItem` instance.

   citation
       Sometimes not quite correctly used as a synonym for :term:`bibliographic item`.

   resource identifier
   document identifier
   docid
       Identifier of a resource (a document, a registry, or otherwise).

       A resource can have multiple identifiers (e.g., a DOI, an ISBN, etc.),
       and sometimes a single identifier can be shared by multiple resources
       (however, such an ambiguous identifier
       should not be :term:`primary <primary resource identifier>`,
       that would be a data integrity issue).

       Identifiers are listed
       under :data:`BibliographicItem.docid <relaton.models.bibdata.BibliographicItem.docid>`,
       and each identifier is a :class:`relaton.models.bibdata.DocID` instance in Python.

   primary resource identifier
   primary document identifier
       Main characteristics of a primary identifier:

       - Identifier value (in Python, the :data:`~relaton.models.bibdata.DocID.id` attribute)
         can be used to unambiguously reference the document (resource).
       - A primary identifier is expected to be
         universally unique to this resource.

       Primary identifier uses format more or less similar to NIST’s PubID
       (possibly the only strongly standardized identifier format).
       It always starts with a prefix that denotes schema/document family.

       In Python, such identifiers have their :data:`~relaton.models.bibdata.DocID.primary`
       attribute set to ``True``.

   resource identifier type
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

   docid.id
       A string that is used to identify a resource
       within the domain (schema, namespace, etc.) designated by :term:`docid.type`.

       Contained in :data:`relaton.models.bibdata.DocID.id`.
