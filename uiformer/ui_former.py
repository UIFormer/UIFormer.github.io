from .tree_processor import TreeProcessor
from .action_executor import ActionExecutor

class UIFormer:
    def __init__(self, controller = None, run_type=""):
        self.controller = controller
        self.run_type = run_type
        self.split_page = []
        self.now_img = None
        self.actions = []
        self.action_map = {}
        self.tab_elements = []
        self.tree_processor = TreeProcessor(self)
        self.executor = ActionExecutor(self)

    def optimize_ui_content(self, screen_info):
        root, img = screen_info
        self.now_img = img
        elements = self.tree_processor.process_accessibility_tree(root)
        self.actions = elements
        parameterized = self.tree_processor.parameterize_actions(root, elements)
        return parameterized

    def execute_action(self, action_str):
        action, desc = self.executor.execute(action_str)
        return action, desc