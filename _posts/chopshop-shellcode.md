Shellcode Detection Module in ChopShop
======================================
date: 12/Mar/2015
summary: This post shows a shellcode detection module that I submitted to MITRECND's ChopShop Protocol Analysis/Decoder Framework.
tags: code, shellcode

Around an year ago I submitted a pull request to the [ChopShop](https://github.com/MITRECND/chopshop) project from [MITRECND](https://github.com/MITRECND). This request included a module that enabled shellcode detection for TCP streams and UDP packets. In this post I'll show how to use this module to identify shellcode within network streams. Here's the project description:

> ChopShop is a MITRE developed framework to aid analysts in the creation and execution of pynids based decoders and detectors of APT tradecraft.

It provides reliable network stream reassembly via libnids and provides an API to write plugins/modules that can operate upon the reassembled network data. The project is in active development since September 2012 and numerous interesting modules have been added to it recently.

Last year I submitted a [shellcode detection module](https://github.com/MITRECND/chopshop/pull/29) that was merged in the project with few changes. This module leverages ChopShop APIs to obtain network data and inspects it using [Libemu to check if it contains shellcode](http://7h3ram.github.io/2013/libemu-shellcode-detection.html). I got this idea while working on one of my projects, [Flowinspect](http://7h3ram.github.io/2014/flowinspect.html), which includes shellcode detection and other interesting ways of identifying suspicious network traffic.

To invoke ChopShop you need to provide a pcapfile as input and then a list of modules to be invoked. Each module can be provided respective arguments as well. Let's have a look at the command line invocation and usage of the shellcode module:

```shell
$ ./chopshop -f ~/toolbox/testfiles/pcaps/shellcode/shellcode-winexec-calc.pcap "shellcode_detector -xp"
Starting ChopShop
Initializing Modules ...
    Initializing module 'shellcode_detector'
Running Modules ...
[2015-03-12 23:31:31 IST]  TCP 56.86.97.100:57416 - 89.86.105.74:80 [NEW]
[2015-03-12 23:31:31 IST]  TCP 56.86.97.100:57416 -> 89.86.105.74:80 (CTS: 123B)
[2015-03-12 23:31:31 IST]  TCP 56.86.97.100:57416 <- 89.86.105.74:80 (STC: 227B)
[2015-03-12 23:31:31 IST]  TCP 56.86.97.100:57416 - 89.86.105.74:80 contains shellcode in STC[0:227] @ offset 107

0000000: e8 44 00 00 00 8b 45 3c 8b 7c 05 78 01 ef 8b 4f  |.D....E<.|.x...O|
0000010: 18 8b 5f 20 01 eb 49 8b 34 8b 01 ee 31 c0 99 ac  |.._ ..I.4...1...|
0000020: 84 c0 74 07 c1 ca 0d 01 c2 eb f4 3b 54 24 04 75  |..t........;T$.u|
0000030: e5 8b 5f 24 01 eb 66 8b 0c 4b 8b 5f 1c 01 eb 8b  |.._$..f..K._....|
0000040: 1c 8b 01 eb 89 5c 24 04 c3 5f 31 f6 60 56 64 8b  |.....\$.._1.`Vd.|
0000050: 46 30 8b 40 0c 8b 70 1c ad 8b 68 08 89 f8 83 c0  |F0.@..p...h.....|
0000060: 6a 50 68 f0 8a 04 5f 68 98 fe 8a 0e 57 ff e7 63  |jPh..._h....W..c|
0000070: 61 6c 63 2e 65 78 65 00                          |alc.exe.        |


UINT WINAPI WinExec (
     LPCSTR = 0xc00f6f10 =>
           = "calc.exe";
     UINT uCmdShow = 0;
) =  0x20;
LPTOP_LEVEL_EXCEPTION_FILTER SetUnhandledExceptionFilter (
     LPTOP_LEVEL_EXCEPTION_FILTER = 0xc00f7190 =>
         none;
) =  0x7c81cdda;

Shutting Down Modules ...
    Shutting Down shellcode_detector
Module Shutdown Complete ...
ChopShop Complete
```

In the above example, ChopShop was invoked to execute the `shellcode_detector` module with its `-p` and `-x` arguments. The output confirms that shellcode was found in the STC stream of input pcap at offset 107. The module then display a hexdump of shellcode bytes as well as a profiled output highlighting the Windows API calls, arguments and their return types. This output is extremely useful as it tells that the shellcode will spawn a `calc.exe` process if it is successfully deployed on the victim system.

You can also have a look at the module [sourcecode](https://github.com/MITRECND/chopshop/blob/master/modules/shellcode_detector.py). I would strongly recommend reading the [project documentation](https://github.com/MITRECND/chopshop/tree/master/docs/chopshop_docs) to familiarize yourself with architecture and terminology. Also checkout the [module authoring documentation](https://github.com/MITRECND/chopshop/blob/master/docs/chopshop_docs/module_authoring.md) and [this](http://www.mitre.org/capabilities/cybersecurity/overview/cybersecurity-blog/how-chopshop-modules-work) amazing post by [Wesley Shields](https://github.com/wxsBSD), who is one of the project authors, if you wish to write your own modules.