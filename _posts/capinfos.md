capinfos.py: Pure Python Pcap Statistics Tool
=============================================
date: 2/Aug/2015
summary: This post introduces a pure-Python way of parsing a pcap file and generating statistics like capinfos tool from Wireshark.
tags: code

## Introduction

The [capinfos](https://www.wireshark.org/docs/man-pages/capinfos.html) tool from Wireshark parses a pcap file and displays useful statistics like packet count, bitrate, byterate, capture duration, etc. I needed a pure-Python parser to obtain these details and ended up with the following code:

```python
from pprint import pprint
import datetime
import struct
import sys

def capinfos(filename):
  # generates wireshark's capinfos like stats
  # limited features
  # needs additional testing
  file_handle = open(filename, 'rb')
  data = file_handle.read()
  pcapstats = dict()
  endianness = None
  datalink_types = {
    0: 'DLT_NULL',
    1: 'DLT_EN10MB',
    2: 'DLT_EN3MB',
    3: 'DLT_AX25',
    4: 'DLT_PRONET',
    5: 'DLT_CHAOS',
    6: 'DLT_IEEE802',
    7: 'DLT_ARCNET',
    8: 'DLT_SLIP',
    9: 'DLT_PPP',
    10: 'DLT_FDDI',
    18: 'DLT_PFSYNC',
    105: 'DLT_IEEE802_11',
    113: 'DLT_LINUX_SLL',
    117: 'DLT_PFLOG',
    127: 'DLT_IEEE802_11_RADIO'
  }
  # extract pcap magic using host's native endianess
  (pcap_magic, ) = struct.unpack('=I', data[:4])
  # if the pcap is LE
  if pcap_magic == 0xa1b2c3d4:
    (pcap_magic, pcap_version_major, pcap_version_minor, pcap_thiszone, pcap_sigfigs, pcap_snaplen, pcap_network) = struct.unpack('<IHHIIII', data[:24])
    endianness = 'LITTLE'
  # if the pcap is BE
  elif pcap_magic == 0xd4c3b2a1:
    (pcap_magic, pcap_version_major, pcap_version_minor, pcap_thiszone, pcap_sigfigs, pcap_snaplen, pcap_network) = struct.unpack('>IHHIIII', data[:24])
    endianness = 'BIG'
  # for pcaps which are something else (0x4d3c2b1a)?
  else:
    return pcapstats
  starttime = None
  endtime = None
  s = 24
  e = s + 16
  packetscount = 0
  bytescount = 0
  while True:
    if endianness is 'LITTLE':
      (ts_sec, ts_usec, incl_len, orig_len) = struct.unpack('<IIII', data[s:e])
    elif endianness is 'BIG':
      (ts_sec, ts_usec, incl_len, orig_len) = struct.unpack('>IIII', data[s:e])
    packetscount += 1
    bytescount += incl_len
    if not starttime:
      starttime = datetime.datetime.fromtimestamp(ts_sec)
      bytescount += incl_len
    endtime = datetime.datetime.fromtimestamp(ts_sec)
    s = e + incl_len
    e = s + 16
    if e > len(data):
      break
  totsecs = int((endtime - starttime).total_seconds())
  if totsecs < 1:
    totsecs = 1
  pcapstats['totsecs'] = totsecs
  pcapstats['pcapmagic'] = '0x%08X' % pcap_magic
  pcapstats['version_major'] = pcap_version_major
  pcapstats['version_minor'] = pcap_version_minor
  pcapstats['snaplen'] = pcap_snaplen
  pcapstats['pcapencapsulation'] = datalink_types[pcap_network]
  pcapstats['packetscount'] = packetscount
  pcapstats['bytescount'] = bytescount
  pcapstats['capturestarttime'] = starttime.strftime('%c').strip()
  pcapstats['captureendtime'] = endtime.strftime('%c').strip()
  pcapstats['captureduration'] = (endtime - starttime).total_seconds()
  byterate = (bytescount / totsecs) if totsecs > 0 else bytescount
  bitrate = ((bytescount * 8) / totsecs) if totsecs > 0 else (bytescount * 8)
  pcapstats['byterate'] = byterate
  pcapstats['bitrate'] = bitrate
  avgpacketsize = (bytescount / packetscount) if packetscount > 0 else bytescount
  avgpacketrate = (packetscount / totsecs) if totsecs > 0 else packetscount
  pcapstats['avgpacketsize'] = avgpacketsize
  pcapstats['avgpacketrate'] = avgpacketrate
  return dict(pcapstats)


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "USAGE: %s <filename>" % (sys.argv[0])
    sys.exit(1)

  pprint(capinfos(sys.argv[1]))
```

## Usage

Let's try this script on a HTTP pcap:

```
$ python capinfos.py /media/shiv/red_third/stoolbox/testfiles/pcaps/layer7/http_espn.pcap
{
 'avgpacketrate': 478,
 'avgpacketsize': 682,
 'bitrate': 2609012,
 'byterate': 326126,
 'bytescount': 652253,
 'captureduration': 2.0,
 'captureendtime': 'Wed Apr  7 22:59:31 2010',
 'capturestarttime': 'Wed Apr  7 22:59:29 2010',
 'packetscount': 956,
 'pcapencapsulation': 'DLT_EN10MB',
 'pcapmagic': '0xA1B2C3D4',
 'snaplen': 65535,
 'totsecs': 2,
 'version_major': 2,
 'version_minor': 4
}
```

## Conclusion

The script accepts a pcap file as input and natively parse its structure to calculate required values. As can be seen in the output file, it shows a quick summary of statistics which could be quite useful for scripting and automation or to have a quick overview of input file. You can get this script [here](https://gist.github.com/7h3rAm/225e36ad59729000e00e7814e9644622).
