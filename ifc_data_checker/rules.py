"""Read the rules file and the get the instances from the ifc file"""
from typing import List

import ifcopenshell

from ifc_data_checker import config
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult


class Rule:
    """Rule"""

    def __init__(self, rule_definition: dict, ifc_instances: tuple):
        """Constructor"""
        self.rule_definition = rule_definition
        self.ifc_instances = ifc_instances
        self.validation = []
        self.validation_information = ValidationInformation()

    def validate(self):
        """Validates a rule on the ifc instances"""
        for ifc_instance in self.ifc_instances:
            validated_constraints = []
            valid_constraint_components_count = 0
            for constraint_component_definition in self.get_constraints():
                constraint_component = config.get_constraint(
                    constraint_component_definition, ifc_instance)
                constraint_component.validate()
                if constraint_component.is_valid():
                    valid_constraint_components_count += 1
                validated_constraints.append(constraint_component)
            instance_validation_result = ValidationInformation()
            if valid_constraint_components_count == len(validated_constraints):
                instance_validation_result.set_valid((
                    f"{ifc_instance.is_a()} "
                    f"{ifc_instance.Name} "
                    f"Global Id: {ifc_instance.GlobalId}: "
                    f"{len(validated_constraints)} of "
                    f"{len(validated_constraints)} constraints "
                    f"are valid."
                ))
            else:
                instance_validation_result.set_failed((
                    f"{ifc_instance.is_a()} "
                    f"{ifc_instance.Name} "
                    f"Global Id: {ifc_instance.GlobalId}: "
                    f"{valid_constraint_components_count} of "
                    f"{len(validated_constraints)} constraints "
                    f"are valid."
                ))
            self.validation.append(
                {
                    'ifc_instance': ifc_instance,
                    'validated_constraints': validated_constraints,
                    'validation_information': instance_validation_result
                })
        valid_instances = [
            v for v in self.validation
            if v['validation_information'].validation_result == ValidationResult.VALID
        ]
        if len(valid_instances) == len(self.validation):
            self.validation_information.set_valid((
                f"Rule: {len(self.validation)} of {len(self.validation)} "
                f"instances of types {self.get_classes()} successfully validated."
            ))
        else:
            self.validation_information.set_failed((
                f"Rule: {len(valid_instances)} of {len(self.validation)} "
                f"instances of types {self.get_classes()} successfully validated."
            ))

    def report(self) -> List[str]:
        """Reports the rule"""
        report = []
        report.append(str(self.validation_information))
        for instance_validation in self.validation:
            report.append("")
            report.append(str(instance_validation['validation_information']))
            for validated_constraint in instance_validation['validated_constraints']:
                report += validated_constraint.report()
        return report

    def get_classes(self):
        """Gets the ifc classes"""
        return self.rule_definition["classes"]

    def get_constraints(self):
        """Gets the constraints"""
        return self.rule_definition["constraints"]


def get_instances(ifc_classes: List[str], ifc_model) -> tuple:
    """Gets the instances by their `ifc_classes` of the given `ifc_model`

        Args:
            ifc_classes (List[str]):
                The defined ifc classes of the rule definition.
            ifc_model:
                The model to get the ifc instances by ifc class.

        Returns:
            tuple:
                The ifc instances with appropriate ifc classes in the ifc model.
    """
    ifc_instances = []
    for ifc_class in ifc_classes:
        ifc_instances += ifc_model.by_type(ifc_class)
    return tuple(ifc_instances)


def get_rule(rule_definition: dict, ifc_model) -> Rule:
    """Gets the rule object by their rule definition.

        Args:
            rule_definition (dict):
                The rule defintion from the rules file.
            ifc_model:
                The ifc model to validate the rule.

        Returns:
            Rule:
                The Rule object ready to validate.
    """
    ifc_instances = get_instances(
        rule_definition["rule"]["classes"], ifc_model)
    return Rule(rule_definition["rule"], ifc_instances)


def validate(rules_definition: List[dict], ifc_file: str) -> List[Rule]:
    """Valdiates the rules definied in the rules file on the given ifc file.

    Args:
        rules_definition (list):
            The definition of all rules from the rules file.
        ifc_file (str):
            The ifc file path.

    Returns:
        List[Rule]:
            List of validated rules.
    """
    ifc_model = ifcopenshell.open(ifc_file)
    rules = []
    for rule_definition in rules_definition:
        rule = get_rule(rule_definition, ifc_model)
        rule.validate()
        rules.append(rule)
    return rules
