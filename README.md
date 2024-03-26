This is code repository for SCU 2023Winter CSEN233 Network

# HW1 Numerical Services

This  is a group assignment.  Find your partner(s).

With provide "csen233intro.tar", unpack several Python modules, including udpPack.py.

It is a combined "client/server" module.  With your partner, separate the functionality into two Python modules "udpPackServer.py" and "udpPackClient.py".

Design, with your partner, the data exchange format and error handling logic so that:

+ Server starts first and wait for connection.
+ Client to request “numerical services” from Server by sending two integers and an “operator” that's one of  "+, -, *, /".
+ Server to carry out the operation and send back the answer
+ Client print out the answer and end connection



# HW2 HTTP Client

Write a Python program that fetches an object from a web server.  This is not a group assignment.  Code on your own.

1. Study Python's built-in "logging" module.  Use it in the program.
2. Connect to an URL on port 80 with socket using TCP.  (Hint: pick a "simple" web site that produce simple HTML contents.  Note that we are not yet ready to do "HTTP/S" connection yet.)
3. Construct an HTTP request, format as described in textbook, and send and fetch content.

Submit source code only.

If you wish, install "wireshark" and observe the bits going back-and-forth with a standard browser.  You may gain some insight on what was exactly requested and what came back from the other side.  Wireshark is a good skill to acquire.

All I expect is you to fetch an object from a random and external web server.  I don't expect you to do anything to that object, including displaying it, let alone checking if that object is of any good.  This means you must keep on trying if the server respond with an error.

The key output that I expect is the logs your program generates.  I will run your program, terminate it, and examine the logs.



# HW3 Simple Network Auction Bake-off

Implement Simple Network Auction and prepared to field test with other teams.  Submit your code prior to the class.  Minimally, the server code must log to a file with sufficient information to understand the auction sequences.  (What if a client dispute the outcome?  You would have the logs to stand your ground.)

We will conduct a round of "bake-off" for everyone's implementation for the selected protocol design.  We will do so in the class with each team electing one computer connecting to the ECC.  There will be, therefore, 6 nodes on the same network.

One team, at a time, will be the auctioneer and the other will be the bidders.  After each auction, everyone terminates the session.  Then we restart with another team being the auctioneer.

Scoring:

1. A client get one point for successfully submitting any bid.
2. An auctioneer get one point for the receipt of any bid from a client and delivering an acknowledgement.
3. Auctioneer get one point for having a winning bid.  And another point for each bidder who receives the result of the auction.

The protocol designer get 10 points for all 6 teams having greater than zero point.



# HW5 Zero Knowledge Key Exchange

Study [Diffie-Hellman algorithmLinks to an external site.](https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange). The wikipedia link is not the totality of Diffie-Hellman description.  You should reach an understanding level to be able to explain to a layman how this algorithm works and why it is secure.  Implement a protocol that your team designs and do key exchanges with your partner.  (For group with three members, do 3 pair-wise attempts.)

The idea is not to achieve security, but for you to understand a zero-knowledge key exchange concept.  It is not for you to generate a cryptographically strong encryption key.  Do not make lives complicated unnecessarily.

Do "simple Diffie-Hellman".  Do not try the more secure versions.  Do only "two-party key exchange."  The length, in terms of number of digits, for the final shared secret is not a consideration for this homework.

This homework is then:

+ Design a key exchange protocol.  It should be a "one pager."
+ Each person on the team to implement the protocol separately.
+ Test implementations with your team members.  Revise protocol as you see fit.
+ Submit the protocol doc (in PDF or plain text), all members' code, and all members' log files.  Package the submission as one zip/tar file that unpack into one directory that's compliant to the guidelines.

**Failure to be compliant to the submission guidelines will lose 30% of the credits from now on.  Test your packaging before you submit.**



# HW6 Wireshark Lab

