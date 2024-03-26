# Homework6 Wireshark Lab

## Description

Install WiresharkLinks to an external site. on your computer. Do the lab as in "Wireshark_DNS_v8.0.pdf" at the "files" section. Answer all questions, but do not take screenshots. Submit answers as a single file in plain text.

## Answer

1. Run *nslookup* to obtain the IP address of a Web server in Asia. What is the IP address of that server?

   Run command `nslookup scu.edu.cn` and the ip address is 202.115.32.43

2. Run *nslookup* to determine the authoritative DNS servers for a university in Europe.

​	Run command: `nslookup -type=NS cam.ac.uk`, and the answer:

​	Non-authoritative answer:

​	cam.ac.uk	nameserver = auth0.dns.cam.ac.uk.

​	cam.ac.uk	nameserver = dns0.eng.cam.ac.uk.

​	cam.ac.uk	nameserver = ns3.mythic-beasts.com.

​	cam.ac.uk	nameserver = dns0.cl.cam.ac.uk.

​	cam.ac.uk	nameserver = ns2.ic.ac.uk.

​	cam.ac.uk	nameserver = ns1.mythic-beasts.com.

3. Run *nslookup* so that one of the DNS servers obtained in Question 2 is queried for the mail servers for Yahoo! mail. What is its IP address?

​	mta7.am0.yahoodns.net	internet address = 67.195.228.111

​	mta7.am0.yahoodns.net	internet address = 67.195.204.77

​	mta7.am0.yahoodns.net	internet address = 67.195.204.79

​	mta7.am0.yahoodns.net	internet address = 67.195.228.110

​	mta7.am0.yahoodns.net	internet address = 67.195.228.109

​	mta7.am0.yahoodns.net	internet address = 98.136.96.91

​	mta7.am0.yahoodns.net	internet address = 67.195.204.73

​	mta7.am0.yahoodns.net	internet address = 67.195.228.106

Note :It was discovered that most European university (I tried five universities) DNS servers refuse external queries, making it impossible to directly query them for Yahoo's mail servers. The practical approach is to use `nslookup -type=MX yahoo.com` for MX records, then `nslookup` on the hostnames to get their IPs. This two-step method bypasses the need for querying university DNS servers, which often restrict such external inquiries for security reasons.



4. Locate the DNS query and response messages. Are then sent over UDP or TCP?

   UDP

   

5. What is the destination port for the DNS query message? What is the source port

of DNS response message?

​	Destination port for DNS query message: 53

​	Source port for DNS response: 53



6. To what IP address is the DNS query message sent? Use ipconfig to determine the

IP address of your local DNS server. Are these two IP addresses the same?

​	Destination IP address for DNS query message: 75.75.75.75

​	Local DNS server IP address by ipconfig: 75.75.75.75

​	These two IP addresses are the same.



7. Examine the DNS query message. What “Type” of DNS query is it? Does the

query message contain any “answers”?

​	There are three 'Type' of DNS query: A, AAAA, HTTPS

​	All the DNS query message don't contain any "answers"



8. Examine the DNS response message. How many “answers” are provided? What

do each of these answers contain?

​	For DNS query with Type A, there are two answers in the 'Answers' field as follow:

```bash
Answers
    www.ietf.org: type A, class IN, addr 104.16.45.99
        Name: www.ietf.org
        Type: A (1) (Host Address)
        Class: IN (0x0001)
        Time to live: 129 (2 minutes, 9 seconds)
        Data length: 4
        Address: 104.16.45.99
    www.ietf.org: type A, class IN, addr 104.16.44.99
        Name: www.ietf.org
        Type: A (1) (Host Address)
        Class: IN (0x0001)
        Time to live: 129 (2 minutes, 9 seconds)
        Data length: 4
        Address: 104.16.44.99
```

​	

For DNS query with Type AAAA, there are two answers in the 'Answers' field as follow:

