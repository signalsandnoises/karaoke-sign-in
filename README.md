## Sign-in to the local karaoke place and get song recommendations

This evening project starts with a short conversation the night before:

> Hey Rishabh, my friends and I are thinking about going to a karaoke bar. Wanna come?

"Maybe? I don't know, I don't really know that many pop songs."

> Hm. Well, you can look at the song list on their website, find something you like.

"Oh! Okay then."


I went to the website, looked at the song list, found a dozen Black Sabbath songs, and told my friend "Sure, I'll go".

----

Then I wrote this script to pull my listening history from my Last.FM profile and match it against the karaoke bar's database.


## Execution

1. Register your Last.FM account with the Last.FM API. [Details here](https://www.last.fm/api#getting-started).

2. Copy `config/config.ini.sample` to `config/config.ini` 

3. Edit `config/config.ini` to include your Last.FM username and API key obtained in step 1.

### Run Locally

4. Create a python virtualenv (`python -m virtualenv venv`) and activate it (`source venv/bin/activate`)

5. `pip install -r requirements.txt`

6. `python main.py`

### Run using Docker

4. `docker build -t karaoke-sign-in .`

5. `docker run --rm -it -v "${PWD}/output:/usr/src/app/output" -v "${PWD}/config:/usr/src/app/config" karaoke-sign-in`

Once the script has finished running, the output will be stored in a tab-separated file `output/songs.tsv`. Read it with a text-editor or spreadsheet software.

