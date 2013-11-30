Zulip bots
---------------

This code requires Zulip's Python API bindings, available [here](https://zulip.com/api/).

Code for two Zulip bots.

printspms.py

This was my first, simple "Hello World"-esque bot I wrote. When a user sends it a PM, it will post the text of the PM to a stream and disclose the sender's name. Violates the user's privacy by design. Currently trying to market it to the NSA.

markov.py

This bot is not yet finished. It's intended to operate similarly to the what-would-i-say webapp that was making the rounds on social media in early November 2013. A user sends the bot a PM, the bot looks up the user's post history, then uses the history to generate a random sentence that sounds like the user wrote it. Initially I used NLTK's trigram sentence generator, but the results were not sufficiently hilarious, so I modified the NLTK code to use bigrams instead.
Again, this is not complete, and I'm still actively working on it. My API requests don't get the user's complete post history yet.