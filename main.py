import json
import os
from typing import Any

from actions_toolkit import core as actions_toolkit
from cookiecutter.main import cookiecutter


###START_INPUT_AUTOMATION###
INPUTS = {
    "cookiecutterValues": {
        "description": "Json blob to pass to the cookiecutter template. Any values not filled in will be set to template's default",
        "required": False,
        "default": "{}",
    },
    "template": {
        "description": "A directory containing a project template directory (or zip file), or a URL to a git repository.",
        "required": True,
    },
    "templateCheckout": {"description": "The branch, tag or commit ID to checkout after clone.", "required": False},
    "templateDirectory": {
        "description": "Relative path to a cookiecutter template in a repository.",
        "required": False,
    },
    "outputDir": {"description": "Where to output the generated project dir into.", "default": ".", "required": False},
    "overwrite": {
        "description": "Overwrite files if they already exist in outputDir if true",
        "required": False,
        "default": "false",
    },
    "skip": {
        "description": "Skip files if they already exist in outputDir if true",
        "required": False,
        "default": "false",
    },
    "zipPassword": {
        "description": "If your template zip is password protected, put your password here",
        "required": False,
    },
    "acceptHooks": {"description": "Accept pre and post hooks if set to true.", "required": False, "default": "true"},
}
###END_INPUT_AUTOMATION###


def get_inputs() -> dict[str, Any]:
    """Get inputs from our workflow, valudate them, and return as a dict

    Reads inputs from actions.yaml. Non required inputs that are not set are returned as None
    Returns:
        Dict[str, Any]: [description]
    """
    parsed_inputs = dict()

    for input_name, input_config in INPUTS.items():
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
    inputs["overwrite_if_exists"] = str_to_bool(inputs.pop("overwrite"))
    inputs["skip_if_file_exists"] = str_to_bool(inputs.pop("skip"))
    # set skip to false if overwrite is true
    inputs["skip_if_file_exists"] = (
        false if inputs["overwrite_if_exists"] else inputs["skip_if_file_exists"]
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
        actions_toolkit.debug(f"Encountered exception while running cookiecutter. {exc.__class__}: {str(exc)}")
        actions_toolkit.set_failed(exc)

    actions_toolkit.debug(os.listdir(inputs["output_dir"]))
    actions_toolkit.debug(os.listdir(output_dir))
    actions_toolkit.set_output("outputDir", output_dir)


if __name__ == "__main__":
    main()
