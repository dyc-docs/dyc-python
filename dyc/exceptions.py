"""
All exception classes are defined here
"""



class DYCError(Exception): pass
class SetupError(DYCError): pass
class UndefinedPattern(DYCError): pass