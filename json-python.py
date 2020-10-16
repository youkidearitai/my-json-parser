#!/usr/bin/env python

class MyJsonParseError(Exception):
  pass

class MyJson():

  json_value = dict()

  def parse(self, string):
    self.json_value = dict()

    self.strings = iter(string)
    self.index = 0

    self.word = next(self.strings)

    if self.word != '{':
      raise MyJsonParseError(f'Invalid first word {first}')

    visited = False
    try:
      self.json_value = self.value_object()
    except StopIteration as e:
      visited = True
      if self.word != '}':
        raise MyJsonParseError(f'Invalid end word {word}')

    return self.json_value

  def value_object(self):
    self.word = next(self.strings)
    json_value = dict()

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
      json_value[key] = value
      if not self.is_nextobject():
        break

    return json_value

  def value_array(self):
    self.word = next(self.strings)
    json_value = []

    while True:
      self.whitespace()
      if self.is_emptyarray():
        break
      value = self.value()
      self.whitespace()
      json_value.append(value)
      if not self.is_nextarray():
        break

    return json_value

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

  def value_number(self):
    def digit():
      number = ""

      if self.word == '-':
        number += '-'
        self.word = next(self.strings)
        self.index += 1

      while True:
        if self.word in [chr(48 + i) for i in range(10)]:
          number += self.word
          self.word = next(self.strings)
          self.index += 1
        else:
          break

      return number

    def fraction():
      nonlocal is_integer

      value = digit()
      if self.word == '.':
        value += '.'
        self.word = next(self.strings)
        self.index += 1
        value += digit() # decimal
        is_integer = False
      return value

    def exponent():
      nonlocal is_integer

      value = fraction()
      if self.word in ['e', 'E']:
        value += 'e'
        self.word = next(self.strings)
        self.index += 1
        if self.word in ['-', '+']:
          value += self.word
          self.word = next(self.strings)
          self.index += 1
        value += digit()
        is_integer = False
      return value

    is_integer = True
    number = exponent()
    if is_integer:
      return int(number, 10)
    else:
      return float(number)

  def value(self):
    if self.word == '"':
      return self.value_string()

    if self.word in ['-'] + [chr(48 + i) for i in range(10)]:
      return self.value_number()

    if self.word == '{':
      value = self.value_object()
      return value

    if self.word == '[':
      value = self.value_array()
      return value

    if self.word == 'f':
      return self.value_false()

    if self.word == 't':
      return self.value_true()

    if self.word == 'n':
      return self.value_null()

    raise MyJsonParseError(f"Value error: {self.word}")

  def is_emptyarray(self):
    if self.word == ']':
      self.word = next(self.strings)
      return True
    return False

  def is_nextarray(self):
    if self.word == ',':
      self.word = next(self.strings)
      return True

    try:
      self.word = next(self.strings)
    except StopIteration as e:
      pass

    return False

  def is_emptyobject(self):
    if self.word == '}':
      self.word = next(self.strings)
      return True
    return False

  def is_nextobject(self):
    if self.word == ',':
      self.word = next(self.strings)
      return True

    try:
      self.word = next(self.strings)
    except StopIteration as e:
      pass

    return False


