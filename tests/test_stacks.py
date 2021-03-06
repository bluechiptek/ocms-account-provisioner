import moto
import pytest

from lib.stacks import Stack, Template
from tests import (VALID_TEMPLATE1_URL,
                   VALID_TEMPLATE2_URL)


def test_template_invalid_path_format():
    with pytest.raises(ValueError):
        Template("test")


def test_template_hexdigest():
    """hexdigest test reading from file and validating template"""
    template = Template(VALID_TEMPLATE1_URL)
    assert template.hexdigest == 'e52c979111e5ea905648146555c689b32b2d5bea'


@pytest.fixture
def cfn_templates():
    """Generating template object in a fixture as moto does not implement the
    cloudformation validate_template method call and will cause a test case
    using mock_cloudformation to fail.
    """
    templates = (
        Template(VALID_TEMPLATE1_URL),
        Template(VALID_TEMPLATE2_URL)
                 )
    return templates


@moto.mock_sts
@moto.mock_cloudformation
@pytest.mark.incremental
class TestCfnCreateUpdate:

    def test_create_stack(self, cfn_templates):
        template = cfn_templates[0]
        stack = Stack("OcmsTest")
        stack.apply_template(template.body)
        assert stack.hexdigest == template.hexdigest

    def test_update_stack(self, cfn_templates):
        template1, template2 = cfn_templates
        stack = Stack("OcmsTest")
        stack.apply_template(template1.body)
        stack.apply_template(template2.body)
        assert stack.hexdigest == template2.hexdigest
