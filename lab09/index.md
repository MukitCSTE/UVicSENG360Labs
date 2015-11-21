# TOCTTOU Attacks and Race Conditions #

This week we will look into race-conditions as well as Time of check to time of use (TOCTTOU) vulnerabilities. A race condition occurs when multiple processes access and manipulate the same data concurrently, and the outcome of the execution depends on the particular order in which the access takes place. If a privileged program has a race-condition vulnerability, attackers can run a parallel process to "race" against the privileged program, with an intention to change the behavior of the program.

You will be given a program with a known race-condition vulnerability. Your task is to develop a scheme to exploit the vulnerability and gain root privilege. As well, you will also look through several protection schemes that can be used in order to counter race-condition attacks.

## Learning Objectives ##

- Get practical experience with TOCTTOU attacks
- Explain the probabilistic nature of such attacks
- Define possible countermeasures

# Part 1: Lab Setup #

Since you will need root access for the lab, we will be using a virtual machine again. As before, you can grab a fresh copy of the virtual machine from `/seng/seng360/vm` if you lost your virtual machine from the previous labs.

- Just like before, copy that vm to your local machine's `/tmp` directory and assign it under your own username. Then point VirtualBox to that VM and start it up. You may need to remove your old VM entry if it's inaccessible or behaving strangely.

Once you have your virtual machine running, ssh into it with:

	ssh -p 3030 -l user360 localhost

To become root in the virtual machine you will need to use the command `su` (use the root password provided).

| what | user    | password   |
|------|---------|------------|
| user | user360 | user360    |
| root | root    | root360lab |

Also, since the base VM does not have gcc installed, you'll need to do it yourself:

	sudo apt-get update && sudo apt-get install build-essential -y

# Part 2: Exploiting Race Condition Vulnerabilities #

The following is a seemingly harmless C program. However, it has a nasty race-condition vulnerability.

``` c
// vulp.c
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#define DELAY 10000

int main() {
  char *fn = "/tmp/XYZ";
  char buffer[60];
  FILE *fp;
  long int i;

  // get user input
  scanf("%50s", buffer);

  if(!access(fn, W_OK)) {
    // simulating delay
	for (i=0; i < DELAY; i++) { int a = i^2; }

    fp = fopen(fn, "a+");
    fwrite("\n", sizeof(char), 1, fp);
    fwrite(buffer, sizeof(char), strlen(buffer), fp);
    fclose(fp);
  } else {
    printf("No permission \n");
  }
}
```

Create this file, name it `vulp.c` and save it in user360's home directory **as user360, not root**. Compile this program as user360:

	gcc -o vulp vulp.c

- Note: When you run vulp, make sure /tmp/XYZ already exists first, otherwise you'll get no permission as a result. You can create the file by doing `touch /tmp/XYZ`.

This is part of a Set-UID program (owned by root). It appends a string of user input to the end of a temporary file /tmp/XYZ. Since the code runs with root privilege, it carefully checks whether the real user actually has access permission to the file /temp/XYZ via the access() call. Once verified, the program opens the file and writes the user input into the file.

The race condition vulnerability is due to the simulated time delay window between the check (access) and use (fopen). There is a possibility that the file used by access is different from the file used by fopen, even though they have the same filename /tmp/XYZ.

If a malicious attacker can somehow make /tmp/XYZ a symbolic link pointing to /etc/shadow within that time delay, the attacker can redirect the user input to be appended to the /etc/shadow file instead of /tmp/XYZ.

## Malicious User Addition ##

As we learned in previous labs, /etc/passwd is the file authentication database for a Unix machine containing basic user attributes. The /etc/shadow file stores the password data for the users and unlike passwd which is world readable, shadow is only readable by root.

We can target these two files in our attacks in order to gain root access. If an attacker can insert information into these two files, they essentially have the power to create new users with root access (by letting uid be 0).

