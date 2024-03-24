import json
from datetime import datetime
from typing import Dict, Any, Set, List


class GraphElement:
    """
    Base class for graph elements (nodes and relationships) with common functionalities.
    """

    def __init__(self, properties: Dict[str, Any], labels: List = [], key="Name"):
        if "Name" not in properties:
            raise ValueError("All elements must include a name")
        if key not in properties:
            raise ValueError(f"Missing key: '{key}'")

        self._labels = set(labels)
        self._key = key

        self._properties = properties

    @staticmethod
    def serialize_properties(properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Serialize properties to ensure they are compatible with Neo4j.
        """
        # Implementation of serialization logic (e.g., converting datetime to string)

        _properties = {}

        for k, v in properties.items():

            if any([isinstance(v, t) for t in [datetime, dict, list, int]]):
                _properties[k] = v
                continue

            elif type(v) is None:
                _properties[k] = ""
                continue

            try:
                _properties[k] = json.loads(v)
                continue
            except json.decoder.JSONDecodeError:
                pass

            try:
                _properties[k] = datetime.strptime(v[:-6], "%Y-%m-%d %H:%M:%S")
                continue
            except ValueError:
                pass

            _properties[k] = str(v)
        return _properties

    def properties(self):
        return self.serialize_properties(self._properties)

    def label(self):
        return [*[l for l in self.labels() if l != self.__class__.__name__], ""][0]

    def labels(self):
        return sorted(list(self._labels))

    def type(self, label):
        return label in self._labels

    def id(self):
        return self._properties[self._key]

    def get(self, k):
        return self._properties[k]

    def set(self, k, v):
        self._properties[k] = v

    def __hash__(self):
        return hash(self.id())

    def __eq__(self, other):
        if isinstance(other, str):
            return other in self.labels()
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__()

    def __repr__(self):
        return self.id()

    def __str__(self):
        return str(self.id())


class Node(GraphElement):
    """
    Base class for all nodes, designed to use a resource's ARN as the node ID.
    """

    def __init__(self, labels: Set[str], properties: Dict[str, Any]):
        super().__init__(properties)
        self._labels = labels
        # Ensure an ARN is provided and valid
        if "Arn" not in properties or not self._is_valid_arn(properties["Arn"]):
            raise ValueError("Invalid or missing ARN in properties")
        # Use ARN as the node's unique identifier
        self._key = "Arn"

    def _is_valid_arn(self, arn: str) -> bool:
        """Checks if the provided ARN is valid."""
        # This is a simple validation; consider enhancing it based on actual ARN formatting rules
        return arn.startswith("arn:aws:") and len(arn.split(":")) >= 6

    def save(self, tx):
        """Save the node to the database using a transaction."""
        label_str = ":".join(self._labels)
        cypher_query = f"MERGE (n:{label_str}) SET n += $properties RETURN n"
        tx.run(cypher_query, properties=self._properties)


class Relationship(GraphElement):
    """Base class for all relationships"""

    def __init__(self, properties: Dict[str, Any], source: str, target: str):
        if labels is None:
            labels = [str(self.__class__.__name__).upper()]

        super().__init__(properties, labels)

        self._source = source
        self._target = target
        self._set_id()

    def save(self, tx):
        # Example Cypher query to create the relationship
        query = (
            "MATCH (source), (target) "
            "WHERE source.id = $source AND target.id = $target "
            "CREATE (source)-[r:{self._type}]->(target) "
            "SET r += $properties RETURN r"
        )
        tx.run(
            query,
            source=self.source(),
            target=self.target(),
            properties=self.properties(),
        )

    def _set_id(self):

        self._id = hash(
            "({source})-[:{label}{{{properties}}}]->({target})".format(
                source=self.source(),
                label=self.labels()[0],
                properties=json.dumps(self.properties(), sort_keys=True),
                target=self.target(),
            )
        )

    def source(self):
        return self._source

    def target(self):
        return self._target

    def id(self):
        return self._id

    def modify(self, k, v):
        super().set(k, v)
        self._set_id()

    def __str__(self):
        return str(self.get("Name"))
