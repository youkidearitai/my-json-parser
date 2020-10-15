#!/usr/bin/env python

class MyJsonParseError(Exception):
  pass

class MyJson():

  def parse(self, string):
    self.strings = iter(string)
    self.index = 0

    self.word = next(self.strings)

    if self.word != '{':
      raise MyJsonParseError(f'Invalid first word {first}')

    self.word = next(self.strings)

    try:
      while True:
        self.whitespace()
        if self.is_emptyobject():
          break
        key = self.string()
        print(f'--- object key: "{key}" ---')
        self.whitespace()
        self.colon()
        self.whitespace()
        value = self.value()
        print(f'--- object value: "{value}" ---')
        self.whitespace()
        if not self.is_nextobject():
          break
    except StopIteration:
      if self.word != '}':
        raise MyJsonParseError(f'Invalid end word {word}')

  def whitespace(self):
    while True:
      if (self.word in [" ", "\n", "\r", "\t"]):
        self.word = next(self.strings)
        self.index += 1
      else:
        break

  def string(self):
    ret = ""

    if self.word != '"':
      raise MyJsonParseError(f'String parser error: {self.word}')

    self.word = next(self.strings)

    while self.word != '"':
      ret += self.word
      self.word = next(self.strings)
      self.index += 1

    self.word = next(self.strings)

    return ret

  def colon(self):
    if self.word != ':':
      raise MyJsonParseError(f'Colon parser error: {self.word}')

    self.word = next(self.strings)

  def value(self):
    return self.string()

  def is_emptyobject(self):
    if self.word == '}':
      self.word = next(self.strings)
      return True
    return False

  def is_nextobject(self):
    if self.word == ',':
      self.word = next(self.strings)
      return True
    return False


if __name__ == '__main__':
  myjson = MyJson()
  myjson.parse("{    }")
  assert(myjson.index == 4)
  myjson.parse("{}")
  assert(myjson.index == 0)
  myjson.parse("{\n}")
  assert(myjson.index == 1)
  myjson.parse("{\r\n}")
  assert(myjson.index == 2)
  myjson.parse("{\t}")
  assert(myjson.index == 1)

  try:
    myjson.parse('{""}')
    assert(myjson.index == 0)
  except MyJsonParseError as e:
    print(e)

  try:
    myjson.parse('{" "}')
    assert(myjson.index == 1)
  except MyJsonParseError as e:
    print(e)

  try:
    myjson.parse('{" \n"}')
    assert(myjson.index == 2)
  except MyJsonParseError as e:
    print(e)

  try:
    myjson.parse('{"  "}')
    assert(myjson.index == 2)
  except MyJsonParseError as e:
    print(e)

  try:
    myjson.parse('{"  " }')
    assert(myjson.index == 3)
  except MyJsonParseError as e:
    print(e)
  """
  """

  myjson.parse('{"  ":" "}')
  assert(myjson.index == 3)
  myjson.parse('{"ab": "b" , "c": "d"}')
  myjson.parse('{"ab":"b","c":"d"}')
  assert(myjson.index == 5)
