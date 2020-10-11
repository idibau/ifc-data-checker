"""The IFC Data Checker"""
import argparse

import json
import jsonschema
import yaml

from ifc_data_checker import rules
from ifc_data_checker import report


def get_json_rules(rules_file: str):
    """Get the yaml by filename"""
    with open(rules_file) as yaml_file:
        return yaml.safe_load(yaml_file)


def get_json_rules_schema(rules_schema_file: str):
    """Get the rules schema by filename"""
    with open(rules_schema_file) as schema_file:
        return json.load(schema_file)


def print_help():
    """print usage help"""
    help_file = open("help.txt", "r")
    print(help_file.read())


def main():
    """execute ifc data checker"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "rules", help="The path to the rules file.")
    parser.add_argument(
        "ifc", help="The path to the ifc file.")
    parser.add_argument("--report-file", action="store_true",
                        help="Create a validation report file, "
                             "instead of showing the validation report on the console.")
    parser.add_argument("--no-rulesfile-validation", action="store_true",
                        help="Disable validation of the rules file.")

    args = parser.parse_args()
    rules_file = args.rules
    ifc_file = args.ifc
    if args.report_file:
        report_strategy = report.create_validation_report_file
    else:
        report_strategy = report.create_validation_report_console

    rules_json = get_json_rules(rules_file)
    if not args.no_rulesfile_validation:
        rules_schema = get_json_rules_schema("rules.schema.json")
        jsonschema.validate(instance=rules_json, schema=rules_schema)

    validated_rules = rules.validate(rules_json["rules"], ifc_file)
    report_strategy(validated_rules, rules_file, ifc_file)


if __name__ == "__main__":
    main()
