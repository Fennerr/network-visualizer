from network_visualizer.lib.classes import ServiceBase
from network_visualizer.lib.managers import SessionManager
from network_visualizer.lib.graph.base import Node


class EC2Node(Node):
    """Node class for EC2s"""

    pass


class EC2(ServiceBase):
    session_manager: SessionManager = None

    def __init__(self, session_manager: SessionManager):
        super().__init__(
            service="ec2", global_service="False", session_manager=session_manager
        )

    def run(self, args):
        pass
