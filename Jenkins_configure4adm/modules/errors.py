# -*- coding: UTF-8 -*-
import urllib2
from urllib2 import HTTPError


class SvnException(Exception): pass

class ShellException(Exception): pass

class JenkinsException(Exception): pass

class XmlException(Exception): pass

class EmptyException(Exception): pass

class NullException(Exception): pass
