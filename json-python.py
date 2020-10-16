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
        key = self.value_string()
        self.whitespace()
        self.colon()
        self.whitespace()
        value = self.value()
        self.whitespace()
        print(f'--- object key: "{key}" ---')
        print(f'--- object type: {type(value)} value: {value} ---')
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

  def value_string(self):
    ret = ""

    if self.word != '"':
      raise MyJsonParseError(f'String parser error: {self.word}')

    self.word = next(self.strings)

    while self.word != '"':
      if self.word == '\\':
        self.word = next(self.strings)
        self.index += 1

        if self.word == '"':
          self.word = '"'
        elif self.word == '\\':
          self.word = '\\'
        elif self.word == '/':
          self.word = '/'
        elif self.word == 'b':
          self.word = '\b'
        elif self.word == 'f':
          self.word = '\f'
        elif self.word == 'n':
          self.word = '\n'
        elif self.word == 'r':
          self.word = '\r'
        elif self.word == 't':
          self.word = '\t'
        elif self.word == 'u':
          codepoint = ""
          valids = [chr(48 + i) for i in range(10)] + [chr(97 + i) for i in range(6)] + [chr(65 + i) for i in range(6)]
          for index in range(4):
            digits = next(self.strings)
            if digits in valids:
              codepoint += digits
          self.word = chr(int(codepoint, 16))

        ret += self.word
        self.word = next(self.strings)
        self.index += 1
      else:
        ret += self.word
        self.word = next(self.strings)
        self.index += 1

    self.word = next(self.strings)

    return ret

  def colon(self):
    if self.word != ':':
      raise MyJsonParseError(f'Colon parser error: {self.word}')

    self.word = next(self.strings)

  def value_false(self):
    token = ""

    for index in range(5):
      token += self.word
      self.word = next(self.strings)
      self.index += 1

    if token != 'false':
      raise MyJsonParseError(f'False parse error: {token}')

    return False

  def value_true(self):
    token = ""

    for index in range(4):
      token += self.word
      self.word = next(self.strings)
      self.index += 1

    if token != 'true':
      raise MyJsonParseError(f'True parse error: {token}')

    return True

  def value_null(self):
    token = ""

    for index in range(4):
      token += self.word
      self.word = next(self.strings)
      self.index += 1

    if token != 'null':
      raise MyJsonParseError(f'Null parse error: {token}')

    return None

  def value(self):
    if self.word == '"':
      return self.value_string()

    if self.word == 'f':
      return self.value_false()

    if self.word == 't':
      return self.value_true()

    if self.word == 'n':
      return self.value_null()

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

  myjson.parse('{"ab": false}')
  assert(myjson.index == 8)

  myjson.parse('{"ab": false, "cd": true}')
  assert(myjson.index == 16)

  myjson.parse('{"ab": false, "cd": true, "ef": null}')
  assert(myjson.index == 24)

  myjson.parse('{"a": "\\""}')
  assert(myjson.index == 4)

  myjson.parse('{"a": "\\"def\\""}')
  assert(myjson.index == 9)

  string = '{"quot": "\\"", "backslash": "\\\\", "solidius": "\\/", "backspace": "\\b", "formfeed": "\\f", "linefeed": "\\n", "carriage return": "\\r", "horizontal tab": "\\t"}'
  print(string)
  myjson.parse(string)

  string = '{"unicode": "\\u9000", "japanese hiragana small a": "\\u3041"}'
  print(string)
  myjson.parse(string)

