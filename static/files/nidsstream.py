#!/usr/bin/env python

import sys
import nids

end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)

def printable(data):
    print ''.join([ch for ch in data if ord(ch) > 31 and ord(ch) < 126
            or ord(ch) == 9
            or ord(ch) == 10
            or ord(ch) == 13
            or ord(ch) == 32])

def tcpcallback(tcp):
    if tcp.nids_state == nids.NIDS_JUST_EST:
        ((src, sport), (dst, dport)) = tcp.addr
        tcp.client.collect = 1
        tcp.server.collect = 1

    elif tcp.nids_state == nids.NIDS_DATA:
        tcp.discard(0)

    elif tcp.nids_state in end_states:
        ((src, sport), (dst, dport)) = tcp.addr
        print "[+] %s:%s - %s:%s (CTS: %dB | STC: %dB)" % (src, sport, dst, dport, 
                len(tcp.server.data[:tcp.server.count]),
                len(tcp.client.data[:tcp.client.count]))
        print
        printable(tcp.server.data)
        printable(tcp.client.data[:333])

def main():
    if len(sys.argv) == 2:
        nids.param("filename", sys.argv[1])

    nids.init()
    nids.register_tcp(tcpcallback)

    try:
        nids.run()
    except nids.error, e:
        print "[-] Error: %s" % (e)
    except Exception, e:
        print "[-] Exception: %s" % (e)

if __name__ == '__main__':
    main()
