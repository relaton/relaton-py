import os
from copy import copy
from io import StringIO
from typing import List
from unittest import TestCase

import yaml
from lxml import etree

from relaton.models import (
    BibliographicItem,
    Contributor,
    DocID,
    Link,
    GenericStringValue,
)
from relaton.models.bibitemlocality import LocalityStack, Locality
from relaton.serializers.bibxml import (
    create_reference,
    get_suitable_anchor,
    get_suitable_target,
    serialize,
)
from relaton.serializers.bibxml.abstracts import (
    create_abstract,
    get_paragraphs,
    get_paragraphs_html,
    get_paragraphs_jats,
)
from relaton.serializers.bibxml.authors import create_author
from relaton.serializers.bibxml.reference import build_refcontent_string
from relaton.serializers.bibxml.series import (
    extract_doi_series,
    extract_rfc_series,
    extract_id_series,
    extract_w3c_series,
    extract_3gpp_tr_series,
    extract_ieee_series,
)


class SerializerTestCase(TestCase):
    def setUp(self):
        # Data for a Contributor (AKA Author) of type Organization
        contributor_organization_data = {
            "organization": {
                "name": "Internet Engineering Task Force",
            },
            "role": "publisher",
        }
        self.contributor_organization = Contributor(**contributor_organization_data)

        # Data for a Contributor (AKA Author) of type Person
        self.contributor_person_data = {
            "person": {
                "name": {
                    "initial": [{"content": "Mr", "language": "en"}],
                    "surname": {"content": "Cerf", "language": "en"},
                    "completename": {"content": "Mr Cerf", "language": "en"},
                },
            },
            "role": "author",
        }
        self.contributor_person = Contributor(**self.contributor_person_data)

        # Data for a BibliographicItem which will be converted
        # to a <reference> root tag in the XML output
        self.bibitem_reference_data = {
            "id": "ref_01",
            "title": [
                {
                    "content": "title",
                    "language": "en",
                    "script": "Latn",
                    "format": "text / plain",
                }
            ],
            "docid": [
                {"id": "ref_01", "scope": "anchor", "type": "type"},
                {"id": "IEEE P2740/D-6.5 2020-08", "type": "IEEE"},
            ],
            "contributor": [self.contributor_person_data],
            "date": [{"type": "published", "value": "1996-02"}],
            "abstract": [{"content": "abstract_content"}],
            "series": [{"title": ["IEEE P2740/D-6.5 2020-08"], "type": "IEEE"}],
            "version": [{"draft": True}],
            "extent": {"locality": [
                {"type": "container-title", "reference_from": "Container Title"},
                {"type": "volume", "reference_from": "1"},
                {"type": "issue", "reference_from": "2"},
                {"type": "page", "reference_from": "3"}
            ]}
        }
        self.bibitem_reference = BibliographicItem(**self.bibitem_reference_data)

        # Data for a BibliographicItem which will be converted
        # to a <referencegroup> root tag in the XML output
        self.bibitem_referencegroup_data = {
            "id": "ref_02",
            "docid": [{"id": "ref_02", "type": "test_dataset_02"}],
            "relation": [
                {
                    "type": "includes",
                    "bibitem": {
                        "id": "test_id",
                        "title": [
                            {
                                "content": "title",
                                "language": "en",
                                "script": "Latn",
                                "format": "text / plain",
                            }
                        ],
                        "contributor": [
                            contributor_organization_data,
                            self.contributor_person_data,
                        ],
                        "link": [
                            {
                                "content": "https://raw.githubusercontent.com/relaton/relaton-data-ietf/master/data"
                                "/reference.RFC"
                                ".1918.xml",
                                "type": "xml",
                            }
                        ],
                        "type": "standard",
                        "docid": [{"id": "RFC1918", "type": "RFC"}],
                        "docnumber": "RFC1918",
                        "date": [{"type": "published", "value": "1998-02"}],
                        "extent": {"locality": [
                            {"type": "container-title", "reference_from": "Container Title"},
                            {"type": "volume", "reference_from": "1"},
                            {"type": "issue", "reference_from": "2"},
                            {"type": "page", "reference_from": "3"}
                        ]}
                    },
                }
            ],
        }
        self.bibitem_referencegroup = BibliographicItem(
            **self.bibitem_referencegroup_data
        )

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, "static/schemas/v3.xsd")
        self.xmlschema = etree.XMLSchema(file=file_path)

    def test_bibliographicitem_to_xml(self):
        """
        Test that a BibliographicItem is properly converted to XML,
        and that its format validates against a converted authoritative
        schema (xml2rfc_compat/tests/static/v3.xsd).
        More info about the schema here
        https://github.com/ietf-ribose/bibxml-service/issues/155
        """

        xml_reference = serialize(self.bibitem_reference)
        xml_referencegroup = serialize(self.bibitem_referencegroup)

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, "static/schemas/v3.xsd")
        xmlschema = etree.XMLSchema(file=file_path)

        xmlschema.assertValid(xml_reference)
        xmlschema.assertValid(xml_referencegroup)

    def test_build_refcontent_string(self):
        """
        Test build_refcontent_string returns a valid XML output.
        Test that schema is valid and that output content
        matches the input.

        A valid reference output looks like:
        <reference anchor="ref_01">
            <front>
                <title py:pytype="str">title</title>
                <author fullname="Mr Cerf" surname="Cerf" initials="Mr"/>
                <date year="1996" month="February"/>
                <abstract>
                    <t>abstract_content</t>
                </abstract>
            </front>
            <refcontent>Ref Content</refcontent>
            <seriesInfo name="IEEE" value="IEEE P2740/D-6.5 2020-08"/>
        </reference>
        """
        reference = create_reference(self.bibitem_reference)
        self.assertEqual(reference.tag, "reference")
        anchor = reference.keys()[0]
        self.assertEqual(anchor, "anchor")
        self.assertEqual(
            reference.get(anchor), self.bibitem_reference_data["docid"][0]["id"]
        )

        # <front> element
        front = reference.getchildren()[0]
        self.assertEqual(front.tag, "front")

        # <title> element
        title = front.getchildren()[0]
        self.assertEqual(title.tag, "title")
        self.assertEqual(title.text, self.bibitem_reference_data["title"][0]["content"])

        # <author> element
        author = front.getchildren()[1]
        self.assertEqual(author.tag, "author")
        self.assertEqual(author.keys()[0], "fullname")
        self.assertEqual(author.keys()[1], "surname")
        self.assertEqual(author.keys()[2], "initials")
        self.assertEqual(
            author.get(author.keys()[0]),
            self.contributor_person_data["person"]["name"]["completename"]["content"],
        )
        self.assertEqual(
            author.get(author.keys()[1]),
            self.contributor_person_data["person"]["name"]["surname"]["content"],
        )
        self.assertEqual(
            author.get(author.keys()[2]),
            self.contributor_person_data["person"]["name"]["initial"][0]["content"],
        )

        # <date> element
        date = front.getchildren()[2]
        self.assertEqual(date.tag, "date")

        self.assertEqual(date.keys()[0], "year")
        self.assertEqual(date.keys()[1], "month")
        self.assertEqual(
            date.get(date.keys()[0]),
            self.bibitem_reference_data["date"][0]["value"].split("-")[0],
        )

        # <abstract> element
        abstract = front.getchildren()[3]
        self.assertEqual(abstract.tag, "abstract")
        self.assertEqual(
            abstract.getchildren()[0],
            self.bibitem_reference_data["abstract"][0]["content"],
        )

        # <refcontent> element
        refcontent = reference.getchildren()[1]
        self.assertEqual(
            refcontent,
            f"{self.bibitem_reference_data['extent']['locality'][0]['reference_from']}, "
            f"vol. {self.bibitem_reference_data['extent']['locality'][1]['reference_from']}, "
            f"no. {self.bibitem_reference_data['extent']['locality'][2]['reference_from']}, "
            f"pp. {self.bibitem_reference_data['extent']['locality'][3]['reference_from']}"
        )

    def test_build_refcontent_string_with_date_type_different_than_published(self):
        """
        build_refcontent_string should create a <date> tag using the date with
        type == 'published'. If no date is of this type, it should choose
        a random date between the ones provided.
        """
        # TODO: Indirectly testing build_refcontent_string without calling it,
        # not sure if a good idea
        data = copy(self.bibitem_reference_data)
        data["date"][0]["type"] = "random_type"
        new_bibitem = BibliographicItem(**data)
        reference = create_reference(new_bibitem)
        date = reference.getchildren()[0].getchildren()[2]
        self.assertEqual(
            date.get(date.keys()[0]), data["date"][0]["value"].split("-")[0]
        )

    def test_build_refcontent_string_with_localitystack(self):
        title = "Container Title"
        volume = "1"
        issue = "2"
        page = "3"
        extent = LocalityStack(locality=[
            Locality(type="container-title", reference_from=title),
            Locality(type="volume", reference_from=volume),
            Locality(type="issue", reference_from=issue),
            Locality(type="page", reference_from=page),

        ])
        refcontent = build_refcontent_string(extent)
        self.assertEqual(refcontent, f"{title}, vol. {volume}, no. {issue}, pp. {page}")

    def test_build_refcontent_string_with_locality(self):
        title = "Container Title"
        extent = Locality(type="container-title", reference_from=title)

        refcontent = build_refcontent_string(extent)
        self.assertEqual(refcontent, f"{title}")

    def test_create_author(self):
        """
        create_author should return a valid XML.
        The XML should validate against an
        authoritative schema.
        """
        author_xsd = StringIO(
            """
            <xsd:schema attributeFormDefault="unqualified" elementFormDefault="qualified"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <xsd:element name="author" type="authorType"/>
                <xsd:complexType name="authorType">
                    <xsd:sequence>
                        <xsd:element type="xsd:string" name="organization"/>
                    </xsd:sequence>
                </xsd:complexType>
            </xsd:schema>
            """
        )
        xmlschema_doc = etree.parse(author_xsd)
        author_xmlschema = etree.XMLSchema(xmlschema_doc)

        author_organization = create_author(self.contributor_organization)
        author_person = create_author(self.contributor_person)
        self.assertEqual(author_organization.tag, "author")
        self.assertEqual(author_person.tag, "author")

        author_xmlschema.validate(author_organization)
        author_xmlschema.validate(author_person)

    def test_fail_create_author_if_incompatible_roles(self):
        """
        create_author should fail if no person or organization has a role.
        """
        contributor_organization = copy(self.contributor_organization)
        contributor_person = copy(self.contributor_person)
        contributor_organization.role = None
        contributor_person.role = None
        with self.assertRaises(ValueError):
            create_author(contributor_organization)
            create_author(contributor_person)

    def test_fail_create_author_if_missing_person_or_organization(self):
        """
        create_author should fail if no person or organization is provided
        """
        contributor_organization = copy(self.contributor_organization)
        contributor_person = copy(self.contributor_person)
        contributor_organization.organization = None
        contributor_person.person = None
        with self.assertRaises(ValueError):
            create_author(contributor_organization)
            create_author(contributor_person)

    def test_get_suitable_anchor(self):
        """
        get_suitable_anchor should return the correct anchor value
        """
        anchor = get_suitable_anchor(self.bibitem_reference)
        self.assertIsInstance(anchor, str)
        self.assertEqual(
            anchor,
            next(
                docid.id
                for docid in self.bibitem_reference.docid
                if docid.scope == "anchor"
            ),
        )

    def test_get_suitable_anchor_without_scope_with_primary(self):
        """
        get_suitable_anchor should return DocID.id if primary=True and
        DocID.scope is not provided or DocID.scope != "anchor"
        """
        bibitem_with_primary_docid = copy(self.bibitem_reference)
        bibitem_with_primary_docid.docid[0].primary = True
        bibitem_with_primary_docid.docid[0].scope = None

        anchor = get_suitable_anchor(bibitem_with_primary_docid)
        self.assertIsInstance(anchor, str)
        self.assertEqual(
            anchor,
            next(
                docid.id for docid in bibitem_with_primary_docid.docid if docid.primary
            ),
        )

        bibitem_with_no_scope = copy(self.bibitem_reference)
        bibitem_with_no_scope.docid[0].scope = "no_scope"
        anchor = get_suitable_anchor(bibitem_with_no_scope)
        self.assertIsInstance(anchor, str)
        self.assertEqual(
            anchor,
            next(
                docid.id
                for docid in bibitem_with_no_scope.docid
                if docid.scope == "no_scope"
            ),
        )

    def test_fail_get_suitable_anchor(self):
        """
        get_suitable_anchor should fail if BibliographicItem.docid == []
        """
        self.bibitem_reference.docid = []
        with self.assertRaises(ValueError):
            get_suitable_anchor(self.bibitem_reference)

    def test_get_suitable_target(self):
        """
        get_suitable_target should return the content of the
        Link whose type == "src"
        """
        link_content = "link_content"
        links = [
            Link(content=link_content, type="src"),
            Link(content="not_src_link", type="not_src"),
        ]
        target_content = get_suitable_target(links)
        self.assertIsInstance(target_content, str)
        self.assertEqual(target_content, link_content)

    def test_get_suitable_target_non_src_link(self):
        """
        get_suitable_target should return the link content if Link.type != "src"
        """
        link_content = "not_src_link"
        links = [Link(content=link_content, type="not_src")]
        target_content = get_suitable_target(links)
        self.assertIsInstance(target_content, str)
        self.assertEqual(target_content, link_content)

    def test_fail_get_suitable_target(self):
        """
        get_suitable_target should fail if called with
        a list of empty links
        """
        links = []
        with self.assertRaises(ValueError):
            get_suitable_target(links)

    def test_extract_doi_series(self):
        """
        extract_doi_series should return the correct
        type and id values
        """
        id_value = "10.17487/RFC4036"
        docid = DocID(id=id_value, type="DOI")
        type, id = extract_doi_series(docid)
        self.assertEqual(type, "DOI")
        self.assertEqual(id, id_value)

    def test_fail_extract_doi_series(self):
        """
        extract_doi_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "10.17487/RFC4036"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_doi_series(docid))

    def test_extract_rfc_series(self):
        """
        extract_rfc_series should return the correct
        serie and id values
        """
        id_value = "RFC 4036"
        docid = DocID(id=id_value, type="IETF")
        serie, id = extract_rfc_series(docid)
        self.assertEqual(serie, "RFC")
        self.assertEqual(id, id_value.split(" ")[-1])

    def test_fail_extract_rfc_series(self):
        """
        extract_rfc_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "RFC 4036"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_rfc_series(docid))

    def test_extract_id_series(self):
        """
        extract_id_series should return the correct
        type and id values
        """
        id_value = "draft-ietf-hip-rfc5201-bis-13"
        type_value = "Internet-Draft"
        docid = DocID(id=id_value, type=type_value)
        serie, id = extract_id_series(docid)
        self.assertEqual(serie, type_value)
        self.assertEqual(id, id_value)

    def test_fail_extract_id_series(self):
        """
        extract_id_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "draft-ietf-hip-rfc5201-bis-13"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_id_series(docid))

    def test_extract_w3c_series(self):
        """
        extract_w3c_series should return the correct
        type and id values
        """
        id_value = "W3C.REC-owl2-syntax-20121211"
        type_value = "W3C"
        docid = DocID(id=id_value, type=type_value)
        serie, id = extract_w3c_series(docid)
        self.assertEqual(serie, type_value)
        self.assertEqual(id, id_value.replace(".", " ").split("W3C ")[-1])

    def test_fail_extract_w3c_series(self):
        """
        extract_w3c_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "W3C REC-owl2-syntax-20121211"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_w3c_series(docid))

    def test_extract_3gpp_tr_series(self):
        """
        extract_3gpp_tr_series should return the correct
        type and id values
        """
        id_value = "3GPP TR 25.321:Rel-8/8.3.0"
        type_value = "3GPP"
        docid = DocID(id=id_value, type=type_value)
        serie, id = extract_3gpp_tr_series(docid)
        self.assertEqual(serie, f"{type_value} TR")
        self.assertEqual(
            id,
            f"{id_value.split('3GPP TR ')[1].split(':')[0]} {id_value.split('/')[-1]}",
        )

    def test_fail_extract_3gpp_tr_series(self):
        """
        extract_3gpp_tr_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "3GPP TR 25.321:Rel-8/8.3.0"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_3gpp_tr_series(docid))

    def test_extract_ieee_series(self):
        """
        extract_ieee_series should return the correct
        type and id values
        """
        id_value = "IEEE P2740/D-6.5.2020-08"
        type_value = "IEEE"
        docid = DocID(id=id_value, type=type_value)
        serie, id = extract_ieee_series(docid)
        id_value_alternative, year, *_ = (
            docid.id.split(" ")[-1].lower().strip().split(".")
        )
        self.assertEqual(serie, type_value)
        self.assertTrue(id == "%s-%s" % (id_value_alternative.replace("-", "."), year))

    def test_extract_ieee_series_with_malformed_id(self):
        """
        extract_ieee_series should return DocID.id if id_value is not
        formatted properly (e.g. right format "IEEE P2740/D-6.5.2020-08").
        """
        id_value = "IEEE P2740/D-6.5 2020-08"
        type_value = "IEEE"
        docid = DocID(id=id_value, type=type_value)
        serie, id = extract_ieee_series(docid)
        self.assertEqual(serie, type_value)
        self.assertEqual(id, id_value)

    def test_fail_extract_ieee_series(self):
        """
        extract_ieee_series should fail with the wrong combination
        of DocID.id and DocID.type.
        """
        id_value = "IEEE P2740/D-6.5.2020-08"
        docid = DocID(id=id_value, type="TYPE")
        self.assertIsNone(extract_ieee_series(docid))

    def test_create_abstract(self):
        """
        create_abstract should return the content in English (en or eng)
        if present or any other content otherwise (normally the first
        of the list)
        """
        abstracts: List[GenericStringValue] = [
            GenericStringValue(content="content", format="text/html", language="en"),
            GenericStringValue(content="contenuto", format="text/html", language="it"),
        ]

        abstract = create_abstract(abstracts)
        self.assertEqual(
            abstract.getchildren()[0],
            next(
                abstract.content for abstract in abstracts if abstract.language == "en"
            ),
        )
        self.assertEqual(abstract.tag, "abstract")

    def test_fail_create_abstract(self):
        """
        create_abstract should fail if called with a list
        of empty abstracts
        """
        abstracts: List[GenericStringValue] = []
        with self.assertRaises(ValueError):
            create_abstract(abstracts)

    def test_get_paragraphs(self):
        """
        get_paragraphs should return the right content based on
        the paragraph format (HTML, JATS or plain text)
        """
        html_content = "HTML"
        html_paragraph = GenericStringValue(
            content=f"<p>{html_content}</p>", format="text/html"
        )
        paragraph = get_paragraphs(html_paragraph)
        self.assertEqual(paragraph[0], html_content)

        jats_content = "JATS"
        jats_paragraph = GenericStringValue(
            content=f"<jats:p>{jats_content}</jats:p>", format="application/x-jats+xml"
        )
        paragraph = get_paragraphs(jats_paragraph)
        self.assertEqual(paragraph[0], jats_content)

        invalid_content = "invalid"
        invalid_paragraph = GenericStringValue(
            content=invalid_content, format="invalid"
        )
        paragraph = get_paragraphs(invalid_paragraph)
        self.assertEqual(paragraph[0], invalid_content)

    def test_fail_get_html_paragraph(self):
        """
        get_paragraphs_html should fail if called with the
        wrong paragraph format
        """
        paragraph = GenericStringValue(
            content="content", format="application/x-jats+xml"
        )
        with self.assertRaises(ValueError):
            get_paragraphs_html(paragraph)

    def test_fail_get_jats_paragraph(self):
        """
        get_paragraphs_jats should fail if called with the
        wrong paragraph format
        """
        paragraph = GenericStringValue(content="content", format="text/html")
        with self.assertRaises(ValueError):
            get_paragraphs_jats(paragraph)

    def _validate_yaml_data(self, url):
        import requests
        r = requests.get(url)
        yaml_object = yaml.safe_load(r.content)
        bibitem = BibliographicItem(**yaml_object)
        serialized_data = serialize(bibitem)

        self.xmlschema.assertValid(serialized_data)

    def test_validate_rfcs_data(self):
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-rfcs/main/data/RFC0001.yaml"
        self._validate_yaml_data(url)

    def test_validate_misc_data(self):
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-misc/main/data/reference.ANSI.T1-102.1987.yaml"
        self._validate_yaml_data(url)

    def test_validate_internet_drafts_data(self):
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-ids/main/data/draft--pale-email-00.yaml"
        self._validate_yaml_data(url)

    def test_validate_w3c_data(self):
        # TODO FIX
        """
        lxml.etree.DocumentInvalid: Element 'front': Missing child element(s). Expected is one of ( seriesInfo, author ).
        """
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-w3c/main/data/2dcontext.yaml"
        self._validate_yaml_data(url)

    def test_validate_threegpp_data(self):
        # TODO FIX
        """
        pydantic.error_wrappers.ValidationError: 1 validation error for BibliographicItem
        contributor -> 0 -> organization -> contact -> 0
        __init__() got an unexpected keyword argument 'street' (type=type_error)
        """
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-3gpp/main/data/TR_00.01U_UMTS_3.0.0.yaml"
        self._validate_yaml_data(url)

    def test_validate_ieee_data(self):
        # TODO FIX
        """
        pydantic.error_wrappers.ValidationError: 1 validation error for BibliographicItem
        contributor -> 0 -> organization -> contact -> 0
        __init__() got an unexpected keyword argument 'city' (type=type_error)
        """
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-ieee/main/data/AIEE_11-1937.yaml"
        self._validate_yaml_data(url)

    def test_validate_iana_data(self):
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-iana/main/data/_6lowpan-parameters.yaml"
        self._validate_yaml_data(url)

    def test_validate_rfcsubseries_data(self):
        # TODO FIX
        """
        lxml.etree.DocumentInvalid: Element 'front': Missing child element(s). Expected is one of ( seriesInfo, author ).
        """
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-rfcsubseries/main/data/BCP0003.yaml"
        self._validate_yaml_data(url)

    def test_validate_nist_data(self):
        # TODO FIX
        """
        pydantic.error_wrappers.ValidationError: 1 validation error for BibliographicItem
        contributor -> 8 -> organization -> contact -> 0
        __init__() got an unexpected keyword argument 'city' (type=type_error)
        """
        url = "https://raw.githubusercontent.com/ietf-tools/relaton-data-nist/main/data/NBS_BH_1.yaml"
        self._validate_yaml_data(url)
