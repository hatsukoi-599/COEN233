# Homework2 HTTP Client

## Description

Write a Python program that fetches an object from a web server. This is not a group assignment. Code on your own.

Study Python's built-in "logging" module. Use it in the program.
Connect to an URL on port 80 with socket using TCP. (Hint: pick a "simple" web site that produce simple HTML contents. Note that we are not yet ready to do "HTTP/S" connection yet.)
Construct an HTTP request, format as described in textbook, and send and fetch content.
Submit source code only.

If you wish, install "wireshark" and observe the bits going back-and-forth with a standard browser. You may gain some insight on what was exactly requested and what came back from the other side. Wireshark is a good skill to acquire.

All I expect is you to fetch an object from a random and external web server. I don't expect you to do anything to that object, including displaying it, let alone checking if that object is of any good. This means you must keep on trying if the server respond with an error.

The key output that I expect is the logs your program generates. I will run your program, terminate it, and examine the logs.
