Visualizing (non-POSIX) Regular Expressions
===========================================
date: 27/Nov/2013
summary: This post details the steps involved in visualizing a (non-POSIX) regular expression using Finite State Automata.
tags: code

I recently came across the
[pyFSA](http://www.osteele.com/software/python/fsa/) project and played
with it for sometime. It includes a built-in API to render finite state
machines as [dotstring](http://www.graphviz.org/doc/info/lang.html).
Regular expressions can be represented as FSMs and then be rendered to a
dot-string for visual introspection. I quickly wrote a proof-of-concept
tool to implement this idea and hence
[re2dotgraph](https://github.com/7h3rAm/re2dotgraph) was born.

First, the pyFSA module has to be installed. Download the package, unzip
it and follow the standard Python module installation steps:

```console
$ python setup.py build
running build
running build_py
creating build
creating build/lib.linux-x86_64-2.7
copying FSA.py -> build/lib.linux-x86_64-2.7
copying NumFSAUtils.py -> build/lib.linux-x86_64-2.7
copying FSChartParser.py -> build/lib.linux-x86_64-2.7
copying reCompiler.py -> build/lib.linux-x86_64-2.7
$
$ sudo python setup.py install
running install
running build
running build_py
running install_lib
copying build/lib.linux-x86_64-2.7/FSChartParser.py -> /usr/local/lib/python2.7/dist-packages
copying build/lib.linux-x86_64-2.7/FSA.py -> /usr/local/lib/python2.7/dist-packages
copying build/lib.linux-x86_64-2.7/reCompiler.py -> /usr/local/lib/python2.7/dist-packages
copying build/lib.linux-x86_64-2.7/NumFSAUtils.py -> /usr/local/lib/python2.7/dist-packages
byte-compiling /usr/local/lib/python2.7/dist-packages/FSChartParser.py to FSChartParser.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/FSA.py to FSA.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/reCompiler.py to reCompiler.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/NumFSAUtils.py to NumFSAUtils.pyc
running install_data
warning: install_data: setup script did not provide a directory for 'README.txt' -- installing right in '/usr/local'

copying README.txt -> /usr/local
warning: install_data: setup script did not provide a directory for 'LICENSE.txt' -- installing right in '/usr/local'

error: can't copy 'LICENSE.txt': doesn't exist or not a regular file
```

Ignore the `LICENSE.txt` copy error. Now you need to install the
`graphviz` package which includes the `dot` tool useful in rendering
`.dot` files into images. Once the dependencies are successfully
installed, you can use `re2dotgraph` and test it with a sample regex:

```console
$ ./re2dotgraph.py 'a*b?c+'

[+] Generating dot string ...
[+] Label: a*b?c+
[+] states: [0, 1, 2]
[+] states count: 3
[+] initialState: 0
[+] finalStates: [2]
[+] alphabet: None
[+] transitions:
        (0, 0, <CharacterSet a>)
        (0, 1, <CharacterSet b>)
        (0, 2, <CharacterSet c>)
        (1, 2, <CharacterSet c>)
        (2, 2, <CharacterSet c>)

[+] Generating dot graph ...
[+] regex: 'a*b?c+' -> regex.png
```

The input regex is represented using a FSM which is then rendered to a
`dot` file. This `dot` file is then rendered to an image name
`regex.png` (name can be changed by passing a custom value as the second
argument) using the installed `dot` program, called natively from inside
Python runtime using the `os.system` method. Here is how the graph looks
like:

![image](/static/files/regex1.png)

I would like to point out that representing regular expressions as FSMs
is really tricky. There are certain aspects of a regex that can never be
represented (like backreferences and lookaheads) due to the fact that
FSMs don't have memory to keep note of what was matched previously. This
highlights the fact that any regexes, with backreferences or lookaheads
won't be rendered correctly. Also, the pyFSA page mentions that the
project currently is not fully compliant with POSIX regex guidelines.
This severely limits the real-world use-cases:

```console
$ ./re2dotgraph.py 'a\dc'

[+] Generating dot string ...
[+] Label: a\dc
[+] states: [2, 0, 3, 1]
[+] states count: 4
[+] initialState: 0
[+] finalStates: [3]
[+] alphabet: None
[+] transitions:
        (0, 1, <CharacterSet a>)
        (1, 2, <CharacterSet \d>)
        (2, 3, <CharacterSet c>)

[+] Generating dot graph ...
[+] regex: 'a\dc' -> regex.png
```

And here's the generated image:

![image](/static/files/regex2.png)

As is evident from the above image, the `\d` escape sequence was not
identified and the graph as such is incorrect. However, this still is an
interesting project and a really easy way of visualizing regular
expressions. For POSIX compliant solutions, refer these projects:
[RegExVis](http://regexvisualizer.apphb.com/),
[Debuggex](https://www.debuggex.com/) and [Regexper](http://www.regexper.com/)

You can get the source files through the project repository on [GitHub](https://github.com/7h3rAm/re2dotgraph).
