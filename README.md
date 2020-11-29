# IFC Data Checker

IFC Data Checker is a tool to validate rules on IFC models. To do so, the IFC Data Checker needs a rules file and an IFC model. The rules file has to match the rules specification in the report of the bachelor thesis of the IFC Data Checker. The IFC model need to be of version 2x3 or version 4.

Clone this repository and install the dependencies:

```shell
pip install ifc-data-checker
```

## IfcOpenShell Python

To run the IFC Data Checker, IfcOpenShell need to fit your machine environment regarding:

* the Python version
* the os (Windows, Linux , Mac)
* the os flavor (32bit or 64bit)

To run the IFC Data Checker, you need to do the following steps:

1. Go to [ifcopenshell.org/python](http://ifcopenshell.org/python) and download the matching IfcOpenShell. Use the latest IfcOpenShell version.
2. Extract the downloaded file and paste the `ifcopenshell` folder to the directory `site-packages` of the python installation. The folder need to be called `ifcopenshell`.
    * On Linux e.g. `/usr/local/lib/python3.8/site-packages/`
    * On Windows e.g. in the python installation folder and then `\Lib\site-packages\`

If IfcOpenShell not matching your machine environment, then it will trow an exception like:

```python
ImportError: IfcOpenShell not built for 'windows\64bit\python3.8'
```

Run the IFC Data Checker with:

```shell
python ifc_data_checker ./path/to/rules-file.yml ./path/to/ifc-model.ifc
```

GitHub Repository example:

```shell
python ifc_data_checker "./rulesfiles/PredefinedType for IfcWall.yml" "./ifcfiles/Duplex-A.ifc"
```

Usage:

```shell
usage: ifc_data_checker [-h] [--report-file] [--no-rulesfile-validation] rules ifc

positional arguments:
  rules                 The path to the rules file.
  ifc                   The path to the ifc file.

optional arguments:
  -h, --help            show this help message and exit
  --report-file         Create a validation report file, instead of showing the validation report on the console.
  --no-rulesfile-validation
                        Disable validation of the rules file.
```

## Contribute

You are invited to participate on the IFC Data Checker.

### Python Style Guide

The IFC Data Checker follows the [Python Style Guide from Google](https://google.github.io/styleguide/pyguide.html)

The source code documentation follows the Google Style. [This example](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) helps to follow the Google Style.

## Extend Constraint Component

The following 4 steps are to extend the IFC Data Checker for a new Constraint Component.

1. Step

    Add a new class in the Python module `ifc_data_checker/constraints.py`. Use the following template and consider the comments.

    ```python
    class NewConstraint(ConstraintComponent):
        """Class description"""
        yaml_keys = tuple(["new"])
        """Set the yaml keys for the new constraint"""

        def __init__(self, definition: dict, ifc_instance):
            """Constructor"""
            super().__init__(definition, ifc_instance)
            self.potentially_new_attribute = None

        def validate(self):
            """Validates. The attribute self.validation_information need to be set."""

        def report(self) -> List[str]:
            """Reports. Return a list of valiation results messages"""
            return [str(self.validation_information)]

        def __eq__(self, other):
            """Equals all the attributes"""
            if not isinstance(other, NewConstraint):
                return False
            return (self.definition == other.definition and
                    self.ifc_instance == other.ifc_instance and
                    self.validation_information == other.validation_information and
                    self.potentially_new_attribute == other.potentially_new_attribute)
    ```

2. Step

    Add the Name of the class in the yaml file `ifc_data_checker/config.yml`.

    ```yaml
    constraints:
    - Constraint
    - SetGroup
    - AndGroup
    - OrGroup
    - NewConstraint
    ```

3. Step

    Write unit and integration tests for the new constraint component. To do so, add a new Python module under `tests/constraints`. This new test class should inherit from `tests.constraints.constraint_component_test.TestConstraintComponent.TestParameterValidation`. After that, set the attribute `constraint_component_class` and `default_constraint_component` on the new test class.

    Now you are ready to implement the test cases. You can have a look at the existing test cases and write the test cases analogously.

    The new Python test module should be in the test report. For that, add the Python test module in the Python module `tests/suite.py` analogously as the others.

4. Step

    The new constraint component need to add to the `rules.schema.json`, to be an accepted constraint component. To do so add the JSON schema of the new constraint component in the JSON schema file `rules.schema.json` under definitions -> constraint -> oneOf. Read the [JSON schema](http://json-schema.org/) specification to create an JSON Schema. Here is an example.

    ```json
    "definitions": {
    "constraint": {
      "oneOf": [
        …
        {
          "type": "object",
          "properties": {
            "new": {
              "type": "string"
            }
          },
          "required": [
            "new"
          ],
          "additionalItems": false
        },
        …
    ```

To extend an new path operator or an new constraint check, the steps are analogously to the steps of the constraint component.
