# Network Security & Protocols #

In this lab you will use a packet sniffing tool to monitor network traffic and intercept unencrypted secrets in insecure protocols. You may work in groups of two.

The basic tool for observing the messages exchanged between executing protocol entities is called a packet sniffer. As the name suggests, a packet sniffer captures (“sniffs”) messages being exchanged on the network connected to your computer. It will also typically store and/or display the contents of the various protocol fields in these captured messages. A packet sniffer itself is passive. It observes messages being sent and received by applications and protocols, but never sends packets itself. Similarly, received packets are never explicitly addressed to the packet sniffer.

## Learning Objectives ##

- Describe the concept of a packet sniffer.
- What risks packet sniffers pose and how they can be mitigated.
- Describe the concept of a man-in-the-middle (MITM) attack.
- Understand HSTS and how MITM attacks can be mitigated?

## Notes ##

- The lab machines this week are on a virtual LAN and they **will not** have external web access (with a few exceptions).
	- Make sure to bring a USB stick and a laptop in order to access CourseSpaces and to transfer your work to/from your workstation.
	- You will login to the workstations with your normal UVic credentials. However, your standard engineering home directories will not be mounted. Your home directory this week will be temporary local directories.
- We will be using a tool called Wireshark in order to perform our packet sniffing.
	- **You are not allowed to use the packet sniffer outside the context of this lab exercise.**
-  Due to department network and security constraints, unfortunately you will only be able to sniff your own computer's generated traffic.
- You should take note of the IP addresses of the workstations. You can do that by using the command `ifconfig`. Look for the one under "p4p1" which will be the interface you will sniff.

# Part 1: Detecting Clear Text Passwords #

**Start up Wireshark**. Wireshark requires root privileges in order to properly sniff. You can start it up by running `wireshark` from command line, or graphically from Applications > Internet > Wireshark. The startup screen should look something like this:

![WireShark Splash](/lab03/splash.png)

**Familiarize yourself with the user interface**. You can start sniffing (capturing) network traffic by selecting a network interface on the left side (under interface list) - or you may select specific capturing options first. The resulting interface will look like the one below:

![WireShark Interface](/lab03/interface.png)

The Wireshark interface has five major components:

- The **command menus** are standard pulldown menus located at the top of the window. Of interest to us now are the File and Capture menus. The File menu allows you to save captured packet data or open a file containing previously captured packet data, and exit the Wireshark application. The Capture menu allows you to begin packet capture.

- The **packet-listing window** displays a one-line summary for each packet captured, including the packet number (assigned by Wireshark; this is not a packet number contained in any protocol’s header), the time at which the packet was captured, the packet’s source and destination addresses, the protocol type, and protocol-specific information contained in the packet. The packet listing can be sorted according to any of these categories by clicking on a column name. The protocol type field lists the highest level protocol that sent or received this packet, i.e., the protocol that is the source or ultimate sink for this packet.

- The **packet-header details window** provides details about the packet selected (highlighted) in the packet listing window. (To select a packet in the packet listing window, place the cursor over the packet’s one-line summary in the packet listing window and click with the left mouse button). These details include information about the Ethernet frame and IP datagram that contains this packet. The amount of Ethernet and IP-layer detail displayed can be expanded or minimized by clicking on the plus-or-minus boxes to the left of the Ethernet frame or IP datagram line in the packet details window.  If the packet has been carried over TCP or UDP, TCP or UDP details will also be displayed, which can similarly be expanded or minimized. Finally, details about the highest level protocol that sent or received this packet are also provided.

- The **packet-contents window** displays the entire contents of the captured frame, in both ASCII and hexadecimal format.

- The **packet display filter field** is found towards the top of Wireshark's graphical user interface. A protocol name or other information can be entered here in order to filter the information displayed in the packet-listing window (and hence the packet-header and packet-contents windows). In the example below, we’ll use the packet-display filter field to have Wireshark hide (not display) packets except those that correspond to HTTP messages.

**Analyze the network traffic of an insecure protocol**. You will use FTP to access a server and have Wireshark running at the same time on the same machine to analyze the network traffic.

The file transfer protocol (FTP) is used to exchange files over the internet. An FTP server was set up here:

`seng360ftp`

Start Wireshark on one console terminal and the FTP client on another console terminal.

Begin capturing network traffic with Wireshark while you are attempting to connect to the FTP server. The login credentials to the FTP server are as follows:

| Attribute | Value          |
|-----------|----------------|
| Username  | seng360student |
| Password  | seng360        |

Use command line to login; something like this: `ftp seng360ftp`. Then enter the provided credentials. Stop capturing the network traffic after you login. Exit the ftp client by typing in "bye".

