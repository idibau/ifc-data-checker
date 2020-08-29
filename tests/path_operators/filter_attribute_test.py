"""Filter Attribute Unit Test Suite"""
from ifc_data_checker.path_operators import AttributeFilterPathOperator
from ifc_data_checker import config

from tests.path_operators.path_operator_test import TestPathOperator
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestFilterAttribute(TestPathOperator.TestParameterValidation):
    """Test Filter Attribute"""

    path_operator_class = AttributeFilterPathOperator
    default_path_operator = {"attribute": "attribute1", "value": "value1"}

    def test_filter_attribute_same_instances(self):
        """Tests ``AttributeFilterPathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each instance, which matching the filtering criteria, gets filtered.

        Under Test:
            ``AttributeFilterPathOperator.apply``

        Given:
            * attribute_name: The name of the attribute to filter
            * filtering_value: The value of the attribute to filter
            * instances: List of Mock Instance, each matching the filter criteria
            * path_operator: the path operator using `attribute_name` and `filtering_value`

        Expected:
            The same list as the given `instances` list,
            because every instance matching the filter criteria.

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        attribute_name = "property"
        filtering_value = "property_value"
        instance = MicroMock(property=filtering_value)
        instances = [instance, instance, instance]
        path_operator = {"attribute": attribute_name, "value": filtering_value}
        expected_result = [instance, instance, instance]
        operator = AttributeFilterPathOperator(instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_filter_attribute_different_instances(self):
        """Tests ``AttributeFilterPathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each instance, which matching the filtering criteria, gets filtered.

        Under Test:
            ``AttributeFilterPathOperator.apply``

        Given:
            * attribute_name: The name of the attribute to filter
            * filtering_value: The value of the attribute to filter
            * instances: List of Mock Instance, some matching the filter criteria, some won't
            * path_operator: the path operator using `attribute_name` and `filtering_value`

        Expected:
            A filtered list with the instances matching the filter criteria only

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        attribute_name = "property"
        filtering_value = "property_value"
        instance = MicroMock(property=filtering_value)
        different_instance = MicroMock(other=42)
        instances = [instance, different_instance,
                     instance, different_instance,
                     instance, different_instance]
        path_operator = {"attribute": attribute_name, "value": filtering_value}
        expected_result = [instance, instance, instance]
        operator = AttributeFilterPathOperator(instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_filter_attribute_none_attribute_name(self):
        """Tests ``AttributeFilterPathOperator`` on validating the input parameter correctly.

        Test-Purpose:
            parameter input validation of the path operator `attribute_name`

        Under Test:
            ``AttributeFilterPathOperator``

        Given:
            * filtering_value: The value of the attribute to filter
            * instances: List of Mock Instance
            * path_operator: the path operator using `filtering_value`

        Expected:
            Raises ``ValueError`` because the path operator has no defined `attribute_name`"""
        filtering_value = "property_value"
        instance = MicroMock(property=filtering_value)
        instances = [instance, instance, instance]
        path_operator = {"value": filtering_value}
        self.assertRaises(ValueError, AttributeFilterPathOperator,
                          instances, path_operator)

    def test_filter_attribute_empty_attribute_name(self):
        """Tests ``AttributeFilterPathOperator`` on validating the input parameter correctly.

        Test-Purpose:
            parameter input validation of the path operator `attribute_name`

        Under Test:
            ``AttributeFilterPathOperator``

        Given:
            * filtering_value: The value of the attribute to filter
            * instances: List of Mock Instance
            * path_operator: the path operator using `filtering_value`

        Expected:
            Raises ``ValueError`` because the path operator has an empty defined `attribute_name`"""
        filtering_value = "value"
        instance = MicroMock(property=filtering_value)
        instances = [instance, instance, instance]
        path_operator = {"attribute": "", "value": filtering_value}
        self.assertRaises(ValueError, AttributeFilterPathOperator,
                          instances, path_operator)

    def test_filter_attribute_none_attribute_value(self):
        """Tests ``AttributeFilterPathOperator`` on validating the input parameter correctly.

        Test-Purpose:
            parameter input validation of the path operator `attribute_value`

        Under Test:
            ``AttributeFilterPathOperator``

        Given:
            * attribute_name: The name of the attribute to filter
            * instances: List of Mock Instance
            * path_operator: the path operator using `attribute_name`

        Expected:
            Raises ``ValueError`` because the path operator has no defined `attribute_value`"""
        attribute_name = "property"
        instance = MicroMock(property="property1")
        instances = [instance, instance, instance]
        path_operator = {"attribute": attribute_name}
        self.assertRaises(ValueError, AttributeFilterPathOperator,
                          instances, path_operator)

    def test_filter_attribute_empty_attribute_value(self):
        """Tests ``AttributeFilterPathOperator`` on validating the input parameter correctly.

        Test-Purpose:
            parameter input validation of the path operator `attribute_value`

        Under Test:
            ``AttributeFilterPathOperator.apply``

        Given:
            * filtering_value: The value of the attribute to filter
            * instances: List of Mock Instance
            * path_operator: the path operator using `filtering_value`

        Expected:
            Raises ``ValueError`` because the path operator
            has an empty defined `attribute_value`"""
        instance = MicroMock(property="property_value")
        instances = [instance, instance, instance]
        attribute_name = "property"
        path_operator = {"attribute": attribute_name, "value": ""}
        self.assertRaises(ValueError, AttributeFilterPathOperator,
                          instances, path_operator)

    def test_filter_attribute_path_operator_yaml_keys(self):
        """Tests ``AttributeFilterPathOperator`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``AttributeFilterPathOperator`` won't change

        Under Test:
            ``AttributeFilterPathOperator.yaml_keys``

        Given:
            ``AttributeFilterPathOperator``

        Expected:
            The `yaml_keys` of ``AttributeFilterPathOperator`` is 'attribute' and 'value'"""
        self.assertEqual(("attribute", "value",),
                         AttributeFilterPathOperator.get_yaml_keys())

    def test_filter_attribute_apply_path(self):
        """Tests ``apply_path`` on applying the path operators correctly.

        Test-Purpose:
            Tests that the path operator ``AttributeFilterPathOperator``
            applied correctly on the actual value

        Under Test:
            * ``apply_path``
            * implicit ``_get_path_operator``
            * implicit ``all_path_operators``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock`` with list of `attributes`
            * `attributes`: list of MicroMock with `MicroMock(IsDefinedBy="MockWindow")` and
            `MicroMock(IsDefinedBy="MockDoor")`
            * list with the path operator ``ListPathOperator``, ``AttributeFilterPathOperator``:
            `[{"attribute": "IsDefinedBy", "value": "MockWindow"}]`

        Expected:
            That the path operator ``AttributeFilterPathOperator`` get applied on the list of
            `attributes` and that the `path_result` is the object of
            `MicroMock(IsDefinedBy="MockWindow")`

        Comment:
            * Usage of ``IfcInstanceMock`` to represent an ifc instance
            * Usage of ``MicroMock`` to represent an attribute"""
        ifc_attribute = MicroMock(
            IsDefinedBy="MockWindow"
        )
        other_ifc_attribute = MicroMock(
            IsDefinedBy="MockDoor"
        )
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType",
            attributes=[ifc_attribute, other_ifc_attribute]
        )
        path_operator = {"attribute": "IsDefinedBy", "value": "MockWindow"}
        operator = config.get_path_operator(path_operator, [ifc_instance])
        self.assertIsInstance(operator, AttributeFilterPathOperator)
