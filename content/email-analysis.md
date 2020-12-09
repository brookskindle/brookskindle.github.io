Title: I analyzed over 3 gigabytes of email (my own)
Date: 2020-10-02
Category: programming
Tags: python, data

How often do you get excited when your phone vibrates and an email notification
shows up? If you're like me, not very. Much like how I only seem to receive
spam calls on my phone, almost all of the emails I receive on a daily basis are
not important to me. I get emails about sales I don't care about, terms of
service updates for services I forgot I was using, the latest updates on social
media sites that I rarely log in to, and a plethora of other marketing type
emails I have absolutely zero interest in reading.

Most of the time I archive the mail and move on with my day, but recently I
took a sabbatical from email (read: I turned off notifications for the Gmail
app) and was amazed at the amount of clutter that my inbox was filled with upon
return. Some emails were important (luckily, not many time-sensitive ones), but
most held no value to me.

**Just many emails do I unconsciously sift through on a daily basis?**

It never really goes down, does it? Signing up for things online presents such
a low barrier to entry that hardly a second thought is given to the act if
there's an app, site, or game I want to try out. Perhaps that's the consumer
culture side of me talking. Do you remember the last time you deleted an online
account of yours?

**How many sites support the deletion of accounts?**

Not enough, I think. Perhaps I should take a cue from my tendency to [fresh
install my operating system every six months](/arch-install.md) and start fresh
with a new email address, and maybe one day I will. But it is not today.

**Today we will analyze my emails to figure out who the most frequent sender
is.**

Google has a convenient interface for accessing all of your user data,
including emails if you use gmail.

![]({static}/images/google-takeout.png)

After requesting a data export, Google will send an email with a link when the
data is ready to be downloaded.

![]({static}/images/gmail-download-ready.png)

I chose a gzipped tar file format (`.tgz`), so I can uncompress it using
`gunzip` and `tar`.

```console
$ gunzip takeout-20200923T060647Z-001.tgz
$ tar -xvf takeout-20200924T022153Z-001.tar
Takeout/Mail/User Settings/Forwarding Addresses.json
Takeout/Mail/User Settings/Blocked Addresses.json
Takeout/Mail/User Settings/Signatures.json
Takeout/Mail/User Settings/Filters.json
Takeout/Mail/All mail Including Spam and Trash.mbox
Takeout/archive_browser.html
$ ls
Takeout
takeout-20200924T022153Z-001.tar
```

The only important file in this list is `All mail Including Spam and
Trash.mbox`. This file is huge - 3.1 gigabytes! Mbox format? I'm not very
familiar with it, but let's see what the format looks like.

```
From 23402857298734987239487@xxx Sun Sep 20 00:38:32 +0000 2020

X-GM-THRID: 358234987239487293847

X-Gmail-Labels: Inbox,Important,Category Personal,Unread

Delivered-To: .............

Received:

        Sat, 19 Sep 2020 17:38:32 -0700 (PDT)

X-Received:

        Sat, 19 Sep 2020 17:38:32 -0700 (PDT)

ARC-Seal: i=1; a=rsa-sha256; t=1600562312; cv=none;

ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;

ARC-Authentication-Results: i=1; mx.google.com;

Return-Path: <name@domain.com>

Received: from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])

Received-SPF: pass ()

Authentication-Results: mx.google.com;

DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;

X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;

X-Gm-Message-State:

X-Google-Smtp-Source:

X-Received:

 Sat, 19 Sep 2020 17:38:31 -0700 (PDT)

MIME-Version: 1.0

From: firstname lastname <name@address.com>

Date: Sat, 19 Sep 2020 17:38:17 -0700

Message-ID: <>

Subject: ......

To: .....

Content-Type: multipart/alternative;

Content-Type: text/plain; charset="UTF-8"



<content>
```

For the most part it looks like plain text with `Name:` type headers. Luckily,
python has an mbox library in the stdlib module `mailbox`, so I don't need to
make my own parser for it. Of these fields, I'm really only interested in a
select few.

This is the script I wrote to parse my mbox file and create a csv of the
interesting fields

```python
#!/usr/bin/env python
import sys
import mailbox
import csv

# pip install python-dateutil
from dateutil.parser import parse

inbox = mailbox.mbox(sys.argv[1])
writer = csv.writer(sys.stdout)

headers = ["X-Gmail-Labels", "From", "Date", "To", "Subject"]
writer.writerow(headers)

for msg in inbox:
    row = [msg.get(header) for header in headers]
    if row[2] is not None:  # Date
        try:
            row[2] = parse(row[2]).isoformat()
        except Exception as err:
            print(err, file=sys.stderr)
    writer.writerow(row)
```
Short and sweet, it accepts a filename as the first command line argument, and
prints csv lines to stdout. There are a couple of checks and type conversions I
included because as I was analyzing the file, I noticed a couple of things

* not every email has a date
* not all dates have the same format

Kind of strange, but nothing we can't work around. For now, let's get this data
into a usable form.

```console
$ checkmail.py All\ mail\ Including\ Spam\ and\ Trash.mbox > mail.csv
```

Normally at this point I would use pandas to load the csv file into a DataFrame
and analyze it, but I've enjoyed using
[visidata](https://github.com/saulpw/visidata), a general purpose spreadsheet
tool built for the command line. It allows interactive searching, filtering,
and aggregations on the data in question. With it, I was able to easily
determine the most frequent sender.

```console
$ vd mail.csv
```

To keep things practical, I restricted the search to the past two years instead
of for all time. For privacy reasons, I will not share most of the results, but
here are some of the interesting ones.
```
domain               count   percent    histogram
linkedin.com         442     14.21	    **************************************************
google.com           225     7.23	    *************************
mint.com             131     4.21	    **************
pagerduty.com        95      3.05	    **********
gmail.com            91      2.93       **********
github.com           88      2.83       *********
indiehackers.com     39      1.25       ****
amazon.com           36      1.16       ****
steampowered.com     32      1.03       ***
```

Hold on. LinkedIn accounts for fourteen percent? I'm barely active on that
site, yet it comprises the lion's share of email I receive.

There's not much I can do about PagerDuty emails, because those are work alerts
and I want to get them. Same with GitHub. It's not work, but I do want to know
when someone responds to a thread that I posted on, or creates an issue in one
of my repositories.

---

And that's all. Armed this knowledge, I was able to modify my email
notification preferences on a lot of the email-happy sites. Only time will tell
how successful it is.

This project was one part research to figure out how to reduce email clutter,
and another part data exploration just for the fun of it. I didn't showcase
much of `visidata`, because it's an interactive tool and it would be hard to
demo it with this dataset, given how much sensitive information there is, but
if you enjoy working with data and like using the command line, the [lightning
demo](https://www.youtube.com/watch?v=N1CBDTgGtOU&list=PLxu7QdBkC7drrAGfYzatPGVHIpv4Et46W)
video will blow your socks off.

Until next time.
