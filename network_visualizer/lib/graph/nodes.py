# For APIs that dont return the ARN, can add logic in here to generate the ARN
from network_visualizer.lib.graph.base import Node


class VPCNode(Node):
    """Node class for VPCs"""

    pass


class SubnetNode(Node):
    """Node class for Subnets"""

    pass


class ENINode(Node):
    def __init__(self, properties):
        super().__init__(labels={"ENI"}, properties=properties)


class SecurityGroupNode(Node):
    def __init__(self, properties):
        super().__init__(labels={"SecurityGroup"}, properties=properties)


class NetworkACLNode(Node):
    def __init__(self, properties):
        super().__init__(labels={"NetworkACL"}, properties=properties)
