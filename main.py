import json
import os
from typing import Any
from typing import Dict
from typing import List

import yaml
from actions_toolkit import core as actions_toolkit
from cookiecutter.main import cookiecutter


INPUT_VALUES = {
    "acceptHooks": {"default": "true", "required": False},
    "cookiecutterValues": {"default": "{}", "required": False},
    "outputDir": {"default": ".", "required": False},
    "overwrite": {"default": "false", "required": False},
    "skip": {"default": "false", "required": False},
    "template": {"required": True},
    "templateCheckout": {"required": False},
    "templateDirectory": {"required": False},
    "zipPassword": {"required": False},
}


def get_inputs() -> Dict[str, Any]:
    """Get inputs from our workflow, valudate them, and return as a dict

    Reads inputs from actions.yaml. Non required inputs that are not set are returned as None
    Returns:
        Dict[str, Any]: [description]
    """
    parsed_inputs = dict()

    for input_name, input_config in INPUT_VALUES.items():
        this_input_value = actions_toolkit.get_input(input_name, required=input_config["required"])
        parsed_inputs[input_name] = this_input_value if this_input_value != "" else None

    # parse the cookiecutterValues into a dict
    try:
        actions_toolkit.debug(f"cookiecutterValues Json String: {parsed_inputs['cookiecutterValues']}")
        parsed_inputs["cookiecutterValues"] = json.loads(parsed_inputs["cookiecutterValues"])
    except json.decoder.JSONDecodeError as jsonerror:
        actions_toolkit.set_failed(f"Json error in cookiecutterValues {jsonerror}")
    except Exception as exc:  # this should be tigther
        actions_toolkit.set_failed(exc)

    try:
        actions_toolkit.debug(f"Listing template directory {os.listdir(parsed_inputs['template'])}")
    except Exception as exc:
        actions_toolkit.debug(f"Not listing template directory due to {exc}")
    return parsed_inputs


def str_to_bool(string: str) -> bool:
    """Will lowercase a passed in string and return if the string is in the set
    {true, t, yes, y}
    """
    return string.lower() in {"true", "t", "yes", "y"}


def main():
    inputs = get_inputs()

    # translate our friendly action input names into cookiecutter kw arguments
    inputs["extra_context"] = inputs.pop("cookiecutterValues")
    inputs["checkout"] = inputs.pop("templateCheckout")
    inputs["directory"] = inputs.pop("templateDirectory")
    inputs["output_dir"] = inputs.pop("outputDir")
    inputs["overwrite_if_exists"] = inputs.pop("overwrite")
    inputs["skip_if_file_exists"] = inputs.pop("skip")
    inputs["skip_if_file_exists"] = (
        str_to_bool(inputs["overwrite_if_exists"]) if inputs["overwrite_if_exists"] is not None else None
    )
    inputs["skip_if_file_exists"] = (
        str_to_bool(inputs["overwrite_if_exists"]) if inputs["overwrite_if_exists"] is not None else None
    )
    inputs["password"] = inputs.pop("zipPassword")
    inputs["accept_hooks"] = inputs.pop("acceptHooks")

    # set our hardcoded defaults
    inputs["no_input"] = True

    # strip out any optional inputs that weren't set
    set_inputs = dict(filter(lambda item: item[1] is not None, inputs.items()))
    print(set_inputs)
    try:
        output_dir = cookiecutter(**set_inputs)
    except Exception as exc:
        actions_toolkit.set_failed(exc)

    actions_toolkit.debug(os.listdir(inputs["output_dir"]))
    actions_toolkit.debug(os.listdir(output_dir))
    actions_toolkit.set_output("outputDir", output_dir)


if __name__ == "__main__":
    main()
