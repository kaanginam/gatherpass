import re
class LeakParser:
    def __init__(self, passlist, providers, config):
        self.passlist = self.get_lines(passlist)
        self.providers = providers
        self.config = config
    def check_patterns(self, string):
        retcode = 0
        for sep in self.config.get_seperators():
            p = re.compile(f"[^{sep}]*" + sep + f"{1}[^sep]*")
            if p.match(string):
                return retcode, sep
            retcode += 1
        return -1
    def has_credentials(self, text):
        retcode = 0
        for pw in self.passlist:
            if pw in text:
                retcode = 1
        for prov in self.providers:
            if prov in text:
                retcode =  2
        # lines = text.split('\n')
        #for line in lines:
        #    line_mod = line.strip()
        #    if len(self.check_patterns(line_mod)) > 1:
        #        retcode = 3
        #        break
        return retcode
    def guess_n(self, text):
        return round(len(text.split('\n'))*self.config.get_ratio())
    def has_credentials_n(self, text):
        cnt = 0
        n = self.guess_n(text)
        for pw in self.passlist:
            if pw in text:
                cnt += 1
        if cnt >= n:
            return True
        else:
            return False
    def get_lines(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()
    def get_full_text(self, filename):
        with open(filename, 'r') as f:
            return f.read()