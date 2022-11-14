# type: ignore
import os
from unittest import TestCase

import yaml
from lxml import etree

from relaton.models import BibliographicItem
from relaton.serializers.bibxml import serialize


class DataValidationTestCase(TestCase):
    """
    Asserts that XML output conforms to the authoritative schema.
    """
    schema_version = "1.13.0"

    def setUp(self):
        self.module_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.module_dir, "static/schemas/v3.xsd")
        self.xmlschema = etree.XMLSchema(file=file_path)

    def _validate_yaml_data(self, dataset):
        dataset_dir = os.path.join(self.module_dir, f"static/fixtures/v{self.schema_version}/{dataset}")
        for file in os.listdir(dataset_dir):
            file_path = os.path.join(f"{dataset_dir}/{file}")
            with open(file_path) as stream:
                yaml_object = yaml.safe_load(stream)
                bibitem = BibliographicItem(**yaml_object)
                serialized_data = serialize(bibitem)
                self.xmlschema.assertValid(serialized_data)

    # TODO: add multiple documents for each dataset

    def test_validate_rfcs_data(self):
        self._validate_yaml_data("rfcs")

    def test_validate_misc_data(self):
        self._validate_yaml_data("misc")

    def test_validate_internet_drafts_data(self):
        self._validate_yaml_data("internet_drafts")

    def test_validate_w3c_data(self):
        self._validate_yaml_data("w3c")

    def test_validate_threegpp_data(self):
        self._validate_yaml_data("3gpp")

    def test_validate_ieee_data(self):
        self._validate_yaml_data("ieee")

    def test_validate_iana_data(self):
        self._validate_yaml_data("iana")

    def test_validate_rfcsubseries_data(self):
        self._validate_yaml_data("rfcsubseries")

    def test_validate_nist_data(self):
        self._validate_yaml_data("nist")
