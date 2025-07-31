def print_info(text, end='\n'):
    print(f"\033[94m{text}\033[0m", end=end)  # Blue

def print_warn(text, end='\n'):
    print(f"\033[93m{text}\033[0m", end=end)  # Yellow

def print_error(text, end='\n'):
    print(f"\033[91m{text}\033[0m", end=end)  # Red

def print_success(text, end='\n'):
    print(f"\033[92m{text}\033[0m", end=end)  # Green