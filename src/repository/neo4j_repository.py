from neo4j import GraphDatabase
from typing import List

class Neo4jRepository:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def create_node(self, node):
        node_query = f"MERGE (n:{':'.join(node.labels)} {{id: $id }}) SET n += $properties RETURN n"
        self.session.run(node_query, id=node.id, properties=node.properties)

    def create_relationship(self, relationship):
        relationship_query = f"MATCH (a:Node {{id: $startId}}), (b:Node {{id: $endId}}) " \
                             f"CREATE (a)-[r:{':'.join(relationship.labels)} {{id: $relationshipId}}]->(b) " \
                             f"SET r += $properties RETURN r"
        self.session.run(relationship_query, startId=relationship.start.id, endId=relationship.end.id,
                         relationshipId=relationship.id, properties=relationship.properties)

    def get_root_node(self):
        root_query = "MATCH (n) WHERE NOT EXISTS( (n)<-[:Relationship]-() ) Return n.id as id"
        return self.session.run(root_query).single()["id"]

    def get_node(self, id):
        query = "MATCH (n:Node) WHERE n.id = $id RETURN n"
        return self.session.run(query, id=id).single()

    def get_child_node(self, id):
        records = []
        query = "MATCH (n:Node)-[r:Relationship]->(c:Node) WHERE n.id = $id RETURN c"
        result = self.session.run(query, id=id)
        for record in result:
            records.append(record)
        return records

    def update_root_node_level(self, rootId):
        update_level_query = "MATCH (n:Node {id: $rootId}) SET n.level = 0 RETURN n"
        self.session.run(update_level_query, rootId=rootId)

    def update_child_node_levels(self, rootId):
        query = "MATCH path=(n:Node{id:$rootId})-[r*]->(child) RETURN child.id as id,length(path) AS level"
        result = self.session.run(query, rootId=rootId)
        for record in result:
            update_level_query = "MATCH (n:Node {id: $id}) SET n.level = $level RETURN n"
            self.session.run(update_level_query, id=record["id"], level=record["level"])

    def update_property(self, id, name, value):
        update_level_query = f"MATCH (n:Node {{id: $id}}) SET n.{name} = $value RETURN n"
        self.session.run(update_level_query, id=id, value=value)

    def get_max_level(self):
        query = "MATCH (n:Node) RETURN max(n.level) as maxLevel"
        return self.session.run(query).single()["maxLevel"]

    def get_nodes_at_level(self, level):
        query = "MATCH (n:Node) WHERE n.level = $level RETURN n.id as id"
        result = self.session.run(query, level=level)
        nodes = []
        for record in result:
            nodes.append(record["id"])
        return nodes

    def close(self):
        self.session.close()
        self.driver.close()