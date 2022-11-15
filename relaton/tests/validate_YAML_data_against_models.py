# type: ignore
import os
from unittest import TestCase

import yaml
from lxml import etree

from relaton.models import BibliographicItem
from relaton.serializers.bibxml import serialize


class DataValidationTestCase(TestCase):
    """
    Validate YAML data against models format and
    validate XML output against authoritative schema.
    """
    schema_version = "1.13.0"

    def setUp(self):
        self.module_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.module_dir, "static/schemas/v3.xsd")
        self.xmlschema = etree.XMLSchema(file=file_path)

    def _validate_dataset(self, dataset):
        dataset_dir = os.path.join(self.module_dir, f"static/fixtures/v{self.schema_version}/{dataset}")
        for file in os.listdir(dataset_dir):
            file_path = os.path.join(f"{dataset_dir}/{file}")
            with open(file_path) as stream:
                yaml_object = yaml.safe_load(stream)
                bibitem = self._construct_bibliographicitem(yaml_object)
                serialized_data = serialize(bibitem)
                self._validate_xml_against_authoritative_schema(serialized_data)

    def _construct_bibliographicitem(self, yaml_object):
        """
        Implicitly validates YAML input format against current model schema version
        """
        return BibliographicItem(**yaml_object)

    def _validate_xml_against_authoritative_schema(self, xml):
        """
        Validate XML output against authoritative schema
        """
        self.xmlschema.assertValid(xml)

    def test_validate_rfcs_data(self):
        self._validate_dataset("rfcs")

    def test_validate_misc_data(self):
        self._validate_dataset("misc")

    def test_validate_internet_drafts_data(self):
        self._validate_dataset("internet_drafts")

    def test_validate_w3c_data(self):
        self._validate_dataset("w3c")

    def test_validate_threegpp_data(self):
        self._validate_dataset("3gpp")

    def test_validate_ieee_data(self):
        self._validate_dataset("ieee")

    def test_validate_iana_data(self):
        self._validate_dataset("iana")

    def test_validate_rfcsubseries_data(self):
        self._validate_dataset("rfcsubseries")

    def test_validate_nist_data(self):
        self._validate_dataset("nist")
