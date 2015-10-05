# -*- coding: utf-8 -*-

class InvalidDocumentException(Exception):
    pass

class CPFInvalidException(InvalidDocumentException):
    pass

class CNPJInvalidException(InvalidDocumentException):
    pass