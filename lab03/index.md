# Network Security & Protocols #

In this lab you will use a packet sniffing tool to monitor network traffic and intercept unencrypted secrets in insecure protocols. You will be working in groups of two.

The basic tool for observing the messages exchanged between executing protocol entities is called a packet sniffer. As the name suggests, a packet sniffer captures (“sniffs”) messages being exchanged on the network connected to your computer. It will also typically store and/or display the contents of the various protocol fields in these captured messages. A packet sniffer itself is passive. It observes messages being sent and received by applications and protocols, but never sends packets it- self. Similarly, received packets are never explicitly addressed to the packet sniffer.

## Learning Objectives ##

- Describe the concept of a packet sniffer.
- What risks packet sniffers pose and how they can be mitigated.
- Describe the concept of a man-in-the-middle (MITM) attack.
- How can MITM attacks can be mitigated?

## Notes ##

- We will be using a tool called WireShark in order to perform our packet sniffing.
- The lab machines this week are on a virtual LAN and they will not have external web access.
	- Make sure to bring a USB stick and a laptop in order to access CourseSpaces and to transfer your work to/from your workstation.
- **You are not allowed to use the packet sniffer outside the context of this lab exercise.**

# Part 1: Detecting Clear Text Passwords #

Start up WireShark. You can find it under the Applications menu in the top right. The startup screen should look something like this:

![WireShark Splash](/lab03/splash.png)

Familiarize yourself with the user interface. You can start sniffing (capturing) network traffic by selecting a network interface on the left side (under interface list) - or you may select specific capturing options first. The resulting interface will look like the one below:

![WireShark Interface](/lab03/interface.png)

# Questions #

Answer the following questions and submit them in `report.txt`.

1. TBD

# Submission #

You will be submitting one file:

- `report.txt` Your answers
