from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

from network_visualizer.lib.logger import logger

MAX_WORKERS = 10


def generate_regional_clients(session, service):
    try:
        # Not all services support the get_available_regions call
        regions = session.get_available_regions(service)
    except Exception as e:
        # Will need a way to handle this, but I dont think it should be an issue for the services we will be using for this tool.
        print(f"Error getting regions for service {service}: {e}")

    regional_clients = {}

    for region in regions:
        regional_client = session.client(service, region_name=region)
        regional_client.region = region
        regional_clients[region] = regional_client

    return regional_clients


class ServiceBase(ABC):
    def __init__(
        self, service: str, session: boto3.session, global_service: bool
    ) -> None:
        super().__init__()
        self.session = session
        self.service = service.lower() if not service.islower() else service
        # Generate Regional Clients for the threading_call function to use
        if not global_service:
            self.regional_clients = generate_regional_clients(session, self.service)

        self.client = self.session.client(self.service)

        # Thread pool for __threading_call__
        self.thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @abstractmethod
    def run(self, args):
        """
        Execute the service.

        :param args: Command line arguments specific to the action
        """
        pass

    def __threading_call__(self, call, iterator=None):
        # Use the provided iterator, or default to self.regional_clients
        items = list()
        if iterator is not None:
            items = iterator
        elif hasattr(self, "regional_clients"):
            items = self.regional_clients
        else:
            raise ValueError(
                "No iterator provided and no regional_clients attribute found."
            )

        # Determine the total count for logging
        item_count = len(items)

        # Trim leading and trailing underscores from the call's name
        call_name = call.__name__.strip("_")
        # Add Capitalization
        call_name = " ".join([x.capitalize() for x in call_name.split("_")])

        # Print a message based on the call's name, and if its regional or processing a list of items
        if iterator is None:
            logger.info(
                f"{self.service.upper()} - Starting threads for '{call_name}' function across {item_count} regions..."
            )
        else:
            logger.info(
                f"{self.service.upper()} - Starting threads for '{call_name}' function to process {item_count} items..."
            )

        # Submit tasks to the thread pool
        futures = [self.thread_pool.submit(call, item) for item in items]

        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()  # Raises exceptions from the thread, if any
            except Exception:
                # Handle exceptions if necessary
                pass  # Replace 'pass' with any additional exception handling logic. Currently handled within the called function
