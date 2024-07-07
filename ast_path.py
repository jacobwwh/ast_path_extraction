import tree_sitter_python as tspython
from tree_sitter import Language, Parser

def find_node_and_path(tree, target_line=-1): 
    """Finding the node for the target line, then build the path from to the target node.
    Using tree.walk() for traversal."""
    #First step: traverse the tree to find the target node
    def traverse_tree(tree): #traverse function with cursor (tree.walk())
        cursor=tree.walk()
        
        visited_children = False
        while True:
            if not visited_children:
                yield cursor    #yield cursors so we can access the cursor outside the function
                if cursor.node.start_point[0]==target_line:
                    break
                if not cursor.goto_first_child():
                    visited_children = True
            elif cursor.goto_next_sibling():
                visited_children = False
            elif not cursor.goto_parent():
                break
    
    all_cursors=list(traverse_tree(tree))
    #print(len(all_cursors))
    for cursor in all_cursors:
        start_point, end_point=cursor.node.start_point, cursor.node.end_point
        start_line=start_point[0]
        
        if start_line==target_line:
            target_cursor=cursor
            break
    target_cursor_1=all_cursors[-1] #theoretically, the last cursor should be the target cursor
    assert target_cursor==target_cursor_1
    
    #Second step: find the backward path with all related condition branches
    condition_path=[]
    satisfy_last_branch=True  # In one hierarchy of branches, only the first visited branch (in backwards order) is satisfied
    while True:
        if not target_cursor.node.parent: #reach the root node
            break
        if target_cursor.node.type=='else_clause':
            print('insert: else')
            condition_path.insert(0, {'node': target_cursor.node, 'content': 'else', 'line': get_startline(target_cursor.node), 'satisfy': True})
            satisfy_last_branch=False
        elif target_cursor.node.type=='elif_clause':
            print('insert: elif')
            condition_node=target_cursor.node.child_by_field_name('condition')
            elif_condition=condition_node.text.decode('utf-8')
            condition_path.insert(0, {'node': target_cursor.node, 'content': f'elif {elif_condition}:', 'line': get_startline(condition_node), 'satisfy': satisfy_last_branch})
            if satisfy_last_branch: #if this elif branch is satisfied, then the previous branch is not satisfied
                satisfy_last_branch=False
        elif target_cursor.node.type=='block' and target_cursor.node.parent.type=='if_statement': #reach the 'true' branch of an if statement
            print('insert: if')
            if_node=target_cursor.node.parent
            condition_node=if_node.child_by_field_name('condition')
            if_condition=condition_node.text.decode('utf-8')
            condition_path.insert(0, {'node': target_cursor.node, 'content': f'if {if_condition}:', 'line': get_startline(condition_node), 'satisfy': satisfy_last_branch})

        if target_cursor.node.prev_sibling:
            target_cursor.goto_previous_sibling() #search backwards
            #print(target_cursor.node.type, target_cursor.node.start_point, target_cursor.node.end_point)
        else: #if no previous branches on the same level, go to the upper level
            target_cursor.goto_parent()
            satisfy_last_branch=True
    
    return condition_path
        


def get_startline(node):
    return node.start_point[0]
