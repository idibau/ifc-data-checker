"""Helpers for testing"""


class MicroMock:
    """Micro Mock for testing"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_attribute(self, attribute_name):
        """Gets the attribute by name"""
        return self.__dict__[attribute_name]

    def set_attribute(self, **kwargs):
        """Sets the attribute name and value"""
        self.__dict__.update(kwargs)


class IfcInstanceMock(MicroMock):
    """IFC Instance Micro Mock

    Use `**kwargs` of constructor like `ifc_type="IfcMock"`
    """

    def is_a(self, comparing_type=None):
        """Checks wheter the given type is the same type as the IFC mock"""
        if comparing_type is None:
            return self.__dict__["ifc_type"]
        return self.__dict__["ifc_type"] == comparing_type
