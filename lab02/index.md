# Public Key Encryption #

In this lab you will learn how to use public key encryption software. You will be working in groups of 2. We *strongly* recommend working on the lab machines instead of your own laptops this week.

This lab will use gpg GNU Privacy Guard. [https://www.gnupg.org/](https://www.gnupg.org/). Its documentation is at [https://www.gnupg.org/documentation/index.html](https://www.gnupg.org/documentation/index.html) or using the command `man gpg`.

You will need hojs-public.key.asc from CourseSpaces.

## Learning Objectives ##

- Apply public-key cryptography for encryption and digital signing
- Apply basic strategies for secure key exchange and validation
- Describe basic principles of the web of trust
- Describe the use of revocation certificates

# Part 0: Command Logging #

Create a new file named `log.txt`. As you go through this lab, please copy the commands you executed in the terminal here.

# Part 1: Create a personal public/private key #

Before we can do anything, we must create a key-pair. For each of you, in your corresponding accounts, generate a key-pair:

	gpg --gen-key

You will see four kinds of options. Options 1 and 2 create two key pairs; one for signing and the other for encrypting. Options 3 and 4 only create keys for signing.

Choose options: (1) RSA and RSA (default), and a keysize of 2048 bits.

Indicate that the key should expire in 90 days (at least) so that I can use your key.  Use your netlink email as the email of your key. You will also be asked for a *pass-phrase* for the key. This is a password that will protect your key from prying eyes. Make sure you can remember this pass-phrase or you will never be able to use the key. You will be asked to generate entropy also (shake that mouse!).

# Part 2: Import/Export your keys #

At this point you have created a pair of private/public keys, but it's no use if only you know it.

## Key Export ##

For somebody to contact you privately, they would need your public key. Let us export it in ASCII-armored format. Type:

	gpg --export -a

You will get an output something like like this:

	-----BEGIN PGP PUBLIC KEY BLOCK-----
	Version: GnuPG v2.0.22 (GNU/Linux)
	
	mQENBFYErFwBCACsGF8QDAwhQsiGSPkQ2p6CY9Q5TtBgBt0vl0n23NbDeZYoCSqu
	MMM+n7NbqPNLGqiL8LRCShXuG5IwGIIPMc1RmZPfQVWNZD6gdkqJOGVCI8pSOrP/
	YBiCr9eT70ZMYapSHVBhsNgIVe/NYr0qFwg776UIAd/pfy5d5n2ogHHzqC9+BvNj
	3sGAiL50UXxwKk8Z5UCM1fOBc1W31ue26it9h2yhUos4Lxpdlu9tmw4oVxoz1xTv
	vwZSswpRAEKOyMZAkPpDyZTuhiRSjbFVKPI6ca/qyGtSQf8qF2+zHYMT2g6mGH8t
	TvPobJmVIy9a8AjyPSQdo7jWjxb1CO9jNo//ABEBAAG0JUplcmVteSBIbyAoU0VO
	RzM2MEYxNSkgPGhvanNAdXZpYy5jYT6JAT8EEwECACkFAlYErFwCGwMFCQB2pwAH
	CwkIBwMCAQYVCAIJCgsEFgIDAQIeAQIXgAAKCRAS3OjjZcm9g+DGB/0TaMvgLsMh
	MWf6PUudTicZVWTfNgvNtIX+bT+4nBjcLgGtVbyCI0Woju/hzqAAtWIJo1E7MZYz
	Q+azchEGF+0prHIjx0zZ3dCnTbMV6g1L8+rzjDb76XLmewXVgLgkR0xKDg1WyKlM
	IS0/4ektfxAZ8s9zCkMznhToOlfH2akrdG0qE/avYAxo3kFyCVzG5z96OSAa9xbT
	d5/cmgwQ97K6HKTas7vHV7gIhXSP/HoFRIRbgV4kYUM7V95Qlw/Ll1X0NYET6I4R
	SoKu52J/45E5CQe0M1unV5O04JB5cIIzO3FQvjbjUiBE0GXAjGFYyO9TAUD/eafE
	qXavGe/+cOshuQENBFYErFwBCADAykoEdkVquZr4zKRhLy9GZwCod2BkDfz9nPzA
	RZzlg3mSmujguFBX7txoQMoMxQkQgtNHCfZ0JfTqD7NY6pASaCdJnzrOxgn59b4i
	I9JI4ieS1gD2LKO5aq9xmMV+zOZXAWg1UI9odkVz8knXU/ouvXs81jSO1WXBgS59
	1mo3iW8ahJcobNw8Tnwp4xE0o4gaUeR/j1ek3yurNRiQ5fvgn334uOU0PDwv3eYV
	b0EqBEFkvONdI6n1EGgUVbd3YQTegZZsfCVfa9VtAgKiIjY4Pp3Y045k711AvNPM
	ZGto5V4ipGx05FijJzEYwqCdA7BMd1QOsJ3r0ads6167E8cJABEBAAGJASUEGAEC
	AA8FAlYErFwCGwwFCQB2pwAACgkQEtzo42XJvYMRGgf9HF2jrja7four+05ZxaNL
	2Ecnolv5yF1hfgGOv9t9cl0YlMnyxkjAni4z+mMZjqybFp7MBU9GHeK3l64KoeOz
	1q5JtYFBjHH6VpJnceDYHmpnB6Un9gQirnluQpeBS/6ahakblNHE5EhRdGblKzAE
	TcDgfaaing6zkEc3uOHixgFzacWp0Ti1e2QN0er20bLYjot4vCeTIkgigOcrANGc
	eHhMGRGpsf2tdQnKO55j4usb1FNjq61P5ON06FQ/rfwSp9tEmN87C55wKp/ZpZdt
	C/0AffLQLL+kYrtuy4sV+3qVM0fd/kObDiPLumzskmvD3/CZ5cb1YA0NhaxnMsW/
	/A==
	=hfdN
	-----END PGP PUBLIC KEY BLOCK-----


This in fact is my public key. In general, gpg has two ways of exporting keys: binary and ASCII-armored. Since binary keys may be inconvenient to handle, we will stick with the ASCII-armored version. The `-a` flag tells gpg to use ASCII-armoring.

Normally, `.sig` is used for detached signatures using the binary OpenPGP format, and `.asc` for when the contents are ASCII-armored. For everything else, `.gpg` is common for the binary format, and `.asc` when armored.

Save your public key (redirect the output of pgp to a file) in the format `lastname_firstname.key.asc` and share your public key file with your lab partner and at least 4 other people in the lab.

You may use email or the shared file system in the lab. Please *do not* use USB flash drives on these lab machines. The shared file system in the lab is mounted at `/seng/seng360`.

- Please remember that since this is a shared folder, anyone else can access the files stored here.
- If you do choose to use the shared folder, make sure to clean-up after yourself and delete the files you added before you leave the lab.

## Key Import ##

Download from CourseSpaces the file with my key (hojs-public.key.asc). Import them into your keyring.

	gpg --import hojs-public.key.asc

Do the same for the other 4 public keys you have received.

## List Keys ##

List all the keys in your keyring:

	gpg --list-key

It should list your own key as well as all the other keys you have imported.

# Part 3: Encryption #

We are ready to encrypt some data. Create a simple text file and write in it a simple message. A good way to create a blank file is the `touch` command.

Encrypt the file for your lab partner. Let us do in ascii-armor format (base64 encoded so it can be easily transferred):

	gpg --encrypt -a -r <recipient email> <filename>

This will create the encrypted file as `<filename>.asc`

Before you give it to your lab partner to decode, try it yourself:

	gpg --decrypt <filename>

As you can see, the encrypted file contains the name of the recipient who is the only one who can decode the file.

Give it to your partner and decode it.

## Symmetric cryptography ##

*This section requires that you meet with a different team to collaborate with.*

You can also use symmetric cryptography. Run

	gpg --version

to see what the current algorithms are. They can be divided into three groups: symmetric algorithms, public key, and hashing algorithms. Look up the full names of these acronyms.

Encrypt a file using BlowFish with a key (do not use the same passphrase you used earlier for your public key-pair).

	gpg --symmetric --cipher-algo blowfish <filename>

This will create a file named `<filename>.gpg`.

Now, if you send an encrypted file to another person, the problem is sharing that key. You can solve that problem by encrypting the key.

Create a simple text file called `key.txt`. In it, include only the key you used to encrypt the file.

Get the public key of a member of another team. Encrypt `key.txt` with their key. Send this person the encrypted file and the encrypted key and have them decrypt it. At some point, their team should send you their corresponding encrypted file and encrypted key. Decrypt it.

	gpg -d <filename>

# Part 4: Digital Signatures #

We can also sign documents using our private key.

	gpg --sign -a <filename>

This will create a file `<filename>.asc`. Inspect it. You can either check the signature of the signed document with `--verify` or you can recover the original document with `--decrypt`.

Pass this file to your teammate and see if he/she can verify the key:

	gpg --verify message.txt.asc

You probably got a message that says that there is no indication that the signature belongs to the owner.

	gpg: Signature made Mon 28 Sep 2015 01:46:47 PM PDT using RSA key ID 65C9BD83
	gpg: Good signature from "Jeremy Ho (SENG360F15) <hojs@uvic.ca>" [uncertain]
	gpg: WARNING: This key is not certified with a trusted signature!
	gpg:          There is no indication that the signature belongs to the owner.

You can read about the keys of others, to make sure that those keys come from the people who they claim to be.

Signing documents in this manner has limited usefulness since recovering the original document requires that you edit the original signed document. A way to avoid this is by creating a detached signature via `--detach-sig`. This will create a separate file.

	gpg --detach-sig <filename>

In this case only the signature will be included in the file `<filename>.sig`. You will need both the source file and the signature file to verify it:

	gpg --verify <signature> <filename>

# Questions #

Answer the following questions and submit them in `report.txt`.

- 1) Modify the original signed file and then verify the validity of the signature. What happens?
- 2) We covered 3 main security properties. For each of them:
	- Does cryptography address it?
	- If so, how?
	- Can cryptography address non-repudiation? How?

# Submission #

You will be submitting four files in one zip file:

- `lastname_firstname.key.asc` Your public key
- `report.txt` Your answers
- `report.txt.sig` Detached signature of your report
- `log.txt` Log of commands you ran

Make sure you digitally sign your answers file as a **detached signature**. Zip up your 4 files and submit them to CourseSpaces.
