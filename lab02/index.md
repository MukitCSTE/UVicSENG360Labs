# Public Key Encryption #

In this lab you will learn how to use public key encryption software. You will be working in groups of 2-3. We *strongly* recommend working on the lab machines instead of your own laptops this week.

This lab will use gpg GNU Privacy Guard. [https://www.gnupg.org/](https://www.gnupg.org/). Its documentation is at [https://www.gnupg.org/documentation/index.html](https://www.gnupg.org/documentation/index.html) or using the command `man gpg`.

You will need hojs-public.key.asc from CourseSpaces.

## Learning Objectives ##

- Apply public-key cryptography for encryption and digital signing
- Apply basic strategies for secure key exchange and validation
- Describe basic principles of the web of trust
- Describe the use of revocation certificates

# Part 0: Command Logging #

Create a new file named `log.txt`. As you go through this lab, please copy the commands you executed in the terminal here.

# Part 1: Public/Private Key Creation #

Before we can do anything, we must create a key-pair. For each of you, in your corresponding accounts, generate a key-pair:

	gpg --gen-key

You will see four kinds of options. Options 1 and 2 create two key pairs; one for signing and the other for encrypting. Options 3 and 4 only create keys for signing.

Choose options: (1) RSA and RSA (default), and a keysize of 2048 bits.

Indicate that the key should expire in 90 days (at least) so that I can use your key.  Use your netlink email as the email of your key. You will also be asked for a *pass-phrase* for the key. This is a password that will protect your key from prying eyes. Make sure you can remember this pass-phrase or you will never be able to use the key. You will be asked to generate entropy also (shake that mouse!).

# Part 2: Key Import/Export #

At this point you have created a pair of private/public keys, but it's no use if only you know it.

## Key Export ##

For somebody to contact you privately, they would need your public key. Let us export it in ASCII-armored format. Type:

	gpg --export -a

You will get an output something like like this:

	-----BEGIN PGP PUBLIC KEY BLOCK-----
	Version: GnuPG v2.0.22 (GNU/Linux)

	...

	-----END PGP PUBLIC KEY BLOCK-----


In general, gpg has two ways of exporting keys: binary and ASCII-armored. Since binary keys may be inconvenient to handle, we will stick with the ASCII-armored version. The `-a` flag tells gpg to use ASCII-armoring.

Normally, `.sig` is used for detached signatures using the binary OpenPGP format, and `.asc` for when the contents are ASCII-armored. For everything else, `.gpg` is common for the binary format, and `.asc` when armored.

Save your public key (redirect the output of pgp to a file) in the format `lastname_firstname.key.asc` and share your public key file with your lab partner and at least 4 other people in the lab.

You may use email or the shared file system in the lab. Please *do not* use USB flash drives on these lab machines. The shared file system in the lab is mounted at `/seng/seng360`.

- Please use the `lab02` folder in the mount for sharing your files.
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

# Part 5: Using a Public Key Server #

Besides sending your public key to others, you can also use a public key server to openly publish your public key to anyone. The key server acts as the "white pages" for public keys. To publish your keys, you will use the `gpg --keyserver` command.

Many keyservers exist; in this lab you will be using [pgp.mit.edu](http://pgp.mit.edu/). Publish your own key with the following command:

	gpg --keyserver pgp.mit.edu --send-key <keyid>

Your keyid is the hexadecimal number in the "pub" column when you list the keys. For example, `94CF0AE4` is the public keyid for Jon Smith.

	$ gpg --list-keys
	------------------------------
	pub 4096R/94CF0AE4 2010-08-17
	uid 			   Jon Smith <jsmith@somedomain.com>
	sub 4096R/CCB47665 2010-08-17

Once you've published your own key, search for your partner's public key on [http://pgp.mit.edu/](http://pgp.mit.edu/) via their email or name. Note their keyid and then import it:

	gpg --keyserver pgp.mit.edu --recv-key <keyid>

- If this is the same key you imported from earlier, you will see an "unchanged" message.

# Part 6: Key Validation #

How can you know that the key somebody sends you (or that you have downloaded from a key server) is authentic? An adversary may try to trick you into thinking that the key was authentic, when it may not be.

Of course, you could validate the key “out of band” with the original owner for example by talking to them on the phone or by exchanging a piece of paper. However, the key may be quite long - and this may be a laborious task.

Alternatively, you can create a short hash of the key (called the fingerprint) and compare that instead. Then you can sign the key with your key if you trust it.

Open your partner's key to inspect:

	gpg --edit-key <email>

Then get the key's fingerprint:

	Command> fpr

With this fingerprint, talk to your partner to make sure this is the right key. Once verified, go ahead and sign the key:

	Command> sign

Congratulations, you have now validated your partner's key.

# Part 7: Web of Trust #

*This section may be difficult. If you are not able to do it successfully, at least make sure you understand what it does and why it is used.*

In the previous section, a procedure was given to validate your correspondents' public keys: a correspondent's key is validated by personally checking his/her key's "fingerprint" and then signing his/her public key with your private key. By personally checking the "fingerprint" you can be sure that the key really does belong to him/her, and since you have signed the key, you can be sure to detect any tampering with it in the future. Unfortunately, this procedure is awkward when either you must validate a large number of keys or communicate with people whom you do not know personally.

GnuPG addresses this problem with a mechanism popularly known as the web of trust. In the web of trust model, responsibility for validating public keys is delegated to people you trust. For example, suppose

- Alice has signed Blake's key, and
- Blake has signed Chloe's key and Dharma's key.

If Alice trusts Blake to properly validate keys that he signs, then Alice can infer that Chloe's and Dharma's keys are valid without having to personally check them. She simply uses her validated copy of Blake's public key to check that Blake's signatures on Chloe's and Dharma's are good. In general, assuming that Alice fully trusts everybody to properly validate keys they sign, then any key signed by a valid key is also considered valid.!e root is Alice's key, which is axiomatically assumed to be valid.

In practice trust is subjective. For example, Blake's key is valid to Alice since she signed it, but she may not trust Blake to properly validate keys that he signs. In that case, she would not take Chloe's and Dharma's key as valid based on Blake's signatures alone. The web of trust model accounts for this by associating with each public key on your keyring an indication of how much you trust the key's owner. There are four trust levels.

1. **unknown**: Nothing is known about the owner's judgment in key signing. Keys on your public keyring that you do not own initially have this trust level.
2. **none**: The owner is known to improperly sign other keys.
3. **marginal**: The owner understands the implications of key signing and properly validates keys before signing them.
4. **full**: The owner has an excellent understanding of key signing, and his signature on a key would be as good as your own.

A key's trust level is something that you alone assign to the key, and it is considered private information. It is not packaged with the key when it is exported; it is even stored separately from your keyrings in a separate database.

The GnuPG key editor may be used to adjust your trust in a key's owner. The command is `trust`. In this example, Alice edits her trust in Blake and then updates the trust database to recompute
which keys are valid based on her new trust in Blake.

	alice% gpg --edit-key blake
	Command> trust
	Please decide how far you trust this user to correctly verify other users'
	keys
	(by looking at passports, checking fingerprints from different sources, etc.)
	1 = I don't know or won't say
	2 = I do NOT trust
	3 = I trust marginally
	4 = I trust fully
	5 = I trust ultimately
	m = back to the main menu
	Your decision? 3
	pub 1024D/8B927C8A created: 1999-07-02 expires: never trust: m/f
	sub 1024g/C19EA233 created: 1999-07-02 expires: never
	(1) Blake (Executioner) <blake@cyb.org>
	Command> quit
	[...]

The web of trust allows an algorithm to be used to validate a key. Formerly, a key was considered valid only if you signed it personally. A more flexible algorithm can now be used: a key K is considered valid if:

- It is signed by enough valid keys:
	- You have signed it personally, or
	- It has been signed by one fully trusted key, or
	- It has been signed by three marginally trusted keys; and the path of signed keys leading from K back to your own key is no larger than five steps.

## Task ##

Try out indirect key validation. Reform into groups of three and build a chain of trust with three links:

- Student B knows Student A and signs Student A's key
- Student C fully trusts Student B

Have student C import the public key of Student A and B.

Check that Student A's public key is considered valid in the keyring of Student C. You can do that by `gpg --edit-key`. (Look into the `trust` and `validity` commands.

# Part 8: Certificate Revocation #

If you forget your passphrase or your private key is compromised/lost, you can issue a revocation certificate to let others know not to use that public key any longer. A revoked public key can still be used to verify signatures made by you in the past, but you cannot use it to encrypt future messages to you. It also does not affect your ability to decrypt messages sent to you in the past if you still have access to that key.

Create a revocation of your key:

	gpg --output revoke.asc --gen-revoke <keyid>

Send `revoke.asc` to your partner and have them import it. Can you still send your partner an encrypted document? Can you still decrypt or validate the signature of documents from your partner from the previous sections?

# Questions #

Answer the following questions and submit them in `report.txt`.

1. Modify your original signed file from Part 4 and then verify the validity of the signature. What happens?
2. Explain the Web of Trust in your own words. What does it accomplish? Why is this used?
3. Send `revoke.asc` to your partner and have them import it.
	- Can you still send your partner an encrypted document?
	- Can you still decrypt or validate the signature of your partner's documents from the earlier sections?
4. We covered 3 main security properties. (Hint: CIA) For each of them:
	- Does cryptography address it?
	- If so, how?
	- Can cryptography address non-repudiation? How?

# Submission #

You will be submitting five files in one zip file:

- `lastname_firstname.key.asc` Your public key in ASCII format
- `report.txt` Your answers in **plain-text**
- `report.txt.sig` Detached signature of your report
- `report.txt.asc` Encrypted file with the TA as the recipient
- `log.txt` Log of commands you ran

Make sure you digitally sign your answers file as a **detached signature**. Zip up your files and submit them on CourseSpaces.