```bash
Answers
    www.ietf.org: type AAAA, class IN, addr 2606:4700::6810:2d63
        Name: www.ietf.org
        Type: AAAA (28) (IP6 Address)
        Class: IN (0x0001)
        Time to live: 300 (5 minutes)
        Data length: 16
        AAAA Address: 2606:4700::6810:2d63
    www.ietf.org: type AAAA, class IN, addr 2606:4700::6810:2c63
        Name: www.ietf.org
        Type: AAAA (28) (IP6 Address)
        Class: IN (0x0001)
        Time to live: 300 (5 minutes)
        Data length: 16
        AAAA Address: 2606:4700::6810:2c63
```

​	For DNS query with Type HTTPS, there are only one answer in the 'Answers' field as follow:

```bash
www.ietf.org: type HTTPS, class IN
            Name: www.ietf.org
            Type: HTTPS (65) (HTTPS Specific Service Endpoints)
            Class: IN (0x0001)
            Time to live: 300 (5 minutes)
            Data length: 61
            SvcPriority: 1
            TargetName: <Root>
            SvcParam: alpn=h3,h2
                SvcParamKey: alpn (1)
                SvcParamValue length: 6
                ALPN length: 2
                ALPN: h3
                ALPN length: 2
                ALPN: h2
            SvcParam: ipv4hint=104.16.44.99,104.16.45.99
                SvcParamKey: ipv4hint (4)
                SvcParamValue length: 8
                IP: 104.16.44.99
                IP: 104.16.45.99
            SvcParam: ipv6hint=2606:4700::6810:2c63,2606:4700::6810:2d63
                SvcParamKey: ipv6hint (6)
                SvcParamValue length: 32
                IP: 2606:4700::6810:2c63
                IP: 2606:4700::6810:2d63
```



9. Consider the subsequent TCP SYN packet sent by your host. Does the destination IP address of the SYN packet correspond to any of the IP addresses provided in the DNS response message?

   YES.

   Explain: This is because the SYN packet is part of the TCP three-way handshake used to establish a TCP connection, and the destination IP address for this connection is obtained from the DNS resolution process



10. This web page contains images. Before retrieving each image, does your host
    issue new DNS queries?

    No.

    Explain: the host does not necessarily issue new DNS queries before retrieving each image on a web page. If the DNS entries for the image sources are already cached and valid, the host will use the cached information. New DNS queries are only issued if the domain names of the images are not in the cache or if the cache entries have expired



11. What is the destination port for the DNS query message? What is the source port of DNS response message?

    Destination port for DNS query message: 53

    Source port for DNS response: 53



12. To what IP address is the DNS query message sent? Is this the IP address of your default local DNS server?

​	Destination IP address for DNS query message: 75.75.75.75

​	Local DNS server IP address by ipconfig: 75.75.75.75

​	These two IP addresses are the same.



13. Examine the DNS query message. What “Type” of DNS query is it? Does the query message contain any “answers”?

​	There are two 'Type' of DNS query: A, AAAA

​	All the DNS query message don't contain any "answers"



14. Examine the DNS response message. How many “answers” are provided? What do each of these answers contain?

​	For DNS query with Type A, there are three answers in the 'Answers' field as follow:

	 Answers
	    www.mit.edu: type CNAME, class IN, cname www.mit.edu.edgekey.net
	        Name: www.mit.edu
	        Type: CNAME (5) (Canonical NAME for an alias)
	        Class: IN (0x0001)
	        Time to live: 1372 (22 minutes, 52 seconds)
	        Data length: 25
	        CNAME: www.mit.edu.edgekey.net
	    www.mit.edu.edgekey.net: type CNAME, class IN, cname e9566.dscb.akamaiedge.net
	        Name: www.mit.edu.edgekey.net
	        Type: CNAME (5) (Canonical NAME for an alias)
	        Class: IN (0x0001)
	        Time to live: 34 (34 seconds)
	        Data length: 24
	        CNAME: e9566.dscb.akamaiedge.net
	    e9566.dscb.akamaiedge.net: type A, class IN, addr 23.56.123.79
	        Name: e9566.dscb.akamaiedge.net
	        Type: A (1) (Host Address)
	        Class: IN (0x0001)
	        Time to live: 7 (7 seconds)
	        Data length: 4
	        Address: 23.56.123.79



