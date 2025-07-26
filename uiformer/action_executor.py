import re
from .element_utils import center_of_element, to_str
from .errors import ActionParseError

class ActionExecutor:
    def __init__(self, uiformer):
        self.uiformer = uiformer

    def execute(self, action_str):
        action = action_str.split("[")[0].strip()
        if action == "click":
            return self._click_action(action_str)
        elif action == "longclick":
            return self._longclick_action(action_str)
        elif action == "text":
            return self._text_action(action_str)
        elif action == "swipe":
            return self._swipe_action(action_str)
        elif action == "press":
            return self._press_action(action_str)
        else:
            raise ActionParseError(f"Invalid action: {action_str}")

    def _click_action(self, action_str):
        pattern = r'click \[(\d+)\]'
        match = re.match(pattern, action_str)
        if not match:
            raise ActionParseError(f"Invalid click action. {action_str}")
        idx = int(match.group(1))
        element = self.uiformer.actions[idx]
        actions = [f"click {center_of_element(element)}"]
        description = f"Click on {to_str(element)}."
        return actions, description

    def _longclick_action(self, action_str):
        pattern = r'longclick \[(\d+)\]'
        match = re.match(pattern, action_str)
        if not match:
            raise ActionParseError(f"Invalid longclick action. {action_str}")
        idx = int(match.group(1))
        element = self.uiformer.actions[idx]
        actions = [f"longclick {center_of_element(element)}"]
        description = f"Long click on {to_str(element)}."
        return actions, description

    def _text_action(self, action_str):
        pattern = r'text \[(\d+)\] \[(.*)\]'
        match = re.match(pattern, action_str)
        if not match:
            raise ActionParseError(f"Invalid text action. {action_str}")
        idx, message = int(match.group(1)), match.group(2)
        element = self.uiformer.actions[idx]
        actions = [f"text {center_of_element(element)} [{message}]", "press [enter]"]
        description = f"Type {message} on {to_str(element)}."
        return actions, description

    def _swipe_action(self, action_str):
        pattern = r'swipe \[(\d+)\] \[(.*)\]'
        match = re.match(pattern, action_str)
        if not match or len(match.groups()) != 2:
            raise ActionParseError(f"Invalid swipe action: {action_str}")
        idx = int(match.group(1))
        direction = match.group(2)
        if direction.startswith("direction="):
            direction = direction.split("=")[1]
        if direction not in ["up", "down", "left", "right"]:
            raise ActionParseError(f"Invalid swipe direction: {direction}. Original action: {action_str}")

        element = self.uiformer.actions[idx]
        x1, y1, x2, y2 = element["position"]
        if direction == "down":
            from_pos = ((x1 + x2) // 2, (y1 * 2 + y2) // 3)
            to_pos = ((x1 + x2) // 2, (y1 + y2 * 2) // 3)
        elif direction == "up":
            from_pos = ((x1 + x2) // 2, (y1 + y2 * 2) // 3)
            to_pos = ((x1 + x2) // 2, (y1 * 2 + y2) // 3)
        elif direction == "left":
            from_pos = ((x1 + x2 * 2) // 3, (y1 + y2) // 2)
            to_pos = ((x1 * 2 + x2) // 3, (y1 + y2) // 2)
        else:  
            from_pos = ((x1 * 2 + x2) // 3, (y1 + y2) // 2)
            to_pos = ((x1 + x2 * 2) // 3, (y1 + y2) // 2)

        actions = [f"swipe [{from_pos[0]},{from_pos[1]}] [{to_pos[0]},{to_pos[1]}]"]
        description = f"Swipe on {to_str(element)} in {direction} direction."
        return actions, description

    def _press_action(self, action_str):
        if action_str not in [
            "press [none]", "press [back]", "press [enter]",
            "press [restart]", "press [stop]", "press [home]"
        ]:
            raise ActionParseError(f"Invalid press action: {action_str}")

        desc_map = {
            "press [none]": "Do nothing.",
            "press [back]": "Go back.",
            "press [enter]": "Press enter.",
            "press [restart]": "Restart the app.",
            "press [stop]": "Stop the app.",
            "press [home]": "Go home."
        }
        return [action_str], desc_map[action_str]
