import re

def validate_string_for_tags(s):
    """
    Validates a string based on the following rules:
    - Contains only lowercase letters, spaces, and hyphens.
    - Must include at least two letters (ignoring spaces and hyphens).
    
    Args:
        s (str): The input string to validate.
    
    Returns:
        bool: True if the string is valid, False otherwise.
    """
    # Check if the string contains only allowed characters
    if not re.fullmatch(r'[a-z\s-]+', s):
        return False
    
    # Remove spaces and hyphens to count letters
    letters_only = s.replace(" ", "").replace("-", "")
    
    # Ensure the string contains at least two letters
    if len(letters_only) < 2:
        return False

    return True

def validate_string(s):
    """
    Validates a given string to ensure it contains only letters, spaces, and hyphens.
    The function performs the following checks:
    1. The string must only contain alphabetic characters (a-z, A-Z), spaces, and hyphens.
    2. After removing spaces and hyphens, the string must contain at least one letter.
    Args:
        s (str): The string to validate.
    Returns:
        bool: True if the string is valid, False otherwise.
    """
    if not re.fullmatch(r'[a-zA-Z\s-]+', s):
        return False
    # Remove spaces and hyphens to count letters
    letters_only = s.replace(" ", "").replace("-", "")
    
    # Ensure the string contains at least one letter
    if len(letters_only) < 1:
        return False
    return True