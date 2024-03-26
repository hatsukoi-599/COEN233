# Homework3

## Description

Design an application-level protocol for network auctioning. This is a group assignment. No late submission will be accepted for this homework.

The protocol should facilitate simple auditioning carried out over the internet. The auctioneer has one item to sell. It opens an auction and accepts "bids" from clients who may join the auction anytime after the opening. Each client may submit "bids" while the auction is still open. The bid minimally has the price they are willing to pay for the item. The server will broadcast to all clients for the current highest bid every 10 seconds. If there was no more bids after 3 such broadcastings, the highest bid that was above the undisclosed minimum wins the auction.

State your assumptions for anything not covered above.

Submit your "protocol design", in PDF or plain text, to Camino.

Your design should include these elements:

Which transport service (TCP or UDP) to use? For this homework, you may assume the transport layer services are "reliable." That means the messages will always be delivered, without error, and with reasonable latency.
How to "discover"? This means how would one side find out and connect to the other side? While discovery is a common design issue that can be complex, for this homework, you should make it simple. For this homework, there is no need to authenticate the clients.

If you choose to adopt the "client/server" model, state so. Otherwise, describe your high-level operational model.

The formats/structure of the messages the client(s) and server exchanges. Typically, also how would each side changes its state when messages were sent/received. There is no need to draw state-transition diagrams.

Reasonable error handlings beyond stated in this homework text..

You should write as if you are giving instructions to a team to implement the protocol. They may use a language that you are not familiar with. Their program may also run computers or operating systems that you don't know well. Assume the skill level similar to who are in this class. You should also assume different teams will develop client and server sides.

Try to limit your document to 2 pages. Long documents are frown upon.

At the class following the due day, prepare to present your protocol design to the class in 10 minutes. I will put your material to Camino first. Elect a member as the presenter. Slide deck is encouraged but not required.
Implement Simple Network Auction and prepared to field test with other teams. Submit your code prior to the class. Minimally, the server code must log to a file with sufficient information to understand the auction sequences. (What if a client dispute the outcome? You would have the logs to stand your ground.)

We will conduct a round of "bake-off" for everyone's implementation for the selected protocol design. We will do so in the class with each team electing one computer connecting to the ECC. There will be, therefore, 6 nodes on the same network.

One team, at a time, will be the auctioneer and the other will be the bidders. After each auction, everyone terminates the session. Then we restart with another team being the auctioneer.

**Scoring**

A client get one point for successfully submitting any bid.
An auctioneer get one point for the receipt of any bid from a client and delivering an acknowledgement.
Auctioneer get one point for having a winning bid. And another point for each bidder who receives the result of the auction.
The protocol designer get 10 points for all 6 teams having greater than zero point.
