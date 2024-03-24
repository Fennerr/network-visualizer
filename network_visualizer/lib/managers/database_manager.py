from neo4j import GraphDatabase
from network_visualizer.lib.graph.base import Node, Relationship


class DatabaseManager:
    """Class for managing the Neo4j database connection and operations."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        """Ensure the Neo4j database connection is closed when the instance is garbage collected."""
        self.close()

    def close(self):
        """Close the Neo4j database connection."""
        if self.driver is not None:
            self.driver.close()

    def add_node(self, node: Node):
        """Add a node to the database."""
        with self.driver.session() as session:
            session.write_transaction(self._add_node_tx, node)

    @staticmethod
    def _add_node_tx(tx, node: Node):
        """Transaction function for adding a node."""
        labels_str = ":".join(node.labels())
        properties_str = ", ".join(
            [f"{key}: ${key}" for key in node.properties().keys()]
        )
        cypher_query = f"MERGE (n:{labels_str}) SET n += $properties RETURN n"
        tx.run(cypher_query, properties=node.properties())

    def add_relationship(self, relationship: Relationship):
        """Add a relationship to the database."""
        with self.driver.session() as session:
            session.write_transaction(self._add_relationship_tx, relationship)

    @staticmethod
    def _add_relationship_tx(tx, relationship: Relationship):
        """Transaction function for adding a relationship."""
        query = (
            "MATCH (source), (target) "
            "WHERE source.Arn = $source AND target.Arn = $target "
            "CREATE (source)-[r:{type}]->(target) "
            "SET r += $properties RETURN id(r)"
        )
        tx.run(
            query,
            source=relationship.source(),
            target=relationship.target(),
            type=relationship.labels()[0],
            properties=relationship.properties(),
        )
