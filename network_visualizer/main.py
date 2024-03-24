from network_visualizer.lib.logger import logger
from network_visualizer.lib.managers import (
    ConfigurationManager,
    SessionManager,
    DatabaseManager,
)
from network_visualizer.lib.util import load_services


def network_visualizer_main():
    logger.debug("Starting network visualizer...")

    # First initialize the configuration manager
    # It will get the args and then be used to initialize the session manager and the database manager
    config_manager = ConfigurationManager()
    config = config_manager.get_configuration()

    session_manager = SessionManager(
        profile_name=config.get("aws_profile"), region_name=config.get("aws_region")
    )

    database_manager = DatabaseManager(
        uri=config.get("neo4j_uri"),
        user=config.get("neo4j_user"),
        password=config.get("neo4j_password"),
    )

    load_services.load_services(session_manager)
