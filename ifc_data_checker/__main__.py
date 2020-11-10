"""init ifc_data_checker"""
import argparse
import json
import jsonschema
import yaml

from ifc_data_checker import rules
from ifc_data_checker import report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ifc_data_checker')
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
    checker.check(args.rules, args.ifc, args.report_file,
                  args.no_rulesfile_validation)


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


def check(rules_file, ifc_file, report_file, no_rulesfile_validation):
    """execute ifc data checker"""
    if report_file:
        report_strategy = report.create_validation_report_file
    else:
        report_strategy = report.create_validation_report_console

    rules_json = get_json_rules(rules_file)
    if not no_rulesfile_validation:
        rules_schema = get_json_rules_schema("rules.schema.json")
        jsonschema.validate(instance=rules_json, schema=rules_schema)

    validated_rules = rules.validate(rules_json["rules"], ifc_file)
    report_strategy(validated_rules, rules_file, ifc_file)
