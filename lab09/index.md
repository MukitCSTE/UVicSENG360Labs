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
/* vulp.c */
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

Create this file, name it `vulp.c` and save it in user360's home directory **as user360, not root**.

This is part of a Set-UID program (owned by root). It appends a string of user input to the end of a temporary file /tmp/XYZ. Since the code runs with root privilege, it carefully checks whether the real user actually has access permission to the file /temp/XYZ via the access() call. Once verified, the program opens the file and writes the user input into the file.

The race condition vulnerability is due to the simulated time delay window between the check (access) and use (fopen). There is a possibility that the file used by access is different from the file used by fopen, even though they have the same filename /tmp/XYZ.

If a malicious attacker can somehow make /tmp/XYZ a symbolic link pointing to /etc/shadow within that time delay, the attacker can redirect the user input to be appended to the /etc/shadow file instead of /tmp/XYZ.

## Task 1: Exploit the Race Condition ##

You are to exploit this race condition vulnerability in the above Set-UID program. Specifically:

- Overwrite any file that belongs to root
- Gain root privileges; namely you should be able to do anything that root can do

# Part 3: Protection Mechanism A - Repeating #

# Part 4: Protection Mechanism B - Principle of Least Privilege #

# Submission #

You will be submitting one file:

- `report.txt` Your answers
