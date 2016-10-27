#!/usr/bin/env python

import sys
import nids

end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)

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
