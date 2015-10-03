# Network Security & Protocols #

In this lab you will use a packet sniffing tool to monitor network traffic and intercept unencrypted secrets in insecure protocols. You will be working in groups of two.

The basic tool for observing the messages exchanged between executing protocol entities is called a packet sniffer. As the name suggests, a packet sniffer captures (“sniffs”) messages being exchanged on the network connected to your computer. It will also typically store and/or display the contents of the various protocol fields in these captured messages. A packet sniffer itself is passive. It observes messages being sent and received by applications and protocols, but never sends packets it- self. Similarly, received packets are never explicitly addressed to the packet sniffer.

## Learning Objectives ##

- Describe the concept of a packet sniffer.
- What risks packet sniffers pose and how they can be mitigated.
- Describe the concept of a man-in-the-middle (MITM) attack.
- How can MITM attacks can be mitigated?

## Notes ##

- The lab machines this week are on a virtual LAN and they **will not** have external web access.
	- Make sure to bring a USB stick and a laptop in order to access CourseSpaces and to transfer your work to/from your workstation.
	- You will not be able to login to the workstations with your normal UVic credentials. Instead, you will login with the following:
	- `TBD`
- You will need the file `mitm-proxy-1.0.tar.gz`. You can download it from CourseSpaces or from [https://crypto.stanford.edu/ssl-mitm/](https://crypto.stanford.edu/ssl-mitm/)
- We will be using a tool called Wireshark in order to perform our packet sniffing.
	- **You are not allowed to use the packet sniffer outside the context of this lab exercise.**
- You should take note of the IP addresses of the workstations. You can do that by using the command `ifconfig`. Look for the one under eth0.

# Part 1: Detecting Clear Text Passwords #

**Start up Wireshark**. You can find it under the Applications menu in the top left. The startup screen should look something like this:

![WireShark Splash](/lab03/splash.png)

**Familiarize yourself with the user interface**. You can start sniffing (capturing) network traffic by selecting a network interface on the left side (under interface list) - or you may select specific capturing options first. The resulting interface will look like the one below:

![WireShark Interface](/lab03/interface.png)

The Wireshark interface has five major components:

- The **command menus** are standard pulldown menus located at the top of the window. Of interest to us now are the File and Capture menus. The File menu allows you to save captured packet data or open a file containing previously captured packet data, and exit the Wireshark application. The Capture menu allows you to begin packet capture.

- The **packet-listing window** displays a one-line summary for each packet captured, including the packet number (assigned by Wireshark; this is not a packet number contained in any protocol’s header), the time at which the packet was captured, the packet’s source and destination addresses, the protocol type, and protocol-specific information contained in the packet. The packet listing can be sorted according to any of these categories by clicking on a column name. The protocol type field lists the highest level protocol that sent or received this packet, i.e., the protocol that is the source or ultimate sink for this packet.

- The **packet-header details window** provides details about the packet selected (highlighted) in the packet listing window. (To select a packet in the packet listing window, place the cursor over the packet’s one-line summary in the packet listing window and click with the left mouse button). These details include information about the Ethernet frame and IP datagram that contains this packet. The amount of Ethernet and IP-layer detail displayed can be expanded or minimized by clicking on the plus-or-minus boxes to the left of the Ethernet frame or IP datagram line in the packet details window.  If the packet has been carried over TCP or UDP, TCP or UDP details will also be displayed, which can similarly be expanded or minimized. Finally, details about the highest level protocol that sent or received this packet are also provided.

- The **packet-contents window** displays the entire contents of the captured frame, in both ASCII and hexadecimal format.

- The **packet display filter field** is found towards the top of Wireshark's graphical user interface. A protocol name or other information can be entered here in order to filter the information displayed in the packet-listing window (and hence the packet-header and packet-contents windows). In the example below, we’ll use the packet-display filter field to have Wireshark hide (not display) packets except those that correspond to HTTP messages.

**Analyze the network traffic of an insecure protocol**. You need two lab workstations in order to work on this experiment, so please pair up with a partner. One of you will use FTP to access a server from one machine, while the other partner will use Wireshark to analyse the network traffic.

The file transfer protocol (FTP) is used to exchange files over the internet. An FTP server was set up here:

`TBD`

Start Wireshark on one computer and the FTP client on the other computer.

Begin capturing network traﬃc with Wireshark while your partner is connecting to the FTP server using the following credentials:

- username: `TBD`
- password: `TBD`

Use command line to login - something like this: `ftp username@TBD`. Stop capturing the network traffic after you login.

Investigate the traﬃc you have captured. Remember that you can filter the traffc in the filter window (for example by IP address `ip.addr == XXXX` or by the protocol type). Can you find the password in the traffic?

Copy the specific packet frame containing the intercepted password in ASCII format into your report.

# Part 2: Analyzing a Secure Protocol #

SFTP is a secure protocol using SSH for encrypting the FTP traffic. An SFTP server has been set up here:

`TBD`

Again, have Wireshark on one computer and the (S)FTP client on the other computer.

Start capturing network traffic with Wireshark while your partner is connecting to the SFTP server using the credentials:

- username: `TBD`
- password: `TBD`

Use command line to login - something like this: `sftp username@TBD`. Stop capturing the network traffic after you login.

Investigate the traffic you have captured. Can you find the password in the traffic? What happened? How was the secure channel established?

# Part 3: Detecting MITM Attacks #

Now on both machines, start capturing network traffic. Open up Firefox on the non-Wireshark machine and visit [https://www.wikipedia.org/](https://www.wikipedia.org/). Once the page has loaded, stop capturing network traffic.

Since you are using a secure connection, take a look at how it is secured. Inspect the certificate. Who is verifying Wikipedia? 

---

For the next step, you will need the file `mitm-proxy-1.0.tar.gz`. You can download it from CourseSpaces or from [https://crypto.stanford.edu/ssl-mitm/](https://crypto.stanford.edu/ssl-mitm/).

Download and extract the file:

`tar -zxvf mitm-proxy-1.0.tar.gz`

Run the proxy with the supplied script:

`cd mitm-proxy-1.0`

`./run.sh`

Open up Firefox and set the browser to use the proxy.

- Open Options > Advanced > Network and then click the Settings button under the Connection section.
- Select "Manual proxy configuration"
- In the "SSL Proxy:" field, enter `localhost` and "Port:" `8888`
- Click OK to apply.
- **NOTE: Remember to undo this proxy setting when you are done with the lab!**

Start capturing network traffic. Open up Firefox on the non-Wireshark machine and re-visit [https://www.wikipedia.org/](https://www.wikipedia.org/) again. Once the page has loaded, stop capturing network traffic.

- We recommend that you do not login to the site.

You should see a warning now talking about the site's certificate being untrusted. Inspect the certificate. What's going on here? Can you detect the MITM attack on Wireshark? 

# Questions #

Answer the following questions and submit them in `report.txt`.

1. Copy the specific packet frame containing the intercepted password in ASCII format here.
2. Were you able to intercept the password? What happened in the SFTP traffic? How was the secured communications established?
3. Who usually verifies Wikipedia for their secure connections?
4. Suppose you ignored the untrusted certificate warning in Part 3 and logged in to the site. What are the potential consequences of this?
5. Characterize the MITM attack in Part 3. How can MITM attacks be mitigated?
6. How do modern browsers "know" to trust a certificate from the server?
	- Hint: Lookup [Certificate Authorities](https://en.wikipedia.org/wiki/Certificate_authority) on Wikipedia and give a brief explanation. Does this remind you of a  certain concept from Lab 02?

# Submission #

You will be submitting one file:

- `report.txt` Your answers
