def logger(code, message):
    if code == "error":
        color_scheme = "\033[91m[ERROR]\033[0m"
    elif code == "success":
        color_scheme = "\033[92m[SUCCESS]\033[0m"
    elif code == "warning":
        color_scheme = "\033[93m[WARNING]\033[0m"
    else:
        color_scheme = "\033[94m[INFO]\033[0m"
    
    print(color_scheme + " " + message)
