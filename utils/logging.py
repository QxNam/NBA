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

class Logger():
    def __init__(self):
        self.B = '\033[94m'
        self.Y = '\033[93m'
        self.G = '\033[92m'
        self.R = '\033[91m'
        self.BOLD = '\033[1m'
        self.E = '\033[0m'

    def FAIL(self, msg='ERROR'):
        return self.R + str(msg) + self.E
    
    def OK(self, msg='SUCCESS'):
        return self.G + str(msg) + self.E
    
    def WARN(self, msg='WARNING'):
        return self.Y + str(msg) + self.E
    
    def TEXT(self, msg=''):
        return self.B + f"{msg}" + self.E
    
    def TEXT_BOLD(self, msg=''):
        return self.BOLD + f"{msg}" + self.E
    
    def status(self, title, idx, n):
        pc = round((idx+1)/n*100, 2)
        if int(pc)*1.0 == pc:
            pc = int(pc)
        return '['+self.TEXT(title)+'] ' + self.OK(f'{pc}%') + self.TEXT_BOLD(f'({idx+1}/{n}):')