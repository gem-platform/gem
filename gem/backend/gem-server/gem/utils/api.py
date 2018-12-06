from glob import glob
from pathlib import Path
from importlib import import_module


def load_api(application, pattern="api/*.py"):
    # register blueprints
    api_modules = ["api." + Path(m).stem for m in glob(pattern)]

    # load all the API modules
    for module_name in api_modules:
        module = import_module(module_name)
        var = getattr(module, "API")
        application.register_blueprint(var)
