# Reliable data transfer using UDP to download files 

<---
## Problem Statement
There should be a client program and a server program. The server program hosts files and responds to requests for files. It breaks the requested file into segments and sends them to the client over UDP. The client program takes a file name as input and requests the file from the server. The programs should handle UDP packet losses to make sure that the entire file is correctly received by the client program. Your code needs to include implementation of the **Alternating Bit** and **Selective Repeat protocols**. Refer chapter 3.4 (Principles of Reliable Data Transfer) - Computer Networking, Kurose to understand these two protocols.

Client program should print detailed information about any requests sent and data received at byte level (e.g., time X received byte Y to Z) during the file download.  Server program should print detailed information about any requests received and data sent at byte level.

During your development, you can run the client and server on the same machine. However, for comprehensive testing and evaluation, your client program and server program should be run on different machines in different networks.
-->
