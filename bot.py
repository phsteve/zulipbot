import zulip
import re
import sys
import nltk


import text_gen

SUBSCRIPTIONS = set(['455 Broadway', 'Broadcasts', 'Iron Blogger', 'OSS at HS',
                 'Off-Topic', 'Sublime', 'Twisted', 'Unix commands', 'Victory',
                 'announce', 'arduino', 'bittorrent', 'code review', 'commits',
                 'elixir', 'food', 'friday-jobs-prep', 'git', 'html5', 'javascript',
                 'jobs', 'machine learning', 'math', 'nand2tetris', 'ocaml', 'pairing',
                 'poker', 'programming', 'python', 'social', 'test-bot', 'test-bot2',
                 'zulip', '1 Liberty Plaza', '137 Varick St', '455', '455\\', '6502',
                 'Broadway', 'C', 'ClojureScript Compiler', 'Hackathons!', 'Hackettes',
                 'ICFP 2013 Contest', 'Linux kernel', 'Matlab', 'PIG', 'SICP slowly',
                 'SICP study group', 'SICP-summer2013', 'San Francisco', 'Stripe CTF',
                 'VIM', 'WHAT', 'algorithms', 'alumni', 'audio programming', 'checkins',
                 'clojure', 'common-lisp', 'compilers', 'coq tutorial', 'couchsurfing',
                 'coursera PL course', 'coursera pl clourse', 'crossfit', 'data', 'dijkstra',
                 'emacs-users', 'erlang', 'functional data structures', 'golang', 'graph databases',
                 'hacker-music', 'haklsdjfas', 'haskell', 'help', 'housing', 'interactive fiction',
                 'julia', 'julia webstack doc-a-thon', 'linux', 'lockpicking', 'lovelace',
                 'lunch circle', 'meta', 'miniKanren', 'mongodb', 'music', 'music software',
                 'network', 'newish hackers', 'node', 'objective-c', 'off the wall',
                 'participation', 'princeton algos coursera', 'projects', 'pushups etc',
                 'racket', 'risk', 'ruby', 'russell-checkin', 'rust', 'sandbox', 'scala',
                 'spot-the-fail', 'stanford algos coursera', 'systems papers reading group',
                 'tapl', 'tech policy', 'test-stream', 'tictax', 'ttrpg', 'videogames',
                 'weekend-retreat', 'work', 'working on'])
SUBSCRIPTIONS_DICT = dict((item.lower(), item) for item in SUBSCRIPTIONS)

def extract_messages(response):
    # import pdb
    # pdb.set_trace()
    return [msg['content'] for msg in response['messages'] if msg['content'] if msg['type'] != 'private' and msg['display_recipient'] != 'test-bot']

def stringify(lst):
    return ' '.join(lst)

def strip_html(lst):
    """Takes a list of strings possibly with HTML tags,
    returns a concatenated string with HTML stripped"""
    #strip punctuation
    #re-render escaped symbols
    #preserve <code> blocks
    stripped = re.sub('<code>.*</code>', ' ', ' '.join(lst), flags=re.DOTALL)
    stripped = re.sub('<div class="codehilite">.*</div>', ' ', stripped, flags=re.DOTALL)
    stripped = re.sub('<a.*</a>', ' ', stripped, flags=re.DOTALL)
    stripped = re.sub('<[^<]+?>', ' ', stripped)
    return stripped

def make_tokens(s):
    sentences = nltk.sent_tokenize(s)
    res = [word for sent in sentences for word in nltk.word_tokenize(sent)]
    return res

def get_messages(anchor, num_before, streams, num_after=0):
    messages = []
    for stream in streams:
        query_response = client.do_api_query({'anchor':anchor, 'num_before': num_before, 'num_after': num_after, 'narrow': [['stream', stream]]},
                                          'https://zulip.com/api/v1/messages',
                                          method='GET'
                                        )
        messages += extract_messages(query_response)
    return messages

def respond(message): 
    if message['type'] == 'private' and message['sender_email'] != 'katzbot-bot@students.hackerschool.com':

        streams = set(SUBSCRIPTIONS_DICT.get(word.strip().lower(), word) for word in message['content'].split(','))
        msg_id = message['id']
        sender = message['sender_email']
        fails = streams - SUBSCRIPTIONS
        wins = SUBSCRIPTIONS & streams
        if fails:
            client.send_message({
                                'type': 'private',
                                'to': sender,
                                'content': 'Sorry, the following streams were not recognized: %s' %(', '.join(fails))
                                })
        messages = get_messages(msg_id, 400, wins)

        if wins:
            client.send_message({
                                'type': 'private',
                                'to': sender,
                                'subject': 'This is what you sound like',
                                'content': text_gen.gen(make_tokens(strip_html(messages)))
                                })

def echo(message):
    print message
    anchor = message['id']
    print client.do_api_query({'anchor':anchor, 'num_before': 0, 'num_after': 0},
                                          'https://zulip.com/api/v1/messages',
                                          method='GET'
                                        )
    # if message['type'] == 'private' and message['sender_email'] != 'katzbot-bot@students.hackerschool.com':
    #     print message

if __name__ == '__main__':
    client = zulip.Client()
    client.call_on_each_message(respond)
    # print get_messages(, 10, ['test-bot'])