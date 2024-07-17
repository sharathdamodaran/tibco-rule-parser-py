from typing import Dict, List
from .Node import Node

class Relationship:
    def __init__(self, id:str, labels:List[str], start:Node, end:Node, properties:Dict[str,object]):
        self.id = id
        self.labels = labels if labels is not None else []
        self.start = start
        self.end = end
        self.properties = properties if properties is not None else {}