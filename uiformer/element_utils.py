import re
import hashlib
from PIL import ImageDraw
import random

def get_position(node, scale=1):
    x, y, xx, yy = map(int, re.findall(r'\d+', node.attrib['bounds']))
    return [x // scale, y // scale, xx // scale, yy // scale]

def get_str_position(s, scale=1):
    x, y, xx, yy = map(int, re.findall(r'\d+', s))
    return [x // scale, y // scale, xx // scale, yy // scale]

def gettext(node):
    text = ""
    description = ""
    if 'text' in node.attrib and node.attrib['text'] != "":
        text = node.attrib['text'] + " "
    if 'content-desc' in node.attrib and node.attrib['content-desc'] != "":
        description = node.attrib['content-desc'] + " "
    return text, description

def make_view(node):
    text, description = gettext(node)

    position = get_position(node)
    actions = set()
    for key, val in node.attrib.items():
        if val == 'true':
            actions.add(key)

    if "class" in node.attrib and node.attrib["class"].endswith("EditText"):
        actions.add("text")

    resource_id = node.attrib.get("resource-id", "").split("/")[-1].split("\\")[-1]

    return {
        "text": text,
        "description": description,
        "position": position,
        "actions": actions,
        "resource_id": resource_id,
        "class": node.attrib.get("class", "")
    }


def make_element(base_text, base_desc, node, contained_views):
    text = base_text
    description = base_desc
    position = get_position(node)
    actions = set()
    for key, val in node.attrib.items():
        if val == 'true':
            actions.add(key)

    for view in contained_views:
        text += view["text"]
        description += view["description"]
        position = [
            min(position[0], view["position"][0]),
            min(position[1], view["position"][1]),
            max(position[2], view["position"][2]),
            max(position[3], view["position"][3])
        ]
        actions.update(view["actions"])

    resource_id = node.attrib.get("resource-id", "").split("/")[-1].split("\\")[-1]
    if "text" in actions:
        node.attrib["class"] = "android.widget.EditText"

    return {
        "text": text,
        "description": description,
        "position": position,
        "actions": actions,
        "resource_id": resource_id,
        "class": node.attrib.get("class", "")
    }


def is_crucial_node(node):
    return any(
        node.attrib.get(key) == "true"
        for key in ["clickable", "checkable", "scrollable", "long-clickable"]
    )


def contains(bbox1, bbox2, threshold=10):
    return bbox1[0] - threshold <= bbox2[0] and \
           bbox1[1] - threshold <= bbox2[1] and \
           bbox1[2] + threshold >= bbox2[2] and \
           bbox1[3] + threshold >= bbox2[3]


def overlap(bbox1, bbox2, threshold=10):
    return not (
        bbox1[2] < bbox2[0] + threshold or
        bbox1[0] > bbox2[2] - threshold or
        bbox1[3] < bbox2[1] + threshold or
        bbox1[1] > bbox2[3] - threshold
    )


def center_of_element(element):
    box = element["position"]
    rndx = random.randint(-2,2)
    rndy = random.randint(-2,2)
    return f"[{(box[0] + box[2]) // 2 + rndx},{(box[1] + box[3]) // 2 + rndy}]"


def to_str(element):
    actions_desc = []
    for action in ["clickable", "scrollable", "long-clickable", "text"]:
        if action in element["actions"]:
            actions_desc.append(action.replace('-', ' '))

    widget = f"a {element['class'].split('.')[-1]} ("
    if "checkable" in element["actions"]:
        widget += f"is checked: {'checked' in element['actions']}; "
    if element["resource_id"]:
        widget += f"resource_id: {element['resource_id']}; "
    if element["text"]:
        widget += f"text: {element['text']}; "
    if element["description"]:
        widget += f"content-desc: {element['description']}; "
    if actions_desc:
        widget += "actions: " + ", ".join(actions_desc) + "; "
    widget += ")"

    return widget

def equal(element1, element2):
    return to_str(element1) == to_str(element2)

def need_expand(element):
    return not element["text"] and not element["description"]

def draw_bbox(img, bbox, color='red'):
    draw = ImageDraw.Draw(img)
    draw.rectangle(bbox, outline=color, width=2)

def get_lca(element1, element2):
    id1_list = [item for item in element1["id"].split(",") if item]
    id2_list = [item for item in element2["id"].split(",") if item]
    
    common = []
    for part1, part2 in zip(id1_list, id2_list):
        if part1 == part2:
            common.append(part1)
        else:
            break
        
    lca = ",".join(common) + "," if common else ""
    return lca     
    
def illegal_node(node):
    if "package" in node.attrib and node.attrib["package"].startswith("com.android.systemui"):
        return True
    if "resource-id" in node.attrib and node.attrib["resource-id"].startswith("com.google.android.inputmethod.latin:id"):
        return True
    
    return False

def get_clickable_box(root):
    clickable_box = []
    text = []
    
    def dfs(node):
        if illegal_node(node):
            return 
        
        if is_crucial_node(node):
            clickable_box.append(node.attrib["bounds"])
        
        if "text" in node.attrib:
            text.append(node.attrib["text"] + node.attrib["content-desc"])
        
        for child in node:
            dfs(child)

    dfs(root)
    
    clickable_box.sort()
    text.sort()
    
    def hash_str(s):
        return hashlib.md5(s.encode()).hexdigest()
    
    return hash_str("".join(clickable_box)), hash_str("".join(text))

def center_of_box(box):
    return f"[{(box[0] + box[2]) // 2},{(box[1] + box[3]) // 2}]"

def parse_from_json(action):
    if action.get("type") == "click":
        return f"click {center_of_box(get_str_position(action.get('element')['bounds']))}"
    
    if action.get("type") == "longclick":
        return f"longclick {center_of_box(get_str_position(action.get('element')['bounds']))}"
    
    if action.get("type") == "input":
        return f"text {center_of_box(get_str_position(action.get('element')['bounds']))} [{action.get('message')}]"
    
    if action.get("element") is None:
        return f"press [{action.get('type')}]"