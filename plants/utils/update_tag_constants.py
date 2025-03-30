# plants/utils/tag_helpers.py
import json
import os

def update_tag_constants(tag_data):
    """
    Update the tag_constants.py file with new tag data
    
    Args:
        tag_data: List of dictionaries with tag information
    """
    # Get the path to the tag_constants.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    constants_file = os.path.join(current_dir, 'tag_constants.py')
    
    # Format the data as a Python assignment
    formatted_data = "TAG_EMOJIS = [\n"
    for tag in tag_data:
        formatted_data += f" {{'name': '{tag['name']}', 'emoji': '{tag['emoji']}', 'color': '{tag['color']}'}},\n"
    formatted_data += "]"
    
    # Write to the file
    with open(constants_file, 'w') as f:
        f.write(formatted_data)
    
    return True