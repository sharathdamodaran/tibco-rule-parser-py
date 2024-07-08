from typing import Dict, List

class Node:
    def __init__(self, id: str, labels: List[str], properties: Dict[str, object]):
        self.id = id
        self.labels = labels if labels is not None else []
        self.properties = properties if properties is not None else {}