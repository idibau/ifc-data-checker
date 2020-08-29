"""Constraint Component Test"""
import unittest

from ifc_data_checker.constraints import ConstraintComponent

from tests.helpers import IfcInstanceMock


class TestConstraintComponent:
    """Test Constraint Component"""
    # pylint: disable=too-few-public-methods

    class TestParameterValidation(unittest.TestCase):
        """Test constraint component parameter validation"""

        constraint_component_class = ConstraintComponent
        default_constraint_component = None
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )

        def check_parameter(self):
            """Checks that all the base class parameters are set.

            `constraint_component_class`, `default_constraint_component`
            need to be set by sub class. If not, the test case will fail

            `ifc_instance` is set by default, can be overridden"""
            if self.constraint_component_class == ConstraintComponent:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`constraint_component_class` need to be set by sub class.")
            if self.default_constraint_component is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`default_constraint_component` need to be set by sub class.")
            if self.ifc_instance is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`ifc_instance` need to be set by sub class.")

        def test_none_ifc_instance(self):
            """Tests the constraint component on correct parameter validation of `ifc_instances`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_component_class.validate``

            Given:
                * `ifc_instance`: ``None``
                * `constraint_component`: using default_constraint_component from subclass

            Expected:
                Raises ``ValueError`` because of `ifc_instances` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_component_class,
                              self.default_constraint_component, None)

        def test_none_constraint_component_definition(self):
            """Tests the constraint component on correct
            parameter validation of `constraint_component`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_component_class``

            Given:
                * `ifc_instances`: a list of `self.ifc_instance`
                * `constraint_component`: ``None``

            Expected:
                Raises ``ValueError`` because of `constraint_component` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_component_class,
                              None, tuple([self.ifc_instance]))

        def test_invalid_constraint_component_definition(self):
            """Tests the constraint component on correct
            parameter validation of `constraint_component`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_component_class``

            Given:
                * `ifc_instance`: a list of `self.ifc_instance`
                * `constraint_component`: ``None``

            Expected:
                Raises ``ValueError`` because of `constraint_component`
                parameter is ``"Invalid"``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_component_class,
                              "Invalid", tuple([self.ifc_instance]))
