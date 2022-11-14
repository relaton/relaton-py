# type: ignore
import os
from unittest import TestCase

import yaml
from lxml import etree

from relaton.models import BibliographicItem
from relaton.serializers.bibxml import serialize


class DataValidationTestCase(TestCase):
    """
    Validate YAML data against model format version and
    validate XML output against authoritative schema.
    """
    schema_version = "1.13.0"

    def setUp(self):
        self.module_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.module_dir, "static/schemas/v3.xsd")
        self.xmlschema = etree.XMLSchema(file=file_path)

    def _validate_yaml_data_and_xmlschema(self, dataset):
        dataset_dir = os.path.join(self.module_dir, f"static/fixtures/v{self.schema_version}/{dataset}")
        for file in os.listdir(dataset_dir):
            file_path = os.path.join(f"{dataset_dir}/{file}")
            with open(file_path) as stream:
                yaml_object = yaml.safe_load(stream)
                # validate YAML data against model format version
                bibitem = BibliographicItem(**yaml_object)
                serialized_data = serialize(bibitem)
                # validate XML output against authoritative schema
                self.xmlschema.assertValid(serialized_data)

    def test_validate_rfcs_data(self):
        self._validate_yaml_data_and_xmlschema("rfcs")

    def test_validate_misc_data(self):
        self._validate_yaml_data_and_xmlschema("misc")

    def test_validate_internet_drafts_data(self):
        self._validate_yaml_data_and_xmlschema("internet_drafts")

    def test_validate_w3c_data(self):
        self._validate_yaml_data_and_xmlschema("w3c")

    def test_validate_threegpp_data(self):
        self._validate_yaml_data_and_xmlschema("3gpp")

    def test_validate_ieee_data(self):
        self._validate_yaml_data_and_xmlschema("ieee")

    def test_validate_iana_data(self):
        self._validate_yaml_data_and_xmlschema("iana")

    def test_validate_rfcsubseries_data(self):
        self._validate_yaml_data_and_xmlschema("rfcsubseries")

    def test_validate_nist_data(self):
        self._validate_yaml_data_and_xmlschema("nist")
