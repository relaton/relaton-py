# type: ignore
import os
from unittest import TestCase

import yaml
from lxml import etree

from relaton.models import BibliographicItem
from relaton.serializers.bibxml import serialize


class DataValidationTestCase(TestCase):
    schema_version = "1.13.0"

    def setUp(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, "static/schemas/v3.xsd")
        self.xmlschema = etree.XMLSchema(file=file_path)

    def _validate_yaml_data(self, dataset, filename):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, f"static/fixtures/v{self.schema_version}/{dataset}/{filename}.yaml")
        with open(file_path) as stream:
            yaml_object = yaml.safe_load(stream)
            bibitem = BibliographicItem(**yaml_object)
            serialized_data = serialize(bibitem)
            self.xmlschema.assertValid(serialized_data)

    # TODO: add multiple documents for each dataset

    def test_validate_rfcs_data(self):
        self._validate_yaml_data("rfcs", "RFC0001")

    def test_validate_misc_data(self):
        self._validate_yaml_data("misc", "reference.ANSI.T1-102.1987")

    def test_validate_internet_drafts_data(self):
        self._validate_yaml_data("internet_drafts", "draft--pale-email-00")

    def test_validate_w3c_data(self):
        self._validate_yaml_data("w3c", "2dcontext")

    def test_validate_threegpp_data(self):
        self._validate_yaml_data("3gpp", "TR_00.01U_UMTS_3.0.0")

    def test_validate_ieee_data(self):
        self._validate_yaml_data("ieee", "AIEE_11-1943")

    def test_validate_iana_data(self):
        self._validate_yaml_data("iana", "_6lowpan-parameters")

    def test_validate_rfcsubseries_data(self):
        self._validate_yaml_data("rfcsubseries", "BCP0003")

    def test_validate_nist_data(self):
        self._validate_yaml_data("nist", "NBS_BH_1")
