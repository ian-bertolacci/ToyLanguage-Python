from __future__ import print_function

class Type:
  def __init__(self, symbol):
    self.symbol = symbol

class Named:
  def __init__(self, symbol, type_):
    self.symbol = symbol
    self.type = type_

class Closure:
  def __init__(self, parameters, return_ ):
    self.parameters = parameters
    self.return_ = return_

class Domain:
  def __init__(self, types ):
    self.types = types

class Map:
  def __init__(self, domain, value):
    self.domain = domain
    self.value = value

class Tuple:
  def __init__(self, types ):
    self.types = types
