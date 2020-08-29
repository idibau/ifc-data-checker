"""Report the validation results"""
from typing import List
from os import path

from ifc_data_checker.rules import Rule


def _create_report(validated_rules: List[Rule]) -> List[str]:
    """Creates the report on the given validated rules

        Args:
            validated_rules (List[Rule]):
                The rules to report

        Returns:
            List[str]:
                The report of the rules as List of lines
    """
    report = []
    for validated_rule in validated_rules:
        report.append(validated_rule.report())
    return report


def create_validation_report_console(validated_rules: List[Rule],
                                     rules_file: str, ifc_file: str):
    """Create a validation report on the console.

        Args:
            validated_rules (List[Rule]):
                The validated rules from the validations
            rules_file (str):
                The file path of the rules file.
            ifc_file (str):
                The file path of the ifc file.
    """
    rules_file_name = path.basename(rules_file)
    ifc_file_name = path.basename(ifc_file)
    print(f"validation report {rules_file_name} {ifc_file_name}")
    reported_rules = _create_report(validated_rules)
    for rule in reported_rules:
        print(*rule, sep="\n")


def create_validation_report_file(validated_rules: List[Rule],
                                  rules_file: str, ifc_file: str):
    """Creates a validation report file.

        If the validation report file already exists, then it will be overridden.

        Args:
            validated_rules (List[Rule]):
                The validated rules from the validations
            rules_file (str):
                The file path of the rules file.
            ifc_file (str):
                The file path of the ifc file.
    """
    rules_file_name = path.basename(rules_file)
    ifc_file_name = path.basename(ifc_file)
    validation_report_file_name = f"validation report {rules_file_name} {ifc_file_name}.txt"
    with open(validation_report_file_name, 'w+') as validation_report_file:
        validation_report_file.write(
            f"validation report {rules_file_name} {ifc_file_name}\n")
        report_lines = _create_report(validated_rules)
        for rule in report_lines:
            validation_report_file.write('\n'.join(rule) + '\n')
