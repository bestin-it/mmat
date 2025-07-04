# mmat/graph/models.py

from typing import Dict, Any, List, Optional

class VisualRef:
    """
    Represents a visual-only reference to an element on the page.
    Used when a standard DOM selector is not available.
    """
    def __init__(self, bbox: Dict[str, int], ocr_text: Optional[str] = None, description: Optional[str] = None):
        """
        Initializes a VisualRef.

        Args:
            bbox: Bounding box coordinates {x, y, width, height}.
            ocr_text: Text recognized by OCR within the bounding box.
            description: A human-readable description of the element.
        """
        self.bbox = bbox
        self.ocr_text = ocr_text
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bbox": self.bbox,
            "ocr_text": self.ocr_text,
            "description": self.description
        }

class GraphNode:
    """
    Represents a node in the test execution graph.
    Can be a DOM element, Action, State, Screenshot, or VisualRef.
    """
    def __init__(self, node_id: str, node_type: str, data: Dict[str, Any]):
        """
        Initializes a GraphNode.

        Args:
            node_id: Unique identifier for the node.
            node_type: Type of the node (e.g., "dom_element", "action", "state", "screenshot", "visual_ref").
            data: Dictionary containing node-specific data.
        """
        self.node_id = node_id
        self.node_type = node_type
        self.data = data
        self.visual_ref: Optional[VisualRef] = None # For visual_ref type nodes

        if node_type == "visual_ref" and "visual_ref" in data:
             self.visual_ref = VisualRef(**data["visual_ref"])


    def to_dict(self) -> Dict[str, Any]:
        data_dict = self.data.copy()
        if self.visual_ref:
            data_dict["visual_ref"] = self.visual_ref.to_dict()

        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "data": data_dict
        }


class GraphEdge:
    """
    Represents an edge in the test execution graph.
    Connects two nodes and represents a relationship or result.
    """
    def __init__(self, source_node_id: str, target_node_id: str, edge_type: str, data: Dict[str, Any]):
        """
        Initializes a GraphEdge.

        Args:
            source_node_id: ID of the source node.
            target_node_id: ID of the target node.
            edge_type: Type of the edge (e.g., "relation", "result").
            data: Dictionary containing edge-specific data (e.g., "click", "fill", "leads to").
        """
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id
        self.edge_type = edge_type
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "edge_type": self.edge_type,
            "data": self.data
        }

class ExecutionGraph:
    """
    Represents the test execution graph.
    Contains nodes and edges defining the test flow and relationships.
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    def add_node(self, node: GraphNode):
        if node.node_id in self.nodes:
            # Handle potential duplicates or updates
            pass # For now, simple add
        self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge):
        self.edges.append(edge)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionGraph":
        graph = cls()
        for node_data in data.get("nodes", []):
            graph.add_node(GraphNode(**node_data))
        for edge_data in data.get("edges", []):
            graph.add_edge(GraphEdge(**edge_data))
        return graph
