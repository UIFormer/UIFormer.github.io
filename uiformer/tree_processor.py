from .element_utils import *
import xml.etree.ElementTree as ET
from itertools import combinations

class TreeProcessor:
    def __init__(self, uiformer):
        self.uiformer = uiformer

    def process_accessibility_tree(self, root):
        reduced_elements = []
        def transform_node(node, node_order="", dep=0):
            sequ_subtree = []
            # LEAF NODE HANDLING
            if len(node) == 0:
                # Phase 1: Filter unwanted leaf nodes
                if gettext(node) == "" and not is_crucial_node(node) and node.attrib.get("resource-id") == "":
                    return []
                # Phase 2: Handle leaf nodes
                else :
                    leaf_view = make_view(node)
                    leaf_view.update({"id": node_order})
                    sequ_subtree.append(leaf_view)
            
            # FILTER_CONDITIONS
            if "package" in node.attrib and node.attrib["package"].startswith("com.android.systemui"):
                return []
            if "resource-id" in node.attrib and node.attrib["resource-id"].startswith("com.google.android.inputmethod.latin:id"):
                return []

            for id, child in enumerate(node):
                sub = transform_node(child, node_order + f"{id},", dep + 1)
                for view in sub:
                    sequ_subtree.append(view)

            # Phase 3: Make merge decision
            if is_crucial_node(node) and len(sequ_subtree) > 0 and not self._main_view(node):
                node_view = make_element("", "", node, sequ_subtree)
                node_view.update({"id": node_order})
                reduced_elements.append(node_view)
                sequ_subtree = []

            return sequ_subtree

        transform_node(root)
        return reduced_elements

    def parameterize_actions(self, root, elements):   
        output = []
        action_nodes = {el["id"]:idx for idx, el in enumerate(elements)}
        
        target_elements = elements
        def dfs1(node, node_order=""):
            if illegal_node(node):
                return 
            
            if node_order in action_nodes:
                return 
            
            if not gettext(node) == ("", ""):
                node_view = {"id": node_order}
                target_elements.append(node_view)
                
            for id, child in enumerate(node):
                dfs1(child, node_order + f"{id},")
        dfs1(root)
        
        lca_set = set(el["id"] for el in target_elements)
        for el1, el2 in combinations(target_elements, 2):
            lca = get_lca(el1, el2)
            if not lca == "":
                lca_set.add(lca)

        def dfs2(node, node_order="", indent=""):
            if illegal_node(node):
                return
            
            if node_order in action_nodes:
                index = action_nodes[node_order]
                output.append(indent + f"[{index}] " + to_str(elements[index]))
                indent += "    "

            elif node_order in lca_set:
                node_view = make_view(node)
                node_view["actions"] = set()
                output.append(indent + to_str(node_view))
                indent += "    "
                
            for id, child in enumerate(node):
                dfs2(child, node_order + f"{id},", indent)
        dfs2(root)
        
        return "\n".join(output)

    def _main_view(self, node):
        width, height = self.uiformer.now_img.size
        x, y, xx, yy = get_position(node)
        return (xx - x) / width > 0.9 and (yy - y) / height > 0.9