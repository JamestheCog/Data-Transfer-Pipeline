'''
A module to contain custom exceptions for the ETL functionality of this application.
'''

class ProcessException(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code

class LoadException(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code