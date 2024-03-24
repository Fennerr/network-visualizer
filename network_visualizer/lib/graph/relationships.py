from network_visualizer.lib.graph.base import Relationship


class ContainsRelationship(Relationship):
    """Relationship class for 'contains' relationship (e.g., VPC contains Subnets)"""

    pass


class AssociatedWith(Relationship):
    def __init__(self, source_id, target_id):
        super().__init__(
            type="ASSOCIATED_WITH",
            properties={},
            source_id=source_id,
            target_id=target_id,
        )


class AllowsTraffic(Relationship):
    def __init__(self, source_id, target_id, properties):
        super().__init__(
            type="ALLOWS_TRAFFIC",
            properties=properties,
            source_id=source_id,
            target_id=target_id,
        )
