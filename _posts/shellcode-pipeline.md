Shellcode Analysis Pipleine
===========================
date: 18/Mar/2014
summary: This post shows how to create an automated shellcode analysis pipeline where shellcode is sourced from public portals and tested using multiple analysis engines. It provides an automated way of testing the accuracy of detection engines like Libemu/Snort/Suricata/Bro against publicly available shellcode.
tags: code, reversing

## Introduction

I recently required an automated way of analyzing shellcode and verifying if it is detected by [Libemu](http://libemu.carnivore.it/), [Snort](http://www.snort.org/), [Suricata](http://suricata-ids.org/), [Bro](https://www.bro.org/), etc. Shellcode had to come from public sources like [ShellStorm](http://repo.shell-storm.org/shellcode/), [ExploitDB](http://www.exploit-db.com/shellcode/) and [Metasploit](https://github.com/rapid7/metasploit-framework/tree/master/modules/payloads). I needed an automated way of sourcing shellcode from these projects and pass it on to the analysis engines in a pipeline-like mechanism. This posts documents the method I used to complete this task and the overall progress of the project.

## Design Considerations

I basically divided the project into three independent tasks:

- source shellcode from shell-storm, exploit-db and metasploit
- generate pcaps for obtained shellcode
- test shellcode with Libemu and pcaps with Snort/Suricata/Bro

These are independent since any of them can be used individually, as a unit, and developed outside of the system. The first task itself was divided into smaller sub-tasks and I started with sourcing shellcode from shell-storm. The shell-storm shellcode page documents steps needed to access shell-storm database and there is an example script that provides an easy to use cli to search for and download individual shellcode files from shell-storm. I used this script in my project and added a wrapper over it to search, download and generate pcaps all with just one cli invocation. The script currently is in beta and satisfies only a few of the above requirements. Shell-storm sourcing is implemented, pcap generation is working and shellcode testing currently happens with Libemu only. Additional sources and analysis engines would be added shortly.

## Implementation and Testing

Please visit the following link to get the complete source listing: [sap](https://gist.github.com/7h3rAm/11087025)

It will read configuration file to populate internal variables and then move on to its core. First, the `doshellstorm()` method is called to source shellcode samples from shell-storm. The API example script is used to search shellcode that satisfies certain search criteria and then matching shell-storm shellcode ids are downloaded, extracted and saved to a `<shellcode-id>.bin` named file. For all shellcode ids for which we successfully extracted shellcode bytes, they are then passed onto the `bin2pcap()` method which uses an updated version of [PCAPGGenerationTTools](https://github.com/7h3rAm/PCAP-Generation-Tools) and creates pcap files with HTTP GET/POST requests and [TCP CTS/STC](https://github.com/7h3rAm/PCAP-Generation-Tools/commit/fc7418eefc9febef936d4646c61bad67e26935b7) sessions. These pcaps can then be tested with intrusion detection engines in the pipeline. Once the pcap generation module completes, the Libemu engine is invoked and run over all `.bin` shellcode files. Later versions will add support for Snort/Suricata/Bro based shellcode pcap testing.

Let's have a look at the help message from the tool:

```
$ ./sap.py -h
sap.py - Shellcode Analysis Pipleline (v0.1)
Ankur Tyagi (7h3rAm)

[18-Mar-2014 20:55:17.441063 IST] [main] [NORM]: Session started @ 2014-04-19 20:55:17.440964
usage: sap.py [-h] [-v] [-s SEARCH] [-c CONFIG] [-d] [-S] [-E] [-M] [-p]

sap.py - Shellcode Analysis Pipleline

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s SEARCH, --search SEARCH
                        shellcode search
  -c CONFIG, --config CONFIG
                        config file - default: sap.cnf
  -d, --debug           enable debug output
  -S, --shellstorm      shellstorm lookup
  -E, --exploitdb       exploitdb lookup
  -M, --metasploit      metasploit lookup
  -p, --genpcaps        generate pcaps

EXAMPLE: sap.py -s windows
```

There are no mandatory options since most of them are read from the config file if not available on the command-line. The tool supports explicit lookup for shell-storm, exploitdb or metasploit projects. Pcap generation has to be explicitly requested but it will be inherently skipped if no bin files are not created for obtained shellcode. Let's have a test run of the tool with `arm` as the search string to test only ARM shellcode available at Shell-Storm:

```
$ ./sap.py -s arm -d
sap.py - Shellcode Analysis Pipleline (v0.1)
Ankur Tyagi (7h3rAm)

[18-Mar-2014 20:54:22.829518 IST] [main] [NORM]: Session started @ 2014-04-19 20:54:22.829437
[18-Mar-2014 20:54:22.830968 IST] [main] [DEBUG]: Using ./sap.cnf as configuration file
[18-Mar-2014 20:54:22.831149 IST] [main] [DEBUG]: Using 'arm' as search string
[18-Mar-2014 20:54:22.831204 IST] [main] [DEBUG]: Enabled all shellcode soruces: shellstorm/exploitdb/metasploit
[18-Mar-2014 20:54:23.434474 IST] [doshellstorm] [NORM]: Found 26 shellcode ids @ shell-storm with search-string: 'arm'
[18-Mar-2014 20:54:23.748633 IST] [doshellstorm] [NORM]: (001/026) Wrote 196B from shellcode id#661 into ./661.bin
[18-Mar-2014 20:54:24.066123 IST] [doshellstorm] [NORM]: (002/026) Wrote 151B from shellcode id#735 into ./735.bin
[18-Mar-2014 20:54:24.390874 IST] [doshellstorm] [NORM]: (003/026) Skipped shellcode id#669 as only 0B found!
[18-Mar-2014 20:54:24.706150 IST] [doshellstorm] [NORM]: (004/026) Wrote 72B from shellcode id#670 into ./670.bin
[18-Mar-2014 20:54:25.016058 IST] [doshellstorm] [NORM]: (005/026) Skipped shellcode id#754 as only 0B found!
[18-Mar-2014 20:54:25.324224 IST] [doshellstorm] [NORM]: (006/026) Wrote 78B from shellcode id#671 into ./671.bin
[18-Mar-2014 20:54:25.637873 IST] [doshellstorm] [NORM]: (007/026) Wrote 53B from shellcode id#765 into ./765.bin
[18-Mar-2014 20:54:25.960882 IST] [doshellstorm] [NORM]: (008/026) Wrote 40B from shellcode id#659 into ./659.bin
[18-Mar-2014 20:54:26.269648 IST] [doshellstorm] [NORM]: (009/026) Wrote 44B from shellcode id#820 into ./820.bin
[18-Mar-2014 20:54:26.584585 IST] [doshellstorm] [NORM]: (010/026) Skipped shellcode id#853 as only 0B found!
[18-Mar-2014 20:54:26.888214 IST] [doshellstorm] [NORM]: (011/026) Skipped shellcode id#854 as only 0B found!
[18-Mar-2014 20:54:27.214914 IST] [doshellstorm] [NORM]: (012/026) Skipped shellcode id#666 as only 0B found!
[18-Mar-2014 20:54:27.528852 IST] [doshellstorm] [NORM]: (013/026) Skipped shellcode id#855 as only 0B found!
[18-Mar-2014 20:54:27.852626 IST] [doshellstorm] [NORM]: (014/026) Wrote 24B from shellcode id#668 into ./668.bin
[18-Mar-2014 20:54:28.156066 IST] [doshellstorm] [NORM]: (015/026) Skipped shellcode id#696 as only 0B found!
[18-Mar-2014 20:54:28.477319 IST] [doshellstorm] [NORM]: (016/026) Skipped shellcode id#665 as only 0B found!
[18-Mar-2014 20:54:28.799106 IST] [doshellstorm] [NORM]: (017/026) Skipped shellcode id#819 as only 0B found!
[18-Mar-2014 20:54:29.112905 IST] [doshellstorm] [NORM]: (018/026) Skipped shellcode id#0 as only 0B found!
[18-Mar-2014 20:54:29.440574 IST] [doshellstorm] [NORM]: (019/026) Skipped shellcode id#667 as only 0B found!
[18-Mar-2014 20:54:29.748897 IST] [doshellstorm] [NORM]: (020/026) Wrote 27B from shellcode id#698 into ./698.bin
[18-Mar-2014 20:54:30.070085 IST] [doshellstorm] [NORM]: (021/026) Skipped shellcode id#821 as only 0B found!
[18-Mar-2014 20:54:30.384414 IST] [doshellstorm] [NORM]: (022/026) Wrote 20B from shellcode id#660 into ./660.bin
[18-Mar-2014 20:54:30.701548 IST] [doshellstorm] [NORM]: (023/026) Skipped shellcode id#729 as only 0B found!
[18-Mar-2014 20:54:31.006583 IST] [doshellstorm] [NORM]: (024/026) Skipped shellcode id#730 as only 0B found!
[18-Mar-2014 20:54:31.313406 IST] [doshellstorm] [NORM]: (025/026) Skipped shellcode id#728 as only 0B found!
[18-Mar-2014 20:54:31.709741 IST] [doshellstorm] [NORM]: (026/026) Skipped shellcode id#727 as only 0B found!
[18-Mar-2014 20:54:31.710338 IST] [main] [DEBUG]: Initiating Libemu testing for downloaded shellcode
[18-Mar-2014 20:54:31.710862 IST] [emutest] [NORM]: (001/010) Testing shellcode file: ./661.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.711142 IST] [emutest] [NORM]: (002/010) Testing shellcode file: ./735.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.711392 IST] [emutest] [NORM]: (003/010) Testing shellcode file: ./670.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.711687 IST] [emutest] [NORM]: (004/010) Testing shellcode file: ./671.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.711952 IST] [emutest] [NORM]: (005/010) Testing shellcode file: ./765.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.712189 IST] [emutest] [NORM]: (006/010) Testing shellcode file: ./659.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.712427 IST] [emutest] [NORM]: (007/010) Testing shellcode file: ./820.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.712659 IST] [emutest] [NORM]: (008/010) Testing shellcode file: ./668.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.712890 IST] [emutest] [NORM]: (009/010) Testing shellcode file: ./698.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.713120 IST] [emutest] [NORM]: (010/010) Testing shellcode file: ./660.bin with Libemu: offset = -1
[18-Mar-2014 20:54:31.713370 IST] [main] [NORM]: Session completed in 0:00:08.883860
```

I enabled `debug` output for additional verbosity in the above command-line. The tool identified 26 shellcode samples that satisfy search criteria `arm`. From these 26 samples, only 10 could be converted to `.bin` equivalents via the regex pattern and these were then passed on to the Libemu analysis engine. Those familiar with Libemu will immediately notice that all of these 10 tested shellcode samples, `offset` was found to be -1 which indicates that Libemu failed in identification of these as probable shellcode candidates. The offset value returned by the `shellcode_getpc_test()` method should ideally be 0 or more to indicate the starting offset inside the input buffer from where the actual shellcode starts. Since Libemu only supports x86 architecture, all the 10 ARM shellcode samples were bound to fail in the above test.

Let's now try a Windows x86 shellcode with the tool:

```
$ ./sap.py -s download
sap.py - Shellcode Analysis Pipleline (v0.1)
Ankur Tyagi (7h3rAm)

[18-Mar-2014 21:32:39.954426 IST] [main] [NORM]: Session started @ 2014-04-19 21:32:39.954321
[18-Mar-2014 21:32:40.501316 IST] [doshellstorm] [NORM]: Found 14 shellcode ids @ shell-storm with search-string: 'download'
[18-Mar-2014 21:32:40.821984 IST] [doshellstorm] [NORM]: (001/014) Wrote 278B from shellcode id#240 into ./240.bin
[18-Mar-2014 21:32:41.130703 IST] [doshellstorm] [NORM]: (002/014) Wrote 202B from shellcode id#162 into ./162.bin
[18-Mar-2014 21:32:41.436970 IST] [doshellstorm] [NORM]: (003/014) Skipped shellcode id#150 as only 0B found!
[18-Mar-2014 21:32:41.760507 IST] [doshellstorm] [NORM]: (004/014) Skipped shellcode id#700 as only 0B found!
[18-Mar-2014 21:32:42.089636 IST] [doshellstorm] [NORM]: (005/014) Wrote 151B from shellcode id#206 into ./206.bin
[18-Mar-2014 21:32:42.402426 IST] [doshellstorm] [NORM]: (006/014) Skipped shellcode id#392 as only 0B found!
[18-Mar-2014 21:32:42.712811 IST] [doshellstorm] [NORM]: (007/014) Wrote 110B from shellcode id#59 into ./59.bin
[18-Mar-2014 21:32:43.025814 IST] [doshellstorm] [NORM]: (008/014) Wrote 108B from shellcode id#862 into ./862.bin
[18-Mar-2014 21:32:43.333005 IST] [doshellstorm] [NORM]: (009/014) Wrote 79B from shellcode id#616 into ./616.bin
[18-Mar-2014 21:32:43.649846 IST] [doshellstorm] [NORM]: (010/014) Wrote 75B from shellcode id#227 into ./227.bin
[18-Mar-2014 21:32:43.949659 IST] [doshellstorm] [NORM]: (011/014) Wrote 42B from shellcode id#611 into ./611.bin
[18-Mar-2014 21:32:44.257083 IST] [doshellstorm] [NORM]: (012/014) Skipped shellcode id#767 as only 0B found!
[18-Mar-2014 21:32:44.582001 IST] [doshellstorm] [NORM]: (013/014) Skipped shellcode id#146 as only 0B found!
[18-Mar-2014 21:32:44.885040 IST] [doshellstorm] [NORM]: (014/014) Skipped shellcode id#159 as only 0B found!
[18-Mar-2014 21:32:44.885900 IST] [emutest] [NORM]: (001/008) Testing shellcode file: ./240.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.927295 IST] [emutest] [NORM]: (002/008) Testing shellcode file: ./162.bin with Libemu: offset = 0
[2014-03-18 21:32:44] Downloading  (C:\U.exe)
[2014-03-18 21:32:44] Error while downloading from
HMODULE LoadLibraryA (
     LPCTSTR = 0x0244d020 =>
           = "urlmon.dll";
) =  0x7df20000;
HRESULT URLDownloadToFile (
     LPUNKNOWN = 0x02452f50 =>
         none;
     LPCTSTR = 0x0244e8f0 =>
           = "";
     LPCTSTR = 0x02453fb0 =>
           = "C:\U.exe";
     DWORD dwReserved = 0;
     LPBINDSTATUSCALLBACK lpfnCB = 0;
) =  0x800c0008;
UINT WINAPI WinExec (
     LPCSTR = 0x023b4940 =>
           = "C:\U.exe";
     UINT uCmdShow = 1972065515;
) =  0x20;
void ExitProcess (
     UINT uExitCode = 0;
) =  0x0;

[18-Mar-2014 21:32:44.955295 IST] [emutest] [NORM]: (003/008) Testing shellcode file: ./206.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955390 IST] [emutest] [NORM]: (004/008) Testing shellcode file: ./59.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955462 IST] [emutest] [NORM]: (005/008) Testing shellcode file: ./862.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955535 IST] [emutest] [NORM]: (006/008) Testing shellcode file: ./616.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955597 IST] [emutest] [NORM]: (007/008) Testing shellcode file: ./227.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955655 IST] [emutest] [NORM]: (008/008) Testing shellcode file: ./611.bin with Libemu: offset = -1
[18-Mar-2014 21:32:44.955725 IST] [main] [NORM]: Session completed in 0:00:05.001388
```

Id 162 was successfully identified by Libemu as shellcode and it even generated the profiling output for it. From the profile output it seems like the shellcode, when executed, will trigger the download and execution of a malware sample. This is also evident from the shellcode description provided by shell-storm for this shellcode id:

```
$ shell-storm-api.py -search download
Connecting to shell-storm.org...
Found 14 shellcodes
ScId    Size Title
[240]   278  Solaris/mips - download and execute - 278 bytes
[162]   226  Windows - download & exec shellcode - 226 bytes+ <-- SCID: 162
[150]   218  Windows-64 - (URLDownloadToFileA) download and execute - 218+ bytes
[700]   164  Windows - null-free 32-bit Windows download and LoadLibrary shellcode - 164 bytes
[206]   149  Linux/x86 - connect back, download a file and execute - 149 bytes
[392]   124  Windows - download and execute - 124 bytes
[59]    111  Linux/x86 - HTTP/1.x GET, Downloads & execve() - 111 bytes+
[862]   108  Linux/x86 - Download + chmod + exec - 108 bytes
[616]   79   Solaris/x86 - Remote Download file - 79 bytes
[227]   68   Linux/x86 - HTTP/1.x GET, Downloads and JMP - 68 bytes+
[611]   42   Linux/x86 - Remote file Download - 42 bytes
[767]   n/a  Windows - Vista/7/2008 - download and execute file via reverse DNS channel
[146]   n/a  Windows - XP download and exec source
[159]   n/a  Windows - Download and Execute Shellcode Generator
```

## Conclusion

Currently Libemu is the only analysis engine but soon I'll be adding support for additional engines. Sourcing from other projects will also be added in subsequent versions. Feel free to try it out and let me know what you think of it.
