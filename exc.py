
class InvalidEntry(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class UnknownEntryType(Exception):
    def __init__(self, t):
        self.msg = '%s is not known to the dispatcher' % t

    def __str__(self):
        return self.msg

class InvalidFilter(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
