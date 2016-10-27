#!/usr/bin/env python

import sys

class morse:
  def __init__(self):
    # https://en.wikipedia.org/wiki/Morse_code
    self.tocode = dict({
      'A': '.-',
      'B': '-...',
      'C': '-.-.',
      'D': '-..',
      'E': '.',
      'F': '..-.',
      'G': '--.',
      'H': '....',
      'I': '..',
      'J': '.---',
      'K': '-.-',
      'L': '.-..',
      'M': '--',
      'N': '-.',
      'O': '---',
      'P': '.--.',
      'Q': '--.-',
      'R': '.-.',
      'S': '...',
      'T': '-',
      'U': '..-',
      'V': '...-',
      'W': '.--',
      'X': '-..-',
      'Y': '-.--',
      'Z': '--..',
      '0': '-----',
      '1': '.----',
      '2': '..---',
      '3': '...--',
      '4': '....-',
      '5': '.....',
      '6': '-....',
      '7': '--...',
      '8': '---..',
      '9': '----.',
      '.': '.-.-.-',
      ',': '--..--',
      '?': '..--..',
      '\'': '.----.',
      '!': '-.-.-- ',
      '/': '-..-.',
      '(': '-.--.',
      ')': '-.--.-',
      '&': '.-...',
      ':': '---...',
      ';': '-.-.-.',
      '=': '-...-',
      '+': '.-.-.',
      '-': '-....-',
      '_': '..--.-',
      '"': '.-..-.',
      '$': '...-..-',
      '@': '.--.-.'
    })

    self.fromcode = dict((v,k) for (k,v) in self.tocode.items())

  def to_morse(self, d):
    i = list()
    for c in d:
      if c.upper() in self.tocode.keys():
        i.append(self.tocode[c.upper()])
      else:
        i.append(" ")
    return " ".join(i)

  def from_morse(self, d):
    i = list()
    for c in d.split(" "):
      if c in self.fromcode.keys():
        i.append(self.fromcode[c])
    return "".join(i)