- *Note: Do not use your UVic login credentials on this ftp server!*

Investigate the traﬃc you have captured. Remember that you can filter the traffic in the filter window (for example by IP address `ip.addr == XXXX` or by the protocol type like `ftp`). Can you find the password in the traffic?

**Question 1:** Copy the specific packet frame containing the intercepted password in ASCII format here. To do this, select the packet with the password, right click, and select print. In the window, make it output to a file. Make sure the resulting output contains the packet header information as well as the password field.

# Part 2: Analyzing a Secure Protocol #

SFTP is a secure protocol using SSH for encrypting the FTP traffic. An SFTP server has been set up here:

`seng360sftp`

- If that does not work, you may try to sftp to the same server in Part 1.

Again, start Wireshark on one console terminal and the (S)FTP client on another console terminal.

Start capturing network traffic with Wireshark while you are connecting to the SFTP server. The login credentials to the SFTP server should be the same as the FTP server and are as follows:

| Attribute | Value          |
|-----------|----------------|
| Username  | seng360student |
| Password  | seng360        |

Use command line to login - something like this: `sftp seng360sftp`. Then enter the provided credentials. Stop capturing the network traffic after you login. Exit the ftp client by typing in "bye". Remember that you can filter the traffic in the filter window (for example by IP address `ip.addr == XXXX` or by the protocol type like `sftp`).

**Question 2:** Investigate the traffic you have captured. Were you able to intercept the password?

**Question 3:** What happened in the SFTP traffic? Describe how the secured communications channel was established.

# Part 3: Detecting MITM Attacks #

We are now going to create a Man In The Middle attack. Start up Wireshark on one of your console terminals. Then open up Firefox on the same machine and visit [https://mitmproxy.org/](https://mitmproxy.org/). Once the page has loaded, stop capturing network traffic.

**Question 4:** Since you are using a secure HTTPS connection, take a look at how it is secured. In Firefox, inspect the certificate. Who is verifying mitmproxy's website?

Now you will be using a Python tool called mitmproxy. We have pre-installed this tool onto the lab machines already.

To start mitmproxy, **open up a new terminal window** and then execute `mitmproxy`. This will start up an interactive command-line based program in the console. It should now be listening for any traffic at port 8080.

- *Note: If you have time and wish to explore what mitmproxy can do, you can visit their documentation at [http://docs.mitmproxy.org/en/stable/index.html](http://docs.mitmproxy.org/en/stable/index.html)*

Open up Firefox and set the browser to use the proxy.

- Open Preferences > Advanced > Network and then click the Settings button under the Connection section.
- Select "Manual proxy configuration"
- In the "SSL Proxy:" field, enter `localhost` and "Port:" `8080`
- There may be a field towards the bottom with "localhost, 127.0.0.1". Blank that field out for now.
- Click OK to apply.
- **NOTE: Remember to undo this proxy setting when you are done with the lab!**

Start capturing network traffic. Open up Firefox on the same machine and re-visit [https://mitmproxy.org/](https://mitmproxy.org/) again. Once the page has loaded, stop capturing network traffic.

You should see a warning now talking about the site's certificate being untrusted. Inspect the certificate. What's going on here? Can you detect the MITM attack on Wireshark? Can you still access the website?

**Question 5:** Suppose you ignored the untrusted certificate warning and logged in to the site. What are the potential consequences of this?

**Question 6:** Characterize/explain the MITM attack you performed. What things would you be looking for to detect a potential MITM attack on Wireshark?

# Part 4: Mitigating HTTPS MITM with HSTS #

One way we can mitigate the type of MITM we just performed in the last section is with the use of HTTP Strict Transport Security (HSTS). You can find out more about it at [https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security)

Not all websites employ HSTS. However, we can check if a website uses HSTS by using the following command:

    curl -s -vv https://website.com 2>&1 | grep Strict

**Question 7:** Try the above command by substituting https://website.com with [https://www.wikipedia.org/](https://www.wikipedia.org/) and then on [https://mitmproxy.org/](https://mitmproxy.org/). What were the results? Can you tell if either of them are using HSTS?

With Firefox still configured to talk to the mitmproxy, try visiting [https://www.wikipedia.org/](https://www.wikipedia.org/). You should see a warning like before.

**Question 8:** Are you able to access Wikipedia through the mitmproxy? Why are you getting this type of behavior?

At this point, kill the mitmproxy program by pressing q. You should return back to command line. Then return back into Firefox's configuration and restore the proxy settings back to the way you found them.

**Question 9:** Explain in your own words what HSTS is and what it does. How does this help to mitigate HTTPS MITM attacks?

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 9 questions.