​	For DNS query with Type AAAA, there are four answers in the 'Answers' foe;d as follow:

	  Answers
	    www.mit.edu: type CNAME, class IN, cname www.mit.edu.edgekey.net
	        Name: www.mit.edu
	        Type: CNAME (5) (Canonical NAME for an alias)
	        Class: IN (0x0001)
	        Time to live: 1800 (30 minutes)
	        Data length: 25
	        CNAME: www.mit.edu.edgekey.net
	    www.mit.edu.edgekey.net: type CNAME, class IN, cname e9566.dscb.akamaiedge.net
	        Name: www.mit.edu.edgekey.net
	        Type: CNAME (5) (Canonical NAME for an alias)
	        Class: IN (0x0001)
	        Time to live: 16 (16 seconds)
	        Data length: 24
	        CNAME: e9566.dscb.akamaiedge.net
	    e9566.dscb.akamaiedge.net: type AAAA, class IN, addr 2600:1406:3a00:786::255e
	        Name: e9566.dscb.akamaiedge.net
	        Type: AAAA (28) (IP6 Address)
	        Class: IN (0x0001)
	        Time to live: 14 (14 seconds)
	        Data length: 16
	        AAAA Address: 2600:1406:3a00:786::255e
	    e9566.dscb.akamaiedge.net: type AAAA, class IN, addr 2600:1406:3a00:789::255e
	        Name: e9566.dscb.akamaiedge.net
	        Type: AAAA (28) (IP6 Address)
	        Class: IN (0x0001)
	        Time to live: 14 (14 seconds)
	        Data length: 16
	        AAAA Address: 2600:1406:3a00:789::255e



16. To what IP address is the DNS query message sent? Is this the IP address of your default local DNS server?

    Destination IP address for DNS query message: 75.75.75.75

    Local DNS server IP address by ipconfig: 75.75.75.75

    These two IP addresses are the same.

    

17. Examine the DNS query message. What “Type” of DNS query is it? Does the query message contain any “answers”?

​	There are three 'Type' of DNS query: NS

​	The DNS query message don't contain any "answers"



18. Examine the DNS response message. What MIT nameservers does the response message provide? Does this response message also provide the IP addresses of the MIT namesers?

​	The DNS response message contained the following information in its 'Answers' field:

	 Answers
	    mit.edu: type NS, class IN, ns usw2.akam.net
	    mit.edu: type NS, class IN, ns use2.akam.net
	    mit.edu: type NS, class IN, ns use5.akam.net
	    mit.edu: type NS, class IN, ns ns1-173.akam.net
	    mit.edu: type NS, class IN, ns asia1.akam.net
	    mit.edu: type NS, class IN, ns ns1-37.akam.net
	    mit.edu: type NS, class IN, ns asia2.akam.net
	    mit.edu: type NS, class IN, ns eur5.akam.net

​	

​	It also provided the corresponding IP addresses of the nameservers in its 'Additional records' field as follow:

	Additional records
	    asia1.akam.net: type A, class IN, addr 95.100.175.64
	    asia2.akam.net: type A, class IN, addr 95.101.36.64
	    eur5.akam.net: type A, class IN, addr 23.74.25.64
	    usw2.akam.net: type A, class IN, addr 184.26.161.64
	    use2.akam.net: type A, class IN, addr 96.7.49.64
	    use5.akam.net: type A, class IN, addr 2.16.40.64
	    use5.akam.net: type AAAA, class IN, addr 2600:1403:a::40



20. To what IP address is the DNS query message sent? Is this the IP address of your default local DNS server? If not, what does the IP address correspond to?

​	The DNS query message destination IP address: 18.72.0.3

​	The IP address is not the default local DNS server. It is correspond to 'bitsy.mit.edu' DNS server IP address.



21. Examine the DNS query message. What “Type” of DNS query is it? Does the query message contain any “answers”?

​	The DNS query message waas with Type A. It did'nt contain any "Answers"



23. Examine the DNS response message. How many “answers” are provided? What does each of these answers contain?

​	Only one answers are provided as follow:

	  Answers
	    www.aiit.or.kr: type A, class IN, addr 218.36.94.200
	        Name: www.aiit.or.kr
	        Type: A (1) (Host Address)
	        Class: IN (0x0001)
	        Time to live: 3338 (55 minutes, 38 seconds)
	        Data length: 4
	        Address: 218.36.94.200

