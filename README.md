## Sign-in to the local karaoke place and get song recommendations

This evening project starts with a short conversation the night before:

> Hey Rishabh, my friends and I are thinking about going to a karaoke bar. Wanna come?

"Maybe? I don't know, I don't really know that many pop songs."

> Hm. Well, you can look at the song list on their website, find something you like.

"Oh! Okay then."


I went to the website, looked at the song list, found a dozen Black Sabbath songs, and told my friend "Sure, I'll go".

----

Then I wrote this script to pull my listening history from my Last.FM profile and match it against the karaoke bar's database.


### Execution
1. Register your Last.FM account with the Last.FM API. [Details here](https://www.last.fm/api#getting-started).

2. Edit config.txt to include your Last.FM username and API key obtained in step 1.

3. Run `main.py` with Python.

4. Step 3 will likely fail to run because you need some package dependencies. Read the error message, install what it says, and GOTO step 3. 

Once the script has finished running, the output will be stored in a tab-separated file `songs.tsv`. Read it with a text-editor or spreadsheet software.

### Design

This script will take a while to run. I don't want to overload my local karaoke's database, so I space my queries out randomly.
The default mean period is 0.3 seconds per artist. This may be adjusted in `main.py`.