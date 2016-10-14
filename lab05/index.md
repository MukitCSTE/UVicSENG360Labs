# Certificates and Certificate Authorities #

As we have seen, symmetric cryptography can be effective, but it has the problem of key-distribution (it requires a pair of keys for every pair of entities wishing to communicate). Public key cryptography alleviates this. Nonetheless, it is still necessary to distribute keys, and equally important, to be able to
authenticate the entity (person or process) we communicate with.

Public Key Infrastructure (PKI) is a mechanism to do solve these problems. The basic premise is that any entity in the system should have a valid certificate that identifies the entity. The certificate is signed by a certificate authority, validating the entity. Go to the Wikipedia and read about them:

- [https://en.wikipedia.org/wiki/Public_key_infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure)
- [https://en.wikipedia.org/wiki/Certificate_authority](https://en.wikipedia.org/wiki/Certificate_authority)

## Certificates and SSL/TLS ##

SSL (and its successor TLS) is the protocol behind the secure Web can use certificates for authentication purposes. It is based on the idea of "Root Certification Authorities" (Root CAs). These CAs (see [https://en.wikipedia.org/wiki/Certificate_authority#Providers](https://en.wikipedia.org/wiki/Certificate_authority#Providers)) sign certificates of organizations. Then such organizations sign certificates of its entities.  In order to verify a certificate, we verify the chain of signatures in those certificates.

Is the certificate in question signed by a valid CA?  If not, was it signed by a CA that was signed by a known CA? We do this recursively until the certificate is signed by a CA, or we cannot further verify the signature. Anybody with a signed certificate can sign other certificates.

However, having a certificate signed by a Root CA costs money (see [https://www.thawte.com/ssl/](https://www.thawte.com/ssl/)). What is even worse is that these certificates are only valid for one year. Talk about printing money!

# Part 1: Web and CAs #

If you are going to do e-commerce you must buy a valid CA from one of the Web CAs. There is no way around it, unfortunately. This will allow any browser to authenticate your server (to this day the practice is that we don't authenticate users, only servers, one day this might change).

Start Firefox and go to [http://www.wolframalpha.com/](http://www.wolframalpha.com/). Click on the icon just before the URL (looks like a globe or world). Click on "More Information". Under "Technical Details" it will tell you that the connection is not encrypted. This is expected.

Now head to [https://www.uvic.ca](https://www.uvic.ca). Click again on the icon (this time a small green lock).

**Question 1** Who is its Signing CA?

Now visit [https://gerrit.seng.uvic.ca:8088/](https://gerrit.seng.uvic.ca:8088/). (Please note that you can only access this page on a UVic network). You should encounter a connection not secure error.

**Question 2** What is the problem with this site?

# Part 2: Using OpenSSL to verify certificates #

OpenSSL is a library but it is also a collection of tools. Download the certificates of the two https sites from Part 1 using openssl. Port 443 is default for https.

	echo -n | openssl s_client -connect <hostname>:<port>

**Question 3** Who is the issuer of each certificate?

As you can see, one of them comes from a CA and the other is self-signed. More on that later.

Save the certificate of *www.uvic.ca* into a file `uvic.cert`. It starts with `-----BEGIN CERTIFICATE-----` and ends with `-----END CERTIFICATE-----`.

## Verifying a Certificate ##

Run openssl with these options on the two sites (uvic.ca on port 443 and gerrit.seng.uvic.ca on port 8088).

	echo -n | openssl s_client -verify_return_error -connect <hostname>:<port>

Look for the Certificate chain section. The Certificate chain is the way in which the certification is verified.

# Part 3: Encryption used by a server and a client #

At the end of the output of openssl you see the description of the encryption achieved. SSL negotiates and uses the best encryption that both sides (client and server) are able to support. This is stated in the `Cipher` field of the SSL-session data.

**Question 4:** What is the cipher achieved between the Lab machine you are using and the following servers: [www.uvic.ca](https://www.uvic.ca), [www.gmail.com](https://www.gmail.com), and [facebook.com](https://facebook.com). 

The cipher is "encoded". See [https://www.openssl.org/docs/manmaster/apps/ciphers.html](https://www.openssl.org/docs/manmaster/apps/ciphers.html) for details. The cipher reported is an abbreviation (see bottom of page for the full name). Each section of the cipher documents one part of it. At the very least it has two parts. From the right: first is the MAC, then the block cipher or stream cipher used and its blocking mode (if applicable). Then it comes the authentication method, and finally, the key exchange algorithm.

**Question 5:** For each of the three servers from Question 4, decode the cipher method into each of its sections.

Read the following websites:  
[https://blogs.technet.com/b/srd/archive/2013/11/12/security-advisory-2868725-recommendation-to-disable-rc4.aspx](https://blogs.technet.com/b/srd/archive/2013/11/12/security-advisory-2868725-recommendation-to-disable-rc4.aspx)  
[https://www.rc4nomore.com/](https://www.rc4nomore.com/)

**Question 6:** What conclusion do you reach about servers which use the old (and deprecated) RC4 cipher?

# Part 4: Self-signing your own certificates #

There are many reasons why we might want to sign our own certificates (saving money is one of them). An example use-case is running your own VPN client and having it use TLS to authenticate the client and the server. To learn to do this, take a look at the tutorial here: [https://pki-tutorial.readthedocs.io/en/latest/simple/](https://pki-tutorial.readthedocs.io/en/latest/simple/)

- Pay close attention to the DN components. If the domain doesn't match simple.org as the tutorial specifies, you may be unable to sign.
- If you think you messed up, do the following to reset: `git clean -f -d`

**Question 7:** Once you are done with Part 4, do a `history` and copy your Part 4 commands as your answer to this question.

# Appendix #

As you can probably tell, using https is not only recommended, but also must be done properly. There are some resources out there that can help you acquire your own trusted SSL certificate: [https://letsencrypt.org/](https://letsencrypt.org/)

Ensuring most websites you visit default to https: [https://www.eff.org/https-everywhere](https://www.eff.org/https-everywhere)

# Submission #

You will be submitting one file:

- `report.txt` Your answers to the 7 questions
