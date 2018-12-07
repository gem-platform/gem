from os import environ
from glob import glob
from pathlib import Path
from importlib import import_module


def load_api(application, pattern="api/*.py"):
    # check for debug is set
    debug = environ.get("DEBUG", "false") == "true"

    # register blueprints
    api_modules = ["api." + Path(m).stem for m in glob(pattern)]

    # load all the API modules
    for module_name in api_modules:
        # skip debug module if no DEBUG variable set
        if module_name == "api.debug" and not debug:
            continue

        # import module
        module = import_module(module_name)
        var = getattr(module, "API")

        # module should provide API var
        if var is None:
            raise Exception("No API variable provided for module " + module_name)

        # register blueprint
        application.register_blueprint(var)
