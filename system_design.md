# system design 

- System is a loosely coupled architechture or collection of technologies that interacts with each other and serves certain set of users to fulfill certain set of requirements 
ex - image sharing systems - instagram
	 texting system - whatsapp 
	 streaming system - netflix, hotstar
	 
- Network Protocols
Protocol is a set of rules, so network protocol is set of rules that has been defined in order to communicate over the network.
These network protocol are present in 2 layers of osi model.
application layers -
client server protocol
Client initiates the request and server response with data.
HTTP - generally used. One way communication. Multiple client can communicate with a server but they can't communicate with each other
FTP - used to transfer file over the network, do not uses encryption while sharing data. Creates 2 connection,one is connection and the other one is data. Connection is always active
SMTP - used with IMAP , SMTP shares the data to user agent which sends to other user agent now IMAP receives that data. It is designed to access message over the network on multiple devices . It is fast
Earlier pop3 was used which allows the email to be downloaded on a single computer and was slow as downloading was involved.
Web Socket - used in real time messaging systems, wherein any message coming to the server, server immediately initiates a request to the client with the message. Two way communication as server is also initiating conversation. Whatsapp
Peer to peer protocol
All computer's are connected with each other , client and server and all can interact.
WebRTC - used in Google meet,live streaming services
Transport layer
TCP/ IP - divides data into packets, maintain an ordering  And after sharing data checks if any packet is missing.Slow as ordering is involved with checking on client end
UDP - fast as no ordering is maintained, data shared in datagrams . Any packets lost will not do any harm , live streaming services,if any part got missed than that will not do much harm.
