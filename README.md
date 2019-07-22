Zulip bots
---------------

This code requires Zulip's Python API bindings, available [here](https://zulip.com/api/).
# test pr
Code for two Zulip bots.

`printspms.py`

This was my first, simple "Hello World"-esque bot I wrote. When a user sends it a PM, it will post the text of the PM to a stream and disclose the sender's name. Violates the user's privacy by design. Currently trying to market it to the NSA.

`markov.py`

####Usage:

Send a PM to 'katzbot' with the stream names from which you wish to generate text, separated by commas. It will reject nonexistent streams. Example: 
`455 Broadway, Off-Topic`

####Status:

Mostly working! Could use some fine-tuning and more sanitization of text. It's intended to operate similarly to the what-would-i-say webapp that was making the rounds on social media in early November 2013. A user sends the bot a PM, the bot looks up the history of each stream in the PM, then uses the history to generate a random sentence that sounds like the user wrote it. Initially I used NLTK's trigram sentence generator, but the results were not sufficiently hilarious, so I modified the NLTK code to use bigrams instead. Still in active development.
