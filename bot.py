import zulip
import re
import sys

import bigram_gen

# client.add_subscriptions([{'name': 'test-bot'}])
# client.register(event_types=['message'])
# client.verbose=True

def extract_messages(response):
    return [msg['content'] for msg in response['messages'] if msg['content'] if msg['type'] != 'private' and msg['display_recipient'] != 'test-bot']

def strip_html_and_tokenize(lst):
    """Takes a list of strings possibly with HTML tags,
    returns a list of word tokens with HTML stripped"""
    return re.sub('<[^<]+?>', ' ', ' '.join(lst)).replace('\n', ' ').split(' ')

def get_messages(anchor, num_before, sender, num_after=0):
    query_response = client.do_api_query({'anchor':anchor, 'num_before': num_before, 'num_after': num_after, 'narrow': [['sender', sender]]},
                                          'https://zulip.com/api/v1/messages',
                                          method='GET'
                                        )
    messages = extract_messages(query_response)
    first = query_response['messages'][0]['id']
    second_response = client.do_api_query({'anchor':first, 'num_before': num_before, 'num_after': num_after, 'narrow': [['sender', sender]]},
                                          'https://zulip.com/api/v1/messages',
                                          method='GET'
                                        )
    second_messages = extract_messages(second_response)
    return messages + second_messages

def respond(message):
    
    if message['type'] == 'private' and message['sender_email'] != 'katzbot-bot@students.hackerschool.com':
        msg_id = message['id']
        sender = message['sender_email']
        messages = get_messages(msg_id, 1000, sender)

        print '%d from %s' %(len(messages), sender)
        print messages

        # client.send_message({
        #                     'type': 'private',
        #                     'to': sender,
        #                     'subject': 'This is what you sound like',
        #                     'content': bigram_gen.gen(strip_html_and_tokenize(messages))
        #                     })

if __name__ == '__main__':
    client = zulip.Client()
    client.call_on_each_message(respond)