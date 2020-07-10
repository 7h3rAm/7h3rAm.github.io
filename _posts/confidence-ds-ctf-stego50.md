CONFidence DS CTF Teaser: Stegano50
===================================
date: 6/May/2014
summary: This post discusses how I completed the stego50 challenge from Dragon Sector CTF team. It is a simplistic challenge but a good source for learning about PDF internals.
tags: code, ctf

The challenge consists a [pdf](/static/files/posts_confidence_ds_ctf_stego50/stegano50.pdf) file. Let's see what `exiftool` tells us about it:

```
$ exiftool stegano50.pdf
ExifTool Version Number         : 9.46
File Name                       : stegano50.pdf
Directory                       : .
File Size                       : 38 kB
File Modification Date/Time     : 2014:05:06 22:08:58+05:30
File Access Date/Time           : 2014:05:06 20:41:54+05:30
File Inode Change Date/Time     : 2014:05:06 13:05:07+05:30
File Permissions                : rw-rw-r--
File Type                       : PDF
MIME Type                       : application/pdf
PDF Version                     : 1.5
Linearized                      : No
Page Count                      : 1
Page Mode                       : UseOutlines
Author                          : KeiDii
Title                           : polar bear during a snow storm
Subject                         : <| tr AB .- |>
Creator                         : LaTeX /o/
Producer                        : find mr.morse text
Keywords                        : Could, this, be, the, flag?, :, Tm9wZSAsIG5vdCBoZXJlIDspCg==
Create Date                     : 2014:03:13 22:33:50+01:00
Modify Date                     : 2014:03:13 22:33:50+01:00
Trapped                         : False
PTEX Fullbanner                 : This is pdfTeX, Version 3.1415926-2.5-1.40.14 (TeX Live 2013/Debian) kpathsea version 6.1.1
```

All attributes seem standard except for `Subject`, `Producer` and `Keywords`. Since the `Keywords` obviously hints at a flag like string which seems to be base64 encoded, the first thing I tried was to decode it:

```
$ echo -n "Tm9wZSAsIG5vdCBoZXJlIDspCg==" | base64 -d - 
Nope , not here ;)
```

Well, that explains. Let's focus on `Subject` and `Producer` once again. These definitely hint towards a blob of text that might need Morse code decoding. The `Subject` hints towards translating A and B to dot and dash and it obviously points to the fact that the blob of text has to be all As and Bs. Let's view the pdf in Firefox via its [pdf.js](https://mozilla.github.io/pdf.js/) renderer:

![stego50_pdfjs.png](/static/files/posts_confidence_ds_ctf_stego50/stego50_pdfjs.png)

There it is! A `div` element has the text blob we need. Let's extract and translate it as per the hint:

```
$ echo -n "BABA BBB BA BBA ABA AB B AAB ABAA AB B AA BBB BA AAA BBAABB AABA ABAA AB BBA BBBAAA ABBBB BA AAAB ABBBB AAAAA ABBBB BAAA ABAA AAABB BB AAABB AAAAA AAAAA AAAAB BBA AAABB" | tr AB .-
-.-. --- -. --. .-. .- - ..- .-.. .- - .. --- -. ... --..-- ..-. .-.. .- --. ---... .---- -. ...- .---- ..... .---- -... .-.. ...-- -- ...-- ..... ..... ....- --. ...--
```

Alright, we now have some Morse code that has to be decoded. There are [several](http://mattfedder.com/cgi-bin/morse.pl) [online](http://morsecode.scphillips.com/translator.html) [decoders](http://www.onlineconversion.com/morse_code.htm) [available](http://www.unit-conversion.info/texttools/morse-code/), however, I tend to use Python for such tasks. Here is a snippet of Python code to help us with encode and decode tasks:

```python
#!/usr/bin/env python

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
```

Let's quickly use this script from within `iPython` and decode the Morse encoded message:

```python
$ ipython --no-banner

>>> import morse
>>> morse = morse.morse()
>>>
>>> message = "-.-. --- -. --. .-. .- - ..- .-.. .- - .. --- -. ... --..-- ..-. .-.. .- --. ---... .---- -. ...- .---- ..... .---- -... .-.. ...-- -- ...-- ..... ..... ....- --. ...--"
>>>
>>> morse.from_morse(message)
'CONGRATULATIONS,FLAG:1NV151BL3M3554G3'
>>>
```

There we go!