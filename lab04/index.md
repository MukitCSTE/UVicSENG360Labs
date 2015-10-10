# AES and Encryption Modes #

AES is a widely used cipher with no known vulnerabilities. But, like any block cipher, it needs to be used with a block encryption mode. As Wikipedia states:

> A block cipher by itself is only suitable for the secure cryptographic transformation (encryption or decryption) of one fixed-length group of bits called a block. A mode of operation describes how to repeatedly apply a cipher’s single-block operation to securely transform amounts of data larger than a block.

You will need `pic_original.bmp` from CourseSpaces.

## Learning Objectives ##

- Apply secret-key cryptography using openssl and different ciphers
- Describe differences between operating modes w.r.t. confidentiality
- Describe differences between operating modes w.r.t. integrity
- Describe the PKCS5 padding scheme and the operating modes that need padding

# Part 1: Encryption using different ciphers and modes #

In this task, we will experiment with various encryption algorithms and modes. You will be using the `openssl` tool for this purpose. Use the `openssl enc` command to encrypt/decrypt a file. To see the manuals, you can type `man openssl` and `man enc`. Below is an example command:

> openssl enc *ciphertype* -e -in plain.txt -out cipher.bin -K 00112233445566778899aabbccddeeff -iv 0102030405060708

Please replace the **ciphertype** with a specific AES cipher type, such as `-aes-128-cbc`, `-aes-128-cfb`, and `-aes-128-ofb`. In this task, you should try at least 3 different ciphers and three different modes. you can find the meaning of the command-line options and all the supported cipher types by typing `man enc`. Below are some common options for the openssl enc command:

| Option | Description |
| --- | --- |
| -in <file> | input file |
| -out <file> | output file |
| -e | encrypt |
| -d | decrypt |
| -K/-iv | key/iv in hex is the next argument |
| -[pP] | print the iv/key (then exit if -P) |

# Part 2: Encryption Mode - ECB vs. CBC #

The file `pic_original.bmp` contains a simple picture. We would like to encrypt this picture so that people without the encryption keys cannot know what is in the picture. Please encrypt the file using the ECB (Electronic Code Book) and CBC (Cipher Block Chaining) modes.

Let us treat the encrypted pictures as a picture, and use a picture viewing software such as `eog` to display it. However, for the .bmp file format, the first 54 bytes contain the header information about the picture. We have to set the header correctly so that the encrypted file can still be treated as a legitimate .bmp file.

We will replace the header of the encrypted picture with that of the original picture. You can use the `hexedit` tool to directly modify binary files. The original picture's 54 byte picture header should look something like this:

	42 4D E4 54  02 00 00 00  00 00 3E 00  00 00 28 00
	00 00 44 04  00 00 43 04  00 00 01 00  01 00 00 00
	00 00 00 00  00 00 80 3D  00 00 80 3D  00 00 00 00
	00 00 00 00  00 00

**Question 1:** Display the encrypted pictures using any picture viewing software. Can you derive any useful information about the original picture from the encrypted picture? Please explain your observations.

# Part 3: Encryption Mode - Corrupted Cipher Text #

To understand the properties of various encryption modes, do the following:

1. Create a text file that is at least 64 bytes long.
2. Encrypt the file using the AES-128 cipher.
3. Unfortunately, a single **bit** of the 30th byte in the encrypted file got corrupted. You can achieve this corruption with `hexedit`.
4. Decrypt the corrupted file (encrypted) using the correct key and IV.

**Question 2:** *Before doing Part 3*, how much information do you expect to recover by decrypting the corrupted file, if the encryption mode is ECB, CBC, CFB, or OFB, respectively? Please explain why.

**Question 3:** *After doing Part 3*, did your expectations from question 2 align with the results? What are the implications of these encryption mode differences?

# Part 4: Padding #

For block ciphers, when the size of the plaintext is not the multiple of the block size, padding may be required. In this task, we will study padding schemes.

*Task 1:* The openssl manual says that it uses the PKCS5 standard for its padding. Please design an experiment to verify this. In particular, use your experiment to figure out the paddings in the AES encryption when the length of the plaintext is 20 octets and 32 octets.

**Question 4:** Please report the findings of your experiment.

*Task 2:* Please use ECB, CBC, CFB, and OFB modes to encrypt a file (you can pick any cipher).

**Question 5:** Which operating modes require padding? Why do the others not require padding?

# Questions #

Answer the following questions and submit them in `report.txt`.

1. Can you derive any useful information about the original picture from the encrypted picture? Please explain your observations.
2. *Before doing Part 3*, how much information do you expect to recover by decrypting the corrupted file, if the encryption mode is ECB, CBC, CFB, or OFB, respectively? Please explain why.
3. *After doing Part 3*, did your expectations from question 2 align with the results? What are the implications of these encryption mode differences?
4. Please report the findings of your experiment in Part 4.
5. Which operating modes require padding? Why do the others not require padding?

# Submission #

You will be submitting one file:

- `report.txt` Your answers
