Northrop's Online Challenge
===========================
date: 27/Mar/2014
summary: This is a writeup for the /reddit/netsec's Q1 2014 Information Security Hiring Thread challenge posted by Northrop Grumman Cyber Intelligence Division.
tags: code, ctf

## Introduction

A while back I was checking out the [/r/netsec's Q1 2014 Information Security Hiring Thread](http://www.reddit.com/r/netsec/comments/1ubzv9/rnetsecs_q1_2014_information_security_hiring/) at Reddit and there I found an interesting challenge posted by someone from Northrop Grumman Cyber Intelligence Division. They were looking for people with interesting skills (IDS/IPS, Big Data, web app development, etc.) and mentioned that candidates solving their [online challenge](https://googledrive.com/host/0B7WgiVv_ihnhX1VRWHVXZmZmMW8/challengeWebpage.html) will be preferred. I find such challenges really interesting and immediately got on top of it. A few hours later I solved it and decided to write about the process. This post details steps I took and lessons learned.

## Research and Testing

The online challenge page looks something like this:

![onlinechallenge.png](/static/files/posts_northrop_challenge/onlinechallenge.png.webp)

It includes a `.png` image which, as mentioned, contains a hidden message that has to be found to solve the challenge. Here is the challenge image for your reference:

![cryptImg.png](/static/files/posts_northrop_challenge/cryptImg.png.webp)

The first thing I did upon opening up this page was looking at its source. In there I found an `iframe` with a `png` file embedded in it. The `iframe` had a comment preceding it: `A frame for my key`. This suggested that the embedded image is a key of some kind that has to be used in the challenge. I immediately extracted it and here it is (in actual dimensions: 128x96):

![key.png](/static/files/posts_northrop_challenge/key.png.webp)

There was also a hint in the page, a link to [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/), which suggested that some image manipulation would be needed to find the hidden message. Before exploring the python library I thought of spending some time with the challenge image itself, though not exactly sure of what I was looking for. The image seemed to have sections in it, actually a grid like structure, comprising of 5x5 cells (ie. a total of 25 sections). Interestingly, the key image is exactly 1/5th the size of challenge image. I immediately had the idea that the base image might be mutated with key image operating on each of its 25 sections individually. This mutation created a seemingly gibberish image with lots of noise but failed to hide the algorithm's cellular structure. The only unknown at this time was the mutation algorithm, which I assumed to be XOR. I immediately crafted a poc to test this hypothesis. It downloads the `.html` webpage, the `.png` challenge image, extract `.png` key file and performs a XOR between the challenge and the key image, on a per cell fashion, rounding up the start of each cell with the start of the key file. Once this operation is completed over all 25 cells, the decoded image will be saved as a `.png` to disk. Here is a test run:

```python
$ ./cry.py

[+] Downloading challenge webpage: https://googledrive.com/host/0B7WgiVv_ihnhX1VRWHVXZmZmMW8challengeWebpage.html ...
[+] Downloading basefile: https://googledrive.com/host/0B7WgiVv_ihnhX1VRWHVXZmZmMW8/cryptImg.png ...
[+] Extracting keyfile: key.png ...

[+] cryptImg.png: (RGB, (640, 480))
[+] key.png: (RGBA, (128, 96))

[+] Decoding basefile: cryptImg.png XOR keyfile: key.png ...
[+] Decoding complete! Saved to decoded.png: (RGB, (640, 480))
```

And here is the `decoded.png` image file:

![decoded.png](/static/files/posts_northrop_challenge/decoded.png.webp)

## Conclusion

This indeed was an interesting challenge and a one that proved to be good source of learning. Stay tuned for more writeups on similar topics.
