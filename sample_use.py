import xml.etree.ElementTree as ET
from PIL import Image
from uiformer import UIFormer

xml_path = f"test.xml"
img_path = f"test.png"
ui = UIFormer()

with open(xml_path, "r", encoding="utf-8") as f:
    root = ET.fromstring(f.read())

img = Image.open(img_path)
print("=== Optimizing UI Content ===")
ui_content = ui.optimize_ui_content((root, img))
print(ui_content)

print("\n=== Testing Action Execution ===")
action_str = f"click [1]"
parsed_actions, description = ui.execute_action(action_str)
print("Parsed Actions:", parsed_actions)
print("Action Description:", description)