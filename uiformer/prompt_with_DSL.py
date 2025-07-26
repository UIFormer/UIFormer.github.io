'''
You are an expert in UI optimization and program synthesis. Your task is to generate a transformation function that processes UI nodes (Android UI Hierarchy in XML format) recursively to reduce token usage while preserving semantic completeness.

## Function Signature
Generate a function with this exact signature:
def transform_node(node, child_views):
    """
    Args:
        node: Current UI node with attributes (class, package, resource-id, text, content-desc, bounds, actions)
        child_views: List of processed views from child nodes (each view has text, description, position, actions, resource_id, class)
    Returns:
        processed_views: List[View]
    """

## Available DSL Operations (USE ONLY THESE)

### Predicates (for conditions):

- `IS_SYSTEM_UI(node)`: node.package.startswith("com.android.systemui")
- `IS_KEYBOARD(node)`: node.package.startswith("com.google.android.inputmethod")
- `IS_LEAF(node)`: len(node.children) == 0
- `IS_CRUCIAL(node)`: node.clickable OR node.scrollable OR node.checkable OR node.long_clickable
- `IS_MAIN_VIEW(node)`: covers >90% of screen area
- `HAS_TEXT(node)`: node.text != ""
- `HAS_CONTENT_DESC(node)`: node.content_desc != ""
- `HAS_RESOURCE_ID(node)`: node.resource_id != ""
- `HAS_CHILDREN(child_views)`: len(child_views) > 0

### Operations (for actions):

- `EMPTY_RESULT()`: return [], False
- `LEAF_RESULT(view)`: return [view], False
- `OPERATION_RESULT(operation)`: return [], True
- `PASSTHROUGH_RESULT(views)`: return views, False
- `CREATE_VIEW(node)`: make_view(node)
- `MERGE_OPERATION(node, child_views, context)`: make_element(context.parent_text, context.parent_content, node, child_views)

## Required Program Structure

Your function MUST follow this pattern:

def transform_node(node, child_views):
    # LEAF NODE HANDLING
    if not child_views:
        # Phase 1: Filter unwanted leaf nodes
        if [LEAF_FILTER_CONDITIONS]: 
            return EMPTY_RESULT()
        # Phase 2: Handle leaf nodes
        else:
            return LEAF_RESULT(CREATE_VIEW(node))
    
    if [FILTER_CONDITIONS]: 
        return child_views
    
    # Phase 3: Make merge decision
    if [MERGE_CONDITIONS]:
        operation = MERGE_OPERATION(node, child_views)
        return OPERATION_RESULT(operation)
    
    # Phase 4: Pass through
    return PASSTHROUGH_RESULT(child_views)

## Examples

Examples of UI node merges that are correctly handled by the synthesis process.  
{positive_examples} 
These include cases where semantically or structurally redundant UI elements are successfully merged without loss of agent-relevant information.

Examples of incorrect and suboptimal node merges during synthesis.  
{negative_examples}
These typically result in loss of critical semantic content (e.g., task-relevant buttons or labels), indicating failure cases that guide iterative refinement.

## Constraints

1. ONLY use the provided DSL operations
2. NEVER modify the function signature
3. ALWAYS handle the five phases in order
4. ALWAYS accumulate parent context before merging
5. Generate semantically valid transformations only

Generate a transformation program that achieves token reduction while preserving semantic completeness.    
'''