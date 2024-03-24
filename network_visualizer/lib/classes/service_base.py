"""
This module defines a base class for AWS service interactions, supporting
both global services and those requiring regional clients, with concurrent execution
capabilities.

Classes:
    ServiceBase: An abstract base class designed to be extended by specific AWS service classes.
    It helps by handling setting the logger and boto session/client, and provides
    a method to perform concurrent execution of service actions across multiple regions or items.

The ServiceBase class utilizes a ThreadPoolExecutor for parallel execution of tasks,
which is particularly useful for actions that need to be performed across multiple AWS
regions. It requires subclasses to implement the `run` method, which defines the
service-specific action to be executed.

This module is designed to be used within the network_visualizer project, leveraging
the session management provided by the `SessionManager` class and utilizing the
project's logging setup.

Attributes:
    MAX_WORKERS (int): The maximum number of worker threads to use for concurrent
    execution of service actions.

Example:
    To use this module, extend the ServiceBase class and implement the `run` method
    with the logic specific to the AWS service you are interfacing with. Then, create
    an instance of your subclass, providing the necessary parameters, and call the
    `run` method with any required arguments.
"""

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from boto3 import Session
from network_visualizer.lib.logger import logger
from network_visualizer.lib.managers.session_manager import SessionManager

# TODO: Allow for this to be set via environment variable or config file
MAX_WORKERS = 10


class ServiceBase(ABC):
    """ """

    session_manager: SessionManager = None
    session: Session = None
    service: str = None
    client: object = None
    max_workers: int = MAX_WORKERS

    def __init__(
        self,
        service: str,
        session_manager: SessionManager,
        global_service: bool = False,
    ) -> None:
        super().__init__()
        self.session_manager = session_manager
        self.session = session_manager.session
        self.service = service.lower() if not service.islower() else service
        # Generate Regional Clients for the threading_call function to use
        if not global_service:
            self.regional_clients = session_manager.generate_regional_clients(
                service=self.service
            )

        self.client = session_manager.create_client(self.service)

        # Logger
        self.logger = logger

        # Thread pool for __threading_call__
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)

    @abstractmethod
    def run(self, args):
        """
        Execute the service.

        :param args: Command line arguments specific to the action
        """

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
