#!/usr/bin/env python

class MyJson():

  def parse(self, string):
    self.strings = list(string)
    self.index = 0

    for string in self.strings:
      self.whitespace(string)

  def whitespace(self, string):
    if (string in [" ", "\n", "\r", "\t"]):
      self.index += 1

myjson = MyJson()
myjson.parse("    ")
print(myjson.index)