[Install WiresharkLinks to an external site.](https://www.wireshark.org/download.html) on your computer.  Do the lab as in "Wireshark_DNS_v8.0.pdf" at the "files" section.  Answer all questions, but do not take screenshots.  Submit answers as a single file in plain text.



# HW7 Dijkstra Shortest Path

Given a network topology described in the JSON file "net.json", find the shortest path (minimal costs) for two nodes within that network.  

**The provided base code for a "network emulator" was inspired from p.444 of the text book.  This code base will be reused for future assignments. You are expected to modify or fix any bugs it as you see fit.  I highly recommend adding logging facility.**

1. Unpack "dijkstra.tar" into your working directory. 
2. You are to modify "dijkstra.py" and implement the "dijkstra" function to generate the shortest path from one router to another.  Create new files if wish.
3. The provide code takes 3 command-line inputs: the topology files and two router names.  (It's not necessary to use "argparse".)  The "main" portion of the code takes the return path from your code.  Modify the file to output the shortest path, in as a list of router names, to stdout.

Note: The Python function **reInit** in the module "netemulate.py" will load the topology file and construct a "network" accordingly.  The emulated network has a list of "routers" each with several "links" that are its direct neighbors and the "cost" of transmission.



# HW8 FIB

nderstand the relationship between "routing" and "forwarding."

Use the code from the previous Dijkstra homework, update the "fib" for each router on the path.  Test by sending a "packet" from the origin to the destination of the shortest path.  Also do negative test by sending another packet from a node to another without fib entries to connect them.

+ Based on the code from Dijkstra homework, add a "fib" data structure to the "router" class representing the "forwarding table."  You can use whatever datastructure for fib.  Usually, it is a "table" of 2 or 3 columns.  The first is the name of the destination (in real world, that will be the IP address.  For this class, it is the name of the destination router.)  The second column is the "link" leading to a neighboring, directly connected, router, also known as the "next hop."  The rest of the table is optional.  I recommend keeping track of the "total cost" to reach the destination.  E.g.: An entry of ('R35', <router object>, 10) means to deliver a packet to the router "R35", the packet should be forwarded to the router object of the tuple and the final cost to reach there is 10.
+ Initialize each router with a fib table consisting of only its directly linked neighbors.  (At this point, the link table and fib look very similar.)
+ Run Dijkstra computation for two random notes.  Add a fib entry into each of the router on the path.  (It is, therefore, a good thing to have an "updateFib" method for the router class.)
+ Send a packet from the first node of the above shortest path to the last node.  Do this by first implementing "sendData" and "recvData" methods to the router class.
  + "sendData" accepts a destination router name (as string) and a data, presumed to be a string.  It consults the FIB table to see if the destination router is present.  If so, it first encapsulates the data into a "packet" by prefixing a header that has, minimally, the destination's name.  After the encapsulation, it calls the "recvData" of the next-hop router object to deliver the packet.  If its FIB table does not have such entry, drop the packet.  Log the event no matter what happened to the data.

In pseudo-code:

```
def sendData(self, dest, data):
    if dest in self.fib:
        destRouter = self.fib[dest]
        packet=encapsulate(dest, data)
        destRouter.recvData(self.name, packet)
    else:
        dropPkt()
```

+ + "recvData" accept a packet from the caller and decapsulate it to understand the final destination.  If the data is meant of itself, it is simply accepted. Otherwise, it uses its own "sendData" method to handle that. the packet header for the final destination of this packet.  If it is for the receiving router, the data is accepted.  Acceptance means logging such event and discarding the packet.

```
# called by the sender
def recvData(self, src, dest, packet, travel=0):
    header, data = unpack(packet)
    if header.destination == myself:
        dropPkt()
    else
        sendData(header.dest, data)
```

+ Write a function (in "main" area) to test both positive and negative case as in the beginning of the assignment.

Submit code and log files.



# Extra1 AES Encryption with Diffie Hellman Key

Install "crypto" package from the internet (pip install pycrypto) and implement encryption and description as a separate module,  (i.e.: A Python file on its own).  After you have done with key exchange, pad the shared secret to the desired key length, then use the shared secret as a key to encrypt a message into a ciphertext, Decrypt the ciphertext back to plaintext.

As an option, send the ciphertext your HW5 partner and persuade him/her to decrypt on his/her side.  Submit both code and log file as a single zip/tar file.

25% if you do this as an individual.  Additional 5% if your partner participates and successfully decrypt the ciphertext.  (The partner credit is applied only once, even if both sides choose to do this extra credit assignment.)



# Extra2 Knapsack Encryption

This is a group project for 2 members. Find your own parter.

1. Study [Knapsack EncryptionLinks to an external site.](https://en.wikipedia.org/wiki/Merkle–Hellman_knapsack_cryptosystem). Write a function to generate a "super-increasing" knapsack of "n" elements, then another one to transform it to a non-super-increasing one.
2. Use the above as "key pair", transmit the public key to your partner.  Upon receipt of such key, the partner transmits an encrypted message back to you to decrypt with your private key.  Verify the result.
3. Use log files as proof of success.  (Set at "INFO" level for your final run before submission.)  Make sure to include partner ID in your source files.
4. Co-write an one-pager (in either PDF or plain text) on the vulnerability of this encryption algorithm.
5. Submit source files, log files, and one pager.



# Extra4 Minimum Spanning Tree (MST)

Same as Disjkstra (HW7), construct a minimum spanning tree starting from a random node at the network.  (Create a new file "mst.py" in similar style as disjktra.py.)

Choose whichever MST algorithm you wish.  (I suggest [Kruskal'sLinks to an external site.](https://en.wikipedia.org/wiki/Kruskal's_algorithm).)  Output the spanning tree in a human readable form.  Submit source code and log for a successful run.

