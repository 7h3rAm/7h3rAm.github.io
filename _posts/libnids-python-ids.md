Developing a Minimal IPS from Scratch
=====================================
date: 15/Sep/2013
summary: What do you get when you combine a TCP/IP reassembly/defragmentation library with Python's re module? Read on to know more.
tags: code

## Introduction

In this post I'll try to explain how [pynids](https://jon.oberheide.org/pynids/) can be combined with Python's `re` module to develop a minimal IPS-like tool. In an earlier post, [Network Stream Reassembly and Defragmentation](https://7h3ram.github.io/posts/20130618_libnids-pynids.html), I talked about how to leverage pynids API to create a TCP reassembly module. I would suggest you read that post before continuing further since I'll be skipping over reassembly basics. First let's understand the architecture of a very basic IPS:

![image](/static/files/posts_libnids_python_ids/minips-arch.png.webp)

Since it is a prevention system, an IPS has to be placed inline between the firewall at the perimeter edge the default gateway of your network. For any sessions that match inspection rules, they will be either dropped or logged or both if required. This action is basically per session/match configurable and can be changed through system's policy files. An inspection system needs network traffic as input and this input can come from different sources but for the sake of simplicity, we'll only be focusing on packet capture files and direct network device access as sources of input. Once the input is available in the form of raw packets, the system will need to reassemble them and extract layer payload which an inspection engine can consume.

Rule/Signature based inspection engines use custom variants of the PCRE engine specifically optimized for performance and throughput. These engines use different techniques for performing string matches, either using native implementations of proven algorithms like [Aho Corasick](http://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_string_matching_algorithm), [Boyer Moore](http://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string_search_algorithm), [Rabin Karp](http://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_string_search_algorithm), etc. [Finite State Automaton](http://en.wikipedia.org/wiki/Finite-state_machine) is also used in some implementations. In this post, we'll be using Libnids to extract TCP streams/UDP packets and match user-supplied regular expressions over this data. If a match is found, we'll log details and optionally drop the connection.

## Design Considerations

Before we begin with development, let's design the pseudocode for our IPS:

```
1. initialize nids
2. register udp callback
3. register tcp callback
4. invoke nids session
5. for udp packet:
  5.1. extract source/destination and identify flow details
  5.2. extract payload and pass on to inspection engine
  5.3. if match found:
    5.3.1 dump source/destination details to output device/file
    5.3.2 dump match statistics to output device/file
6. for tcp packet:
  6.1 identify current tcp state
  6.2 if new connection:
    6.2.1 add source/destination to session table
    6.2.2 request cts/stc data collection from libnids
  6.3 elif existing connection with data:
    6.3.1 identify direction
    6.3.2 extract payload and pass on to inspection engine
    6.3.3 if match found:
      6.3.3.1 dump source/destination details to output device/file
      6.3.3.2 dump match statistics to output device/file
      6.3.3.3 stop cts/stc data collection
  6.4 elif existing connection with closing tcp sequence:
    6.4.1 stop cts/stc data collection
7. for each inspection request:
  7.1 match user-supplied regex over input data
  7.2 if match found:
    7.2.1 return match statistics
```

## Implementation and Testing

Please have a look at the [minips.py](https://gist.github.com/7h3rAm/10974463) program which implements the above pseudo code.

It will inspect each TCP and UDP packet and for matching TCP streams, stop tracking it any further. This is a performance optimization feature with an understanding that if a stream matches certain regex, it is the one the user intended to find. There is no need to inspect additional data in the stream since it already has what the user intended to find. This is only true for TCP streams as for UDP there is no stream/flow and as such inspection always happens on a per-packet basis.

For streams/packets that match input expression, match direction (only for TCP matches), start/end of match inside input buffer, match size etc are dumped along with a hexdump of the matching content. To limit the size of the hexdump output, a cli option is added. Regular expression engine's match behavior can be tweaked to enable case insensitive and multiline matches using cli options.

Here is a test run of this program on a pcap that contains HTTP session and UDP packets:

```
$ python minips.py -p ~/toolbox/testfiles/pcaps/http.cap -r '.*com'
[15-Sep-2013 15:03:02.341813 IST] TCP 145.254.160.237:3372 - 65.208.228.223:80 (NEW)
[15-Sep-2013 15:03:02.341903 IST] TCP 145.254.160.237:3372 - 65.208.228.223:80 (CTS: 479B | STC: 0B)
[15-Sep-2013 15:03:02.341946 IST] TCP 145.254.160.237:3372 - 65.208.228.223:80 matches regex '.*com' @ CTS[29:51] 22B
00000000: 48 6f 73 74 3a 20 77 77 77 2e 65 74 68 65 72 65  |Host: www.ethere|
00000010: 61 6c 2e 63 6f 6d                                |al.com|

[15-Sep-2013 15:03:02.342179 IST] UDP 145.254.160.237:3009 - 145.253.2.203:53 (47B)
[15-Sep-2013 15:03:02.342210 IST] UDP 145.254.160.237:3009 - 145.253.2.203:53 matches regex '.*com' @ [0:42] 42B
00000000: 00 23 01 00 00 01 00 00 00 00 00 00 07 70 61 67  |.#...........pag|
00000010: 65 61 64 32 11 67 6f 6f 67 6c 65 73 79 6e 64 69  |ead2.googlesyndi|
00000020: 63 61 74 69 6f 6e 03 63 6f 6d                    |cation.com|

[15-Sep-2013 15:03:02.342439 IST] UDP 145.253.2.203:53 - 145.254.160.237:3009 (146B)
[15-Sep-2013 15:03:02.342479 IST] UDP 145.253.2.203:53 - 145.254.160.237:3009 matches regex '.*com' @ [0:42] 42B
00000000: 00 23 81 80 00 01 00 04 00 00 00 00 07 70 61 67  |.#...........pag|
00000010: 65 61 64 32 11 67 6f 6f 67 6c 65 73 79 6e 64 69  |ead2.googlesyndi|
00000020: 63 61 74 69 6f 6e 03 63 6f 6d                    |cation.com|
```

The program correctly identified regex match over the TCP stream in the CTS (client-to-server) direction and dumped match statistics along with matching content. The regex might have matched on the STC payload as well but when the first match on this stream was found, the program stopped tracking it any further and since that match was on CTS direction, any payload following it was never seen. For UDP matches, note that for the same flow, there are two matches: one while the data is being sent from a client at UDP/3009 to server at `UDP/53` and again when the server replied to the client. Since, there are no flow details for a UDP session, any such program won't have an implicit knowledge of the direction towards which payload is forwarded. However, it is not trivial to implement such functionality in the UDP callback enabling it to identify the client and server sides of the connection and then taking appropriate action.

## Conclusion

The `inspect` function currently only includes regex matches as the only source of inspection over TCP/UDP payload but this can be extended to add really interesting capabilities like [shellcode detection](https://7h3ram.github.io/posts/20130306_libemu-shellcode-detection.html), [Yara](http://code.google.com/p/yara-project/) rule matching, [Fuzzy String](https://github.com/seatgeek/fuzzywuzzy) matching, file identification, file type based inspection, hash matching, javascript extraction, deobfuscation, emulation and analysis, etc. I've been working on a project which implements a few of these capabilities in addition to various other nifty features desirable from such inspection tools. Check it out @ [flowinspect](https://github.com/7h3rAm/flowinspect). The `minips.py` program can also be extended to read input regex from a flat file and match them in sequence over input packets. This will allow the user to inspect network flows using multiple regexes, enabling true IPS-like matching functionality.
