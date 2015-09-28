# Generating Random Numbers #

Generating random numbers in a computer is hard. The theory was laid down long ago in Knuth's Art's of Computer Programming. In security, random numbers are an important building block. For example, they can be used for creating:

- [Salts](https://en.wikipedia.org/wiki/Salt_%28cryptography%29)
- [Nonces](https://en.wikipedia.org/wiki/Cryptographic_nonce)
- [One-time pads](https://en.wikipedia.org/wiki/One-time_pad)
- [Keys](https://en.wikipedia.org/wiki/Key_%28cryptography%29)

It is often the case that security is broken not because the algorithms are weak, but because the random number generation is not properly implemented. For example, one of the first successful attacks of a web browser (Netscape) [exploited poorly written random number generators](http://www.cs.berkeley.edu/~daw/papers/ddj-netscape.html) (used to generate cryptographic keys that were to be used during a SSL session).

What you really need to understand is that:

- Generating random numbers is hard, and
- Learning how to generate random numbers is important.

# Part 1. Generating random numbers #

For applications that require true randomness, you should always use [hardware random number generators](http://en.wikipedia.org/wiki/Hardware_random_number_generator). These are created from available entropy. You can even buy PCI cards that serve this purpose. New Intel chips have implemented hardware random generators, although some believe this could be backdoor to secure applications (I guess at the end you have to trust somebody).

Otherwise you can choose to use a software random number generator, which are called *Pseudo-random number generators* (PRNG).  One particular type of generator that we need to know is *Cryptographically Secure Pseudo-Random Number Generators* (CSPRNG).

Most programming languages provide PRNG, and some provide CSPRNG. But why trust a middle-person when you can go directly to the source for random numbers? Most operating systems provide PRNGs. In this lab we'll use the Linux PRNGs.

In Linux, random numbers are can be created by the kernel and are made available via the `/dev/random` and `/dev/urandom` pseudo-files. To learn about them read their main page:

`man -s 4 random`

Both pseudo-files (`/dev/random` and `/dev/urandom`) behave like any other unix file: all you have to do is read as many bytes as you need. If you need a 32-bit integer, you read 4 bytes.

For this part you, will implement two programs, both of them identical except that one reads `/dev/random` and one `/dev/urandom`. Call the first program `random.c` and the second `urandom.c`.

Each program should read from their corresponding random-generator file a byte (8 bits) and output it one per line as a value between 0 and 255. These numbers should be output to standard output, like this:

	34
	12
	128
	219
	3
	...

Once Ctrl-C (`SIGING`) or a kill signal (`SIGKILL`) is sent to the program, your program should gracefully terminate and output the number of numbers generated to standard error. For example:

	Received SIGINT
	Generated 53563 values.

Use `skeleton.c` and the `Makefile` provided as the basis for your programs. 

# Part 2. Benchmark them #

Using the command `timeout` (do `man timeout`) you can run any program for a certain period. Run `random` for 5 minutes and `urandom` for 60 seconds.

	timeout -s SIGINT 300 ./random > random.out 
	timeout -s SIGINT 60 ./urandom > urandom.out

- How many numbers per second were you able to generate with each method?

# Part 3. Count the distribution of numbers #

Write a small program (use any language) that reads the generated files and outputs, in order, for each potential random value, the number of values generated in CSV format. For example:

	0,194278
	1,193755
	2,194559
	3,194288
	4,194172
	...
	216,193738
	217,194310
	218,194049
	...
	253,193738
	254,194041
	255,194093

The first value is the number you are counting, and the second number is the number of times the number was found. Save the output of as `urandom.report` and `random.report`. Compute the minimum, maximum, median and the average of the values that you generated for each set and append it to the bottom of each report.

## Plot them ##

How do we know if the numbers are truly random? Well, that is a good question. We would require statistics to properly do it. Instead, we will simply visualize the results. For this we are going to use `R`. We will only plot the first 1000 values.  Create two files called `random.R` and `urandom.R` by reusing the following script. Replace `data` with `random` and `urandom` to process the corresponding files.

Each script creates two png files, the first with the points plotted in the order they were generated, and the second with them in order.

	data<-read.table('data.out',col.names=c('values'))
	summary(data)
	
	subset<-head(data$values,1000)
	summary(subset)
	
	png("dataRandom.png", width=600, height=600)
	plot(subset)
	dev.off()
	
	png("dataSorted.png", width=600, height=600)
	plot(sort(subset))
	dev.off()

You can run an R script using:

	Rscript <filename>

# Questions #

- Why are PRNGs called "Pseudo"?
- What are the properties that CSPRNG should have?
- Explain why reading from `/dev/urandom` is significantly faster than `/dev/random/`.

# Submission #

Submit, via CourseSpaces, in a single zip file:

- The files `urandom.report` and `random.report`
- The 4 pngs created

In paper:

- The answers to the questions of Part 2, and Part 4.
