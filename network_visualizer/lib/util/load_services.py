from pathlib import Path
import importlib.util
from network_visualizer.lib.classes.service_base import ServiceBase


def load_services(session_manager):
    """
    Dynamically load and instantiate service classes.

    Loads all service classes from the services directory and instantiates them.
    It returns all subclasses of ServiceBase as a dictionary with the class name as the key.

    """
    service_dir = Path(__file__).parent.parent / "services"
    # Import all service modules
    for file in service_dir.iterdir():
        if file.name.endswith(".py") and file.is_file():
            module_name = file.stem  # Get the file name without '.py'
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
    # Instantiate service classes
    services = {
        cls.__name__.lower(): cls(session_manager)
        for cls in ServiceBase.__subclasses__()
    }
    return services
