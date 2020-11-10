"""init ifc_data_checker"""

import argparse

from ifc_data_checker import checker

if __name__ == "__main__":
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
    checker.check(args.rules, args.ifc, args.report_file,
                  args.no_rulesfile_validation)