if __name__ == '__main__':
  myjson = MyJson()
  assert(myjson.parse("{    }") == {})
  assert(myjson.index == 4)
  assert(myjson.parse("{}") == {})
  assert(myjson.index == 0)
  assert(myjson.parse("{\n}") == {})
  assert(myjson.index == 1)
  assert(myjson.parse("{\r\n}") == {})
  assert(myjson.index == 2)
  assert(myjson.parse("{\t}") == {})
  assert(myjson.index == 1)

  try:
    myjson.parse('{""}')
    assert(myjson.index == 0)
  except MyJsonParseError as e:
    assert("Colon parser error: }" == str(e))

  try:
    myjson.parse('{" "}')
    assert(myjson.index == 1)
  except MyJsonParseError as e:
    assert("Colon parser error: }" == str(e))

  try:
    myjson.parse('{" \n"}')
    assert(myjson.index == 2)
  except MyJsonParseError as e:
    assert("Colon parser error: }" == str(e))

  try:
    myjson.parse('{"  "}')
    assert(myjson.index == 2)
  except MyJsonParseError as e:
    assert("Colon parser error: }" == str(e))

  try:
    myjson.parse('{"  " }')
    assert(myjson.index == 3)
  except MyJsonParseError as e:
    assert("Colon parser error: }" == str(e))

  assert(myjson.parse('{"  ":" "}') == {"  ": " "})
  assert(myjson.index == 3)
  assert(myjson.parse('{"ab": "b" , "c": "d"}') == {"ab": "b", "c": "d"})
  assert(myjson.parse('{"ab":"b","c":"d"}') == {"ab": "b", "c": "d"})
  assert(myjson.index == 5)

  assert(myjson.parse('{"ab": false}') == {"ab": False})
  assert(myjson.index == 8)

  assert(myjson.parse('{"ab": false, "cd": true}') == {"ab": False, "cd": True})
  assert(myjson.index == 16)

  assert(myjson.parse('{"ab": false, "cd": true, "ef": null}') == {"ab": False, "cd": True, "ef": None})
  assert(myjson.index == 24)

  assert(myjson.parse('{"a": "\\""}') == {"a": "\""})
  assert(myjson.index == 4)

  assert(myjson.parse('{"a": "\\"def\\""}') == {"a": "\"def\""})
  assert(myjson.index == 9)

  string = '{"quot": "\\"", "backslash": "\\\\", "solidius": "\\/", "backspace": "\\b", "formfeed": "\\f", "linefeed": "\\n", "carriage return": "\\r", "horizontal tab": "\\t"}'
  assert(myjson.parse(string) == {"quot": '"', "backslash": '\\', "solidius": '/', "backspace": '\b', "formfeed": '\f', "linefeed": '\n', "carriage return": '\r', "horizontal tab": '\t'})

  string = '{"unicode": "\\u9000", "japanese hiragana small a": "\\u3041"}'
  assert(myjson.parse(string) == {"unicode": "\u9000", "japanese hiragana small a": "\u3041"})

  string = '{"number": 123, "minus number": -123, "zero": 0, "minus zero": -0}'
  assert(myjson.parse(string) == {"number": 123, "minus number": -123, "zero": 0, "minus zero": 0})

  string = '{"fraction": 123.5, "minus fraction": -123.5, "zero": 0.0, "minus zero": -0.0, "exponent": -123.4e+5}'
  assert(myjson.parse(string) == {"fraction": 123.5, "minus fraction": -123.5, "zero": 0.0, "minus zero": -0.0, "exponent": -123.4e+5})

  string = '{"object": {}}'
  assert(myjson.parse(string) == {'object': {}})

  string = '{"object": {}, "abc": {}}'
  assert(myjson.parse(string) == {'object': {}, 'abc': {}})

  string = '{"object": {}, "abc": {}, "def": {}}'
  assert(myjson.parse(string) == {'object': {}, 'abc': {}, 'def': {}})
  string = '{"object": {"obj": {}}}'
  parsed = myjson.parse(string)
  assert(parsed == {'object': {'obj': {}}})

  string = '{"object": {"obj": {}}, "abc": {}}'
  parsed = myjson.parse(string)
  assert(parsed == {'object': {'obj': {}}, 'abc': {}})

  string = '{"object": {"obj": {}}, "abc": 2}'
  parsed = myjson.parse(string)
  assert(parsed == {'object': {'obj': {}}, 'abc': 2})

  string = '{"object": {"obj": {"aaa": 3}}, "abc": 2}'
  parsed = myjson.parse(string)
  assert(parsed == {'object': {'obj': {"aaa": 3}}, 'abc': 2})

  string = '{"array": [1,2,3,4,5]}'
  parsed = myjson.parse(string)
  assert(parsed == {"array": [1, 2, 3, 4, 5]})

  string = '{"object": {"array": [1,2,3,4,5]}, "array": [{"1": "aaa", "2": "bbb"}]}'
  parsed = myjson.parse(string)
  assert(parsed == {"object": {"array": [1, 2, 3, 4, 5]}, "array": [{"1": "aaa", "2": "bbb"}]})
