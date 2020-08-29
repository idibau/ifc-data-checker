"""Constraint Check Unit Test Suite"""
import unittest

from tests.helpers import IfcInstanceMock


class TestConstraintCheck:
    """Test Constraint Check"""
    # pylint: disable=too-few-public-methods

    class TestParameterValidation(unittest.TestCase):
        """Test constraint check parameter validation"""

        constraint_check_class = None
        default_constraint = None
        default_path_result = None
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )

        def check_parameter(self):
            """Checks that all the base class parameters are set.

            `constraint_check_class`, `default_constraint`, `default_path_result`
            need to be set by sub class. If not, the test case will fail

            `ifc_instance` is set by default, can be overridden"""
            if self.constraint_check_class is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`constraint_check_class` need to be set by sub class.")
            if self.default_constraint is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`default_constraint` need to be set by sub class.")
            if self.default_path_result is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`default_path_result` need to be set by sub class.")
            if self.ifc_instance is None:
                self.fail("Incorrect usage of `TestParameterValidation`." +
                          "`ifc_instance` need to be set by sub class.")

        def test_none_instance(self):
            """Tests the constraint check on correct parameter validation of `ifc_instance`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_check_class.validate``

            Given:
                * ifc_instance: ``None``
                * default_path_result: set by sub class
                * default_constraint: set by sub class

            Expected:
                Raises ``ValueError`` because of `ifc_instance` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_check_class,
                              self.default_constraint, self.default_path_result, None)

        def test_none_path_result(self):
            """Tests the constraint check on correct parameter validation of `path_result`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_check_class.validate``

            Given:
                * ifc_instance: The mock ifc instance
                * default_path_result: ``None``
                * default_constraint: set by sub class

            Expected:
                Raises ``ValueError`` because of `path_result` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_check_class,
                              self.default_constraint, None, self.ifc_instance)

        def test_none_constraint(self):
            """Tests the constraint check on correct parameter validation of `constraint`

            Test-Purpose:
                parameter input validation

            Under Test:
                * ``self.constraint_check_class.validate``

            Given:
                * ifc_instance: The mock ifc instance
                * default_path_result: set by sub class
                * default_constraint: ``None``

            Expected:
                Raises ``ValueError`` because of `constraint` parameter is ``None``"""
            self.check_parameter()
            self.assertRaises(ValueError, self.constraint_check_class,
                              None, self.default_path_result, self.ifc_instance)
