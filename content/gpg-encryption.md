Title: Encrypting files using PGP/GPG
Date: 2020-11-08
Category: Programming
Tags: security, encryption

This past week I had to encrypt several sensitive files before transmitting
them to a third party vendor we were working with. It being my first time doing
such a thing, I read up on the PGP encryption algorithm and and learned how to work with
GnuPG (gpg), the open source implementation of PGP. My first impression: `gpg` is a
mature software with an easy-to-use interface, provided you read the first few
pages of the [GNU Privacy
Handbook](https://www.gnupg.org/gph/en/manual/c14.html)

## Cheatsheet
description|command
---|---
create a key pair | `gpg --gen-key`
list keys | `gpg --list-keys`
export a public key | `gpg --export --armor > pubkey.asc`
import a public key | `gpg --import pubkey.asc`
encrypt a file | `gpg --encrypt --recipient 'name/email/sha' file.txt`
decrypt a file | `gpg [--decrypt] file.txt.gpg`

When encrypting a file, you may specify more than one `--recipient`.

When decrypting a file, passing `--decrypt` will print to stdout instead of
saving to a file.

## Resources

* [How To Use GPG on the Command
  Line](https://blog.ghostinthemachines.com/2015/03/01/how-to-use-gpg-command-line/)
* [The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual/c14.html)
* [Email Self-Defense - a guide to fighting surveillance with GnuPG
  encryption](https://emailselfdefense.fsf.org/en/)
