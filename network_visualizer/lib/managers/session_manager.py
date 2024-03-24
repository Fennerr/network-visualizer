import boto3
from botocore.config import Config
from botocore.exceptions import NoRegionError


from network_visualizer.lib.config import boto_config
from network_visualizer.lib.logger import logger


class SessionManager:
    config: Config = None
    session: boto3.Session = None
    profile_name: str = None
    region_name: str = None
    default_region: str = "eu-west-1"

    def __init__(self, profile_name=None, region_name=None):
        self.profile_name = profile_name
        self.region_name = region_name
        self.config = boto_config
        self.session = self.create_session()
        self.logger = logger

    def set_region(self, region_name):
        self.region_name = region_name
        self.session = self.create_session()

    def create_session(self):
        session = boto3.Session(
            profile_name=self.profile_name, region_name=self.region_name
        )
        return session

    def create_client(self, service_name: str):
        try:
            client = self.session.client(service_name, config=self.config)
        except NoRegionError:
            # Use the session with the default region
            return self.session.client(
                service_name, region_name=self.default_region, config=self.config
            )
        return client

    def generate_regional_clients(self, service: str) -> dict:
        try:
            # Not all services support the get_available_regions call
            regions = self.session.get_available_regions(service)
        except Exception as e:
            # Will need a way to handle this, but I dont think it should be an issue for the services we will be using for this tool.
            self.logger.error(f"Error getting regions for service {service}: {e}")
            self.logger.error(f"Error getting regions for service {service}: {e}")

        regional_clients = {}

        for region in regions:
            regional_client = self.session.client(service, region_name=region)
            regional_client.region = region
            regional_clients[region] = regional_client

        return regional_clients