The normal way of making a user is with the `useradd` command. As user user360, go ahead and create a new user called `smith` with a password `smith`. (If you want more information on general unix user administration, see here: [http://www.tutorialspoint.com/unix/unix-user-administration.htm](http://www.tutorialspoint.com/unix/unix-user-administration.htm))

	sudo useradd -m smith
	sudo passwd smith

If you take a look at /etc/passwd and /etc/shadow, you'll see new entries for the smith user. They should look something like this:

	/etc/passwd
	-----------
	smith:x:1001:1001::/home/smith:
	
	/etc/shadow
	-----------
	smith:$6$blahblahsomejibberishhere/:16759:0:99999:7:::

The third column of the smith entry has a UID of 1001 which is nothing special. If we change that entry to 0, smith can become root.

## Exploit the Race Condition ##

You are to exploit this race condition vulnerability in the above Set-UID program. Specifically:

- Overwrite any file that belongs to root (/etc/shadow)
- Gain root privileges; namely you should be able to do anything that root can do

Your goal is to create a C program that can create symbolic links from /tmp/XYZ to the /etc/passwd and /etc/shadow files. You can create a symbolic link on command line via the `ln -s` command. In C, you may call the `symlink` function to create a symlink. Since Linux doesn't allow you to create a link if it already exists, you'll need to delete old symlinks first. You can do that via the `unlink` function. Below is a code snippet showing how to remove a symlink and then make /tmp/XYZ point to /etc/passwd:

``` c
unlink("/tmp/XYZ");
symlink("/etc/passwd", "/tmp/XYZ");
```

Since user360 doesn't have read permission for /etc/shadow, the only way we know if it was modified is by comparing timestamps. The following shell script checks if the /etc/shadow timestamps have changed, and will print a message once the change is noticed.

``` bash
#!/bin/sh
old='ls -l /etc/shadow'
new='ls -l /etc/shadow'
while [ "$old" = "$new" ]
do
	new='ls -l /etc/shadow'
done
echo "STOP! The shadow file has been changed"
```

Create this script, name it `check.sh` and save it in user360's home directory **as user360, not root**. Make sure the script has execution permission by doing `chmod +x check.sh`. You should have this script run in a separate terminal session (so create another terminal and ssh into the VM again)

### Improving Success Rate ###

As with any race-condition attack, the critical step (pointing the link to our target file) of the attack must occur within the window between check and use - namely between access and fopen. Since we can't modify the vulnerable program, the only thing we can do is to run our attacking program in parallel with the target program and hope that the link creation occurs in that window.

We cannot achieve perfect timing with this - thus the success of this attack is probabilistic. The smaller the window of opportunity, the less likely you will get a successful attack. You will need to consider ways to increase the probability of succeeding in an attack. (Hint: you an run the vulnerable program many times, you only need to be successful in one of the attempts to get through).

Since you need to run the attack and vulnerable program many times, consider writing a script to automate the process. You can leverage file redirection or piping to achieve this. For example:

	echo 'yourinputhere' | ./vulp

or

	./vulp < FILE

Where file consists of just your input. The time command `time <program>` could be useful in your script because it times how long program takes to execute.

**Question 1:** Describe how you achieved your solution to Part 2.

The vulp program deliberately has a DELAY parameter in order to make your attack easier. Once you have succeeded in your attacks, gradually reduce the value of DELAY.

**Question 2:** As the DELAY approaches zero, how much longer does it take for you to succeed?

# Part 3: Protection Mechanism A - Repeating #

Addressing race condition bugs is not an easy task because the *check-and-us*e pattern is often necessary in programs. Instead, we can introduce more race conditions, such that in order to compromise the security of the program, attackers need to win all these additional race conditions. Designed properly, we can exponentially reduce the winning probability for attackers.

The basic idea is to repeat access() and open() several time. At each time, we open the file, and at the end, we check if the same file opened is the same file by checking their i-nodes. They should be the same - otherwise notify the user of file tampering.

Use this strategy to modify vuln.c and evaluate the race condition. In order to check i-nodes, consider using the `stat` C function in the `sys/stat.h` library header.

**Question 3:** With your repeating modifications in place, how difficult is it to succeed, if at all? Please include your modified vulp.c source code for this step inline with this question.

# Part 4: Protection Mechanism B - Principle of Least Privilege #

The fundamental problem of the vulnerable program in this lab is the violation of the *Principle of Least Privilege*. The programmer understands that the user who runs the program may be too powerful, so they introduced access() as a limiting factor. However, this isn't the proper approach. A better way is to make it so that if users do not need certain privileges, those privileges are disabled.

Apply the Principle of Least Privilege to the original vulnerable program vulp.c. You should consider using the `seteuid` system call in order to temporarily disable root privilege, and flip it back on only when necessary. Then reevaluate the race condition.

**Question 4:** With your principle of least privilege modifications in place, how difficult is it to succeed, if at all? Please include your modified vulp.c source code for this step inline with this question.

# Troubleshooting #

- While testing the program, sometimes /tmp/XYZ may get into an unusable state because of untimely killing of the attack program. When this happens, the OS automatically creates a normal file with root as owner. If this happens, delete this file before restarting the attack.
- If you accidentally modify and recompile vulp as root, you'll need to run `chmod 4755 vulp` in order to make it accessible to user360 again.

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 4 questions with the requested source code copy-pasted in as part of your answer
