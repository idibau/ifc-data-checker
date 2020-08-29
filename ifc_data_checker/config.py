"""Config interface of the IFC Data Checker"""
import importlib
from typing import Any, List

import os
import yaml

import ifc_data_checker

all_constraints = set()
all_path_operators = set()
all_constraint_checks = set()

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def init():
    """Init"""
    with open(os.path.join(__location__, 'config.yml')) as config_file:
        config = yaml.safe_load(config_file)
        if not all_constraints:
            module = importlib.import_module('ifc_data_checker.constraints')
            for config_constraint in config['constraints']:
                all_constraints.add(
                    getattr(module, config_constraint))
        if not all_path_operators:
            module = importlib.import_module('ifc_data_checker.path_operators')
            for config_path_operator in config['path_operators']:
                all_path_operators.add(
                    getattr(module, config_path_operator))
        if not all_constraint_checks:
            module = importlib.import_module('ifc_data_checker.constraint_checks')
            for config_constraint_check in config['constraint_checks']:
                all_constraint_checks.add(
                    getattr(module, config_constraint_check))


init()


def get_constraint(constraint_definition: dict,
                   ifc_instance) -> ifc_data_checker.constraints.ConstraintComponent:
    """Gets the constraint component by the given definition"""
    keys = tuple(constraint_definition.keys())
    for component in all_constraints:
        if component.matching_yaml_keys(keys):
            return component(constraint_definition, ifc_instance)
    raise ValueError(f"No appropriate constraint component with keys {keys}")


def get_path_operator(path_operator_definition: dict,
                      actual_position: List[Any]) -> ifc_data_checker.path_operators.PathOperator:
    """Gets the constraint component by the given definition"""
    keys = tuple(path_operator_definition.keys())
    for path_operator in all_path_operators:
        if path_operator.matching_yaml_keys(keys):
            return path_operator(actual_position, path_operator_definition)
    raise ValueError(f"No appropriate path operator with keys {keys}")


def get_constraint_check(constraint_check_definition: dict, path_result,
                         ifc_instance) -> ifc_data_checker.constraint_checks.ConstraintCheck:
    """Gets the constraint component by the given definition"""
    keys = tuple(constraint_check_definition.keys())
    for check in all_constraint_checks:
        if check.matching_yaml_keys(keys):
            return check(constraint_check_definition, path_result, ifc_instance)
    raise ValueError(f"No appropriate constraint check with keys {keys}")
