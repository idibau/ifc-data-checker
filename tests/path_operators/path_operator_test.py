"""Path Operator Unit Test Suite"""
import unittest

from tests.helpers import IfcInstanceMock


class TestPathOperator:
    """Test Path Operator"""
    # pylint: disable=too-few-public-methods

    class TestParameterValidation(unittest.TestCase):
        """Test path operator parameter validation"""

        path_operator_class = None
        default_path_operator = None
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )

        def check_parameter(self):
            """Checks that all the base class parameters are set.

            `path_operator_class`, `default_path_operator`
            need to be set by sub class. If not, the test case will fail

            `ifc_instance` is set by default, can be overridden"""
            if self.path_operator_class is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`path_operator_class` need to be set by sub class.")
            if self.default_path_operator is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`default_path_operator` need to be set by sub class.")
            if self.ifc_instance is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`ifc_instance` need to be set by sub class.")

        def test_none_actual_path_position(self):
            """Tests the path operator on correct parameter validation of `actual_path_position`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.path_operator_class.apply``

            Given:
                * actual_path_position: ``None``
                * path_operator: using default_path_operator from subclass

            Expected:
                Raises ``ValueError`` because of `actual_path_position` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.path_operator_class,
                              None, self.default_path_operator)

        def test_none_actual_path_position_list(self):
            """Tests the path operator on correct parameter validation of `actual_path_position`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.path_operator_class.apply``

            Given:
                * actual_path_position: object of `self.ifc_instance`
                * path_operator: using default_path_operator from subclass

            Expected:
                Raises ``ValueError`` because of `actual_path_position`
                parameter isn't of type ``list``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.path_operator_class,
                              self.ifc_instance, self.default_path_operator)

        def test_none_path_operator(self):
            """Tests the path operator on correct parameter validation of `path_operator`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.path_operator_class.apply``

            Given:
                * actual_path_position: a list of `self.ifc_instance`
                * path_operator: ``None``

            Expected:
                Raises ``ValueError`` because of `path_operator` parameter is ``None``"""
            self.check_parameter()
            actual_path_position = [self.ifc_instance, self.ifc_instance,
                                    self.ifc_instance, self.ifc_instance]
            self.assertRaises(ValueError, self.path_operator_class,
                              actual_path_position, None)

        def test_invalid_path_operator_definition(self):
            """Tests the path operator on correct
            parameter validation of `definition`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_component_class``

            Given:
                * `ifc_instance`: a list of `self.ifc_instance`
                * `definition`: "Invalid"

            Expected:
                Raises ``ValueError`` because of `definition`
                parameter is ``"Invalid"``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.path_operator_class,
                              [self.ifc_instance], "Invalid")
