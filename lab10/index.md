# Privacy #

How can we protect ourselves from others? Whether they are government agencies, thieves, friends or coworkers, we need to prepare ourselves. This week lab will consist of a survey of applications that we can use to protect our online assets.

## Preliminaries ##

Before we start, make sure you understand the following three concepts. You can find the necessary information by searching the Internet:

- Forward Privacy
- Repudiation
- Non-Repudiation

# Part 1: Tor #

Tor is a Web browser that anonymises where you are located. 

1. Download it into your home directory: [https://www.torproject.org/download/download-easy.html.en](https://www.torproject.org/download/download-easy.html.en) Use the 64-bit version. It is statically compiled, so you can simply download and uncompress it with the tar command (it uses xz compression)
2. Run it. As you can see, it is relatively spartan compared to Chrome and Firefox.
3. Check your IP address both in Tor and in Chrome or Firefox. There are various web site where you can do this. For example: [http://www.whatismyip.com/](http://www.whatismyip.com/)

**Question 1:** Where is your browser's IP "located"?

## Fingerprinting ##

Well, it wasn't that easy, wasn't it? WhatismyIp tried to fingerprint your browser and Tor stopped it (and asked you what to do.) Read the first page of this paper: [http://www.w2spconf.com/2012/papers/w2sp12-final4.pdf](http://www.w2spconf.com/2012/papers/w2sp12-final4.pdf)

**Question 2:** Describe what is *HMTL 5 Canvas Image rendering fingerprinting*.

## Other Vulnerabilities ##

If you do some browsing, going to shopping sites and news sites, any of those sites that are likely to want to know who you are. As you can see, Tor does not provide the best browsing experience. This is because it does not integrate any plugins (e.g. flash).

Check your IP address again.

## HTTPs, Tor and Privacy ##

Read: [https://www.eff.org/pages/tor-and-https](https://www.eff.org/pages/tor-and-https)

In this diagram, we see a user *USER* with password *PW* connecting to a server *SITE.COM* from location *LOCATION* exchanging *DATA*. We have hackers, police, NSA, sysadmins and lawyers - all of which want to get a hold of your information by being passive men-in-the-middle.

**Question 3:** Without Tor and without HTTPs, what can every different attacker see?

**Question 4:** When HTTPs is always used, what information can be seen by each attacker?

**Question 5:** When both Tor and HTTPs are in use, what information can be seen by each attacker?

## Threats to Anonymity ##

Read the section "Want Tor to really work?" [https://www.torproject.org/download/download-easy.html.en#warning](https://www.torproject.org/download/download-easy.html.en#warning)

**Question 6:** Why are downloaded documents (specially PDFs and Word) potential threats to your anonymity? What information do they disclose?

# Part 2: Truecrypt #

Unfortunately we won't be able to use TrueCrypt because we require administrative privileges to use it. Instead, we will read a little bit about it. Truecrypt is used to encrypt partitions and to create mountable partitions that are encrypted. Is it safe? Read this section (Legal Cases) of its Wikipedia Entry:
[https://en.wikipedia.org/wiki/TrueCrypt#Legal_cases](https://en.wikipedia.org/wiki/TrueCrypt#Legal_cases)

**Question 7:** How do these legal cases provide evidence that TrueCrypt actually works?

But suddenly it disappeared. Fortunately there were archives of the software and people are still using it (last usable version is 7.1) The Electronic Frontier Foundation recommends [https://ssd.eff.org/en/module/how-encrypt-your-windows-device](https://ssd.eff.org/en/module/how-encrypt-your-windows-device) It is not as good, and it is meant for Windows. 

**Question 8:** Why did TrueCrypt disappear?

* Off-The-Record communication

Some chat services support "off-the-record" communication. However, how do we know that they actually work? For instance, when we indicate in google-chat that
we want an off-the-record communication, are they really not logging it?

A few years back, a group of security PhD students (one of them now a prof at Univ. of Waterloo) developed a protocol and library to create off-the-record
communication on top of any chat service. The idea is that if you can transter text between clients, you can transfer encrypted information to support
off-the-record communication. Go to https://otr.cypherpunks.ca/

Q9. What are the four main features supported by OTR? (Off-the-record communication)

Q10. What is the relationship between deniability and repudiation?

There are many clients that support OTR (none official, unfortunately.) If you have your laptop with you, the easiest would be for you to download one of them. See https://otr.cypherpunks.ca/software.php (I use Adium in OS X.)

I have compiled a version of pidgin with the OTR pluggin. Copy the file =/project/seng360/dmg/pidgin/local.tar.gz= and uncompress it at the top level of your home directory. It will create a directory called =local= with many files inside it.

To run it execute:

#+BEGIN_SRC bash
export LD_LIBRARY_PATH=${HOME}/local/lib:
~/local/bin/pidgin
#+END_SRC

Add an account to it (it supports almost any protocol.) If you don't have one (or prefer not to use one that you already have), create one at jabber.az. You can
use the "Add Account" window. Use the protocol XMPP, domain =jabber.az=, and select the option "Create this account on the server" (it will be available after
you select XMPP as the protocol.)

At this point, you need to find somebody else in the lab who is using the same protocol as you (so you can both communicate), then follow this tutorial.

https://securityinabox.org/pidgin_securechat

Q11. Without certificates, how does OTR authenticate the person in the other end?


* Password Safe

I am a strong believer that the best way to have secure passwords is to write them down. The challenge is to write them down in a secure location in such a
way that they are easy to retrieve and use. PasswordSafe is probably the best tool for the job (available for Windows, Mac and
Linux.) http://passwordsafe.sourceforge.net/. Watch the second video in this page: http://passwordsafe.sourceforge.net/quickstart.shtml

Q12. Can PasswordSafe be a counter-measure against physical keyloggers (e.g. a keyboard)? Explain.

Q13. What do you consider the main disadvantages of PasswordSafe? (Aside from having your master password stolen and all your usernames/passwords lost at once.)

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the questions