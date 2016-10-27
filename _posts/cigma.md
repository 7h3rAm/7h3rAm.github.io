cigma: A Pure Python Filetype Identification Library
====================================================
date: 22/Nov/2015
summary: Cigma is a minimal, pure Python filetype identification library I created as an alternative to various Python ports of libmagic that are floating around.
tags: code

Filetype identification is the process of scanning [respective](https://en.wikipedia.org/wiki/Magic_number_%28programming%29) [magicbytes](https://en.wikipedia.org/wiki/List_of_file_signatures) for each filetype within input streams. The mapping for various filetypes and their magicbytes are stored in different formats which is then queried by the identification library. If a match is found, input stream is classified to be of that type. In case of match collisions, a signature preference logic prioritizes matches. Tools like [TrID](http://mark0.net/soft-trid-e.html) and [others](http://www.forensicswiki.org/wiki/File_Format_Identification) use similar logic.

[cigma](https://github.com/7h3rAm/cigma) is a Python library to identify filetypes. It provides [libmagic](https://github.com/threatstack/libmagic) like mimetype identification of a file or data buffer. This is similar to what the `file` command on *nix systems will provide:

```shell
$ file cigma.py
cigma.py: Python script, ASCII text executable
$
$ file readme.md
readme.md: Python script, ASCII text executable, with very long lines
$
$ file /bin/ls
/bin/ls: ELF 64-bit LSB  executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=9d2a434c4ff55aad2ddd19348c0ac75971606483, stripped
$
$ file /etc/passwd
/etc/passwd: ASCII text
$
$ file /dev/sda
/dev/sda: block special
```

`cigma` uses a custom JSON formatted signature file to stores filetype mappings. Let's try identifying a few files:

```shell
$ python cigma.py /bin/ls
('/bin/ls',
 {'id': 29,
  'longname': 'Executable and Linkable Format (ELF)',
  'mimetype': 'application/x-executable',
  'patterns': [{'offset': 0, 'regex': '\\x7F\\x45\\x4C\\x46', 'size': 4}],
  'shortname': 'ELF'})
$
$ python cigma.py ~/toolbox/testfiles/binary/suspicious/35d249cdd501aeb5a5b39daeb4f275c41c73e91ef299a094d27edbfd0396715d.VXE
('/home/shiv/toolbox/testfiles/binary/suspicious/35d249cdd501aeb5a5b39daeb4f275c41c73e91ef299a094d27edbfd0396715d.VXE',
 {'id': 31,
  'longname': 'Windows Executable',
  'mimetype': 'application/x-dosexec',
  'patterns': [{'offset': 0, 'regex': '\\x4D\\x5A', 'size': 2}],
  'shortname': 'EXE'})
$
$ python cigma.py ~/toolbox/testfiles/pcaps/exploitkits/2015-04-03-Nuclear-EK-traffic.pcap
('/home/shiv/toolbox/testfiles/pcaps/exploitkits/2015-04-03-Nuclear-EK-traffic.pcap',
 {'id': 5,
  'longname': 'Packet Capture (winpcap)',
  'mimetype': 'application/vnd.tcpdump.pcap',
  'patterns': [{'offset': 0, 'regex': '\\xD4\\xC3\\xB2\\xA1', 'size': 4}],
  'shortname': 'PCAP'})
```

If a match is found, `cigma` returns a `(source, resultdict)` tuple. Here is a snippet of few signatures from the current set:

```json
{
  "meta": {
    "rulescount": 72,
    "version": 0.1
  },
  "rules": [
    {
      "id": 1,
      "longname": "PKZIP",
      "mimetype": "application/octet-stream",
      "patterns": [
        {
          "offset": 0,
          "regex": "\\x50\\x4B\\x05\\x06",
          "size": 4
        }
      ],
      "shortname": "ZIP"
    },
    {
      "id": 5,
      "longname": "Packet Capture (winpcap)",
      "mimetype": "application/vnd.tcpdump.pcap",
      "patterns": [
        {
          "offset": 0,
          "regex": "\\xD4\\xC3\\xB2\\xA1",
          "size": 4
        }
      ],
      "shortname": "PCAP"
    },
    {
      "id": 27,
      "longname": "Flash Video",
      "mimetype": "video/x-flv",
      "patterns": [
        {
          "offset": 0,
          "regex": "\\x46\\x4C\\x56",
          "size": 3
        }
      ],
      "shortname": "FLV"
    },
    {
      "id": 29,
      "longname": "Executable and Linkable Format (ELF)",
      "mimetype": "application/x-executable",
      "patterns": [
        {
          "offset": 0,
          "regex": "\\x7F\\x45\\x4C\\x46",
          "size": 4
        }
      ],
      "shortname": "ELF"
    }
  ]
}
```

Adding a new signature is really easy. Just edit the included `magicbytes.json` file and add a new node with an unique `id`. Each node should have a `patterns` list which should contain the `offset`, `regex` and `size` keys with respective values.

Using `cigma` as a library is really easy:

```python
from cigma import Cigma
```

One this is done, you can identify a file buffer:

```python
with open("/home/shiv/toolbox/testfiles/binary/crafted_corkami/gui.exe") as fo:
  filedata = fo.read()

Cigma(data=filedata).cigma()
('databuffer',
 {'longname': 'Windows Executable',
  'mimetype': 'application/x-dosexec',
  'patterns': [{'offset': 0, 'regex': '\\x4D\\x5A', 'size': 2}],
  'shortname': 'EXE'})
```

Or else you can also identify a file itself:

```python
Cigma(filename="/home/shiv/toolbox/testfiles/binary/crafted_corkami/gui.exe").cigma()
('/home/shiv/toolbox/testfiles/binary/crafted_corkami/gui.exe',
 {'longname': 'Windows Executable',
  'mimetype': 'application/x-dosexec',
  'patterns': [{'offset': 0, 'regex': '\\x4D\\x5A', 'size': 2}],
  'shortname': 'EXE'})
```

The primary purpose of `cigma` is to be able to identify mundane files at lightning speeds. It doesn't aim to provide exhaustive insight into each file by parsing and decoding it. Currently, there are 70+ signatures and identification for more filetypes will be available as the project grows.