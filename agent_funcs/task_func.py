def check_all_int(dict_input):
    print("Checking if all values are integers...")
    
    for key, value in dict_input.items():
        if not isinstance(value, int):
            return f"The value for '{key}' is not an integer."
    return "All values are integers."