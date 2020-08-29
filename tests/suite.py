"""IFC Data Checker Test Suite"""
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner

from tests.constraint_checks.equals_test import TestEqualsCheck
from tests.constraint_checks.exists_test import TestExistsCheck
from tests.constraint_checks.in_test import TestInCheck
from tests.constraint_checks.not_test import TestNotCheck
from tests.constraint_checks.type_test import TestTypeCheck

from tests.constraints.constraint_test import TestConstraint
from tests.constraints.and_test import TestAndConstraint
from tests.constraints.or_test import TestOrConstraint
from tests.constraints.set_test import TestSetConstraint

from tests.path_operators.filter_attribute_test import TestFilterAttribute
from tests.path_operators.filter_type_test import TestFilterType
from tests.path_operators.get_attribute_test import TestGetAttribute
from tests.path_operators.get_list_test import TestGetList


constraint_tests = TestLoader().loadTestsFromTestCase(
    TestConstraint)
and_tests = TestLoader().loadTestsFromTestCase(TestAndConstraint)
or_tests = TestLoader().loadTestsFromTestCase(TestOrConstraint)
set_tests = TestLoader().loadTestsFromTestCase(TestSetConstraint)

equals_tests = TestLoader().loadTestsFromTestCase(
    TestEqualsCheck)
exist_tests = TestLoader().loadTestsFromTestCase(
    TestExistsCheck)
in_tests = TestLoader().loadTestsFromTestCase(
    TestInCheck)
not_tests = TestLoader().loadTestsFromTestCase(
    TestNotCheck)
type_tests = TestLoader().loadTestsFromTestCase(
    TestTypeCheck)

filter_attribute_tests = TestLoader().loadTestsFromTestCase(
    TestFilterAttribute
)
filter_type_tests = TestLoader().loadTestsFromTestCase(
    TestFilterType
)
get_attribute_tests = TestLoader().loadTestsFromTestCase(
    TestGetAttribute
)
get_list_tests = TestLoader().loadTestsFromTestCase(
    TestGetList
)

suite = TestSuite([constraint_tests, and_tests, or_tests, set_tests,
                   equals_tests, exist_tests, in_tests, not_tests, type_tests,
                   filter_attribute_tests, filter_type_tests, get_attribute_tests, get_list_tests])

runner = HTMLTestRunner(
    report_title="IFC Data Checker Unit Testing",
    combine_reports=True,
    add_timestamp=False,
    report_name="IFCDataCheckerUnitTestsResults")

runner.run(suite)
