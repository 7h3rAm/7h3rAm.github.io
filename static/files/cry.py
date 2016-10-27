#!/usr/bin/env python

import sys, re, mmap
import requests
from PIL import Image


# download and save a file
def das(baseurl, filename):
    resp = requests.get("%s/%s" % (baseurl, filename), verify=False)
    if not resp.ok:
        print("[-] Download failed! Exiting.")
        sys.exit(1)
    else:
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        f.close()


# extract key file from webpage
def xtractKey(webpage, keyfile):
    # mmap webpage and find offset of embedded png file
    f = open(webpage, 'r+b')
    m = mmap.mmap(f.fileno(), 0)
    m.seek(0)
    r = re.compile(r'\x89PNG\x0D\x0A.*', re.MULTILINE|re.DOTALL)
    r = re.search(r, m)
    m.close()
    f.close()

    # read png data and save it to keyfile
    with open(webpage, 'r+b') as f:
        f.seek(r.start())
        pngbuf = f.read(r.end())
    f.close()

    k = open(keyfile, 'wb')
    k.write(pngbuf)
    k.close()


# basefile xor keyfile
def xorImg(conf):
    # x, y (width, height) offsets for keyfile
    w, h = 0, 0

    # loop over basefile width
    for x in range(0, conf['imx']):

        # loop over basefile height
        for y in range(0, conf['imy']):

            # wrap keyfile width if max reached
            if x % conf['kyx'] == 0: w = 0
            # wrap keyfile height if max reached
            if y % conf['kyy'] == 0: h = 0

            # read color values for current pixel in basefile
            conf['imr'], conf['img'], conf['imb'] = conf['impix'][x, y]
            # read color values for current pixel in keyfile
            conf['kyr'], conf['kyg'], conf['kyh'], conf['kyw'] = conf['kypix'][w, h]

            # basefile[red]   XOR keyfile[red]
            conf['otr'] = conf['imr'] ^ conf['kyr']
            # basefile[green] XOR keyfile[green]
            conf['otg'] = conf['img'] ^ conf['kyg']
            # basefile[blue]  XOR keyfile[blue]
            conf['otb'] = conf['imb'] ^ conf['kyh']

            # update outfile with XOR'd RGB values
            conf['otpix'][x, y] = (conf['otr'], conf['otg'], conf['otb'])

            #print "impix[%d, %d] = %s" % (x, y, conf['impix'][x, y])
            #print "kypix[%d, %d] = %s" % (w, h, conf['kypix'][w, h])
            #print "otpix[%d, %d] = %s" % (x, y, conf['otpix'][x, y])
            #print

            # move to next row
            h += 1

        # move to next column
        w += 1

# populate conf n call xor method
def main():
    conf = {}

    conf['baseurl'] = "https://googledrive.com/host/0B7WgiVv_ihnhX1VRWHVXZmZmMW8"
    conf['webpage'] = "challengeWebpage.html"
    conf['filename'] = "cryptImg.png"

    conf['keyfile'] = "key.png"
    conf['outfile'] = "decoded.png"

    print("\n[+] Downloading challenge webpage: %s%s ..." % (conf['baseurl'], conf['webpage']))
    das(conf['baseurl'], conf['webpage'])

    print("[+] Downloading basefile: %s/%s ..." % (conf['baseurl'], conf['filename']))
    das(conf['baseurl'], conf['filename'])

    print("[+] Extracting keyfile: %s ..." % (conf['keyfile']))
    xtractKey(conf['webpage'], conf['keyfile'])

    conf['im'] = Image.open(conf['filename'])
    conf['impix'] = conf['im'].load()

    conf['ky'] = Image.open(conf['keyfile'])
    conf['kypix'] = conf['ky'].load()

    conf['ot'] = Image.open(conf['filename'])
    conf['otpix'] = conf['ot'].load()

    conf['immode'] = conf['im'].mode
    (conf['imx'], conf['imy']) = conf['im'].size

    conf['kymode'] = conf['ky'].mode
    (conf['kyx'], conf['kyy']) = conf['ky'].size

    print("\n[+] %s: (%s, %s)" % (conf['filename'], conf['im'].mode, conf['im'].size))
    print("[+] %s: (%s, %s)\n" % (conf['keyfile'], conf['ky'].mode, conf['ky'].size))
    print("[+] Decoding basefile: %s XOR keyfile: %s ..." % (conf['filename'], conf['keyfile']))
    xorImg(conf)
    conf['ot'].save(conf['outfile'])
    print("[+] Decoding complete! Saved to %s: (%s, %s)\n" % (conf['outfile'], conf['ot'].mode, conf['ot'].size))
    conf['ot'].show()


if __name__ == "__main__":
    main()
