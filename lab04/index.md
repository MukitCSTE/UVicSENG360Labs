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

Let us treat the encrypted picture as a picture, and use a picture viewing software such as `eog` to display it. However, for the .bmp file format, the first 54 bytes contain the header information about the picture. We have to set the header correctly so that the encrypted file can still be treated as a legitimate .bmp file. We will replace the header of the encrypted picture with that of the original picture. You can use the `ghex` tool to directly modify binary files.

**Question 1:** Display the encrypted pictures using any picture viewing software. Can you derive any useful information about the original picture from the encrypted picture? Please explain your observations.

# Part 3: Encryption Mode - Corrupted Cipher Text #

# Part 4: Padding #

# Questions #

Answer the following questions and submit them in `report.txt`.

1. (From Part 1): Can you derive any useful information about the original picture from the encrypted picture? Please explain your observations.

# Submission #

You will be submitting one file:

- `report.txt` Your answers
