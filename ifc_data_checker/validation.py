"""Validation"""
from enum import Enum


class ValidationResult(Enum):
    """Validation Result"""

    NOT_EVALUATED = 0
    ERROR = 1
    FAILED = 2
    VALID = 3


class ValidationInformation():
    """Validation information of a check"""

    def __init__(self):
        """Constructor

        Default `validation_result` is `ValidationResult.NOT_EVALUATED`
        """
        self.validation_result = ValidationResult.NOT_EVALUATED
        self.message = None

    def set_error(self, message: str):
        """Sets the validation result to error including the message"""
        self.validation_result = ValidationResult.ERROR
        self.message = message

    def set_failed(self, message: str):
        """Sets the validation result to failed including the message"""
        self.validation_result = ValidationResult.FAILED
        self.message = message

    def set_valid(self, message: str):
        """Sets the validation result to valid including the message"""
        self.validation_result = ValidationResult.VALID
        self.message = message

    def __eq__(self, other):
        """Equals the self object on the other by their attributes"""
        if not isinstance(other, ValidationInformation):
            return False
        return (self.validation_result == other.validation_result and
                self.message == other.message)

    def __bool__(self):
        """Check ValidationInformation is VALID means True, Otherwise False"""
        return self.validation_result == ValidationResult.VALID

    def __str__(self):
        """To Str"""
        return self.message
