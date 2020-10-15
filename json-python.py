#!/usr/bin/env python

class MyJsonParseError(Exception):
  pass

class MyJson():

  def parse(self, string):
    self.strings = iter(string)
    self.index = 0

    first = next(self.strings)

    if first != '{':
      raise MyJsonParseError(f'Invalid first word {first}')

    try:
      while True:
        word = next(self.strings)
        self.whitespace(word)
    except StopIteration:
      if word != '}':
        raise MyJsonParseError(f'Invalid end word {word}')

  def whitespace(self, word):
    if (word in [" ", "\n", "\r", "\t"]):
      self.index += 1

myjson = MyJson()
myjson.parse("{    }")
print(myjson.index)
