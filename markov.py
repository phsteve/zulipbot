import zulip
import sys

import bigram_gen

client = zulip.Client()
# client.add_subscriptions([{'name': 'test-bot'}])
# client.register(event_types=['message'])
# client.verbose=True

def get_messages(anchor, num_before, sender):
    query_response = client.do_api_query({'anchor':anchor, 'num_before': num_before, 'num_after':'0', 'narrow': [['sender', sender]]},
                             'https://zulip.com/api/v1/messages',
                             method='GET',
                             )
    result = [message['content'] for message in query_response['messages'] if message['type'] != 'private' and message['display_recipient'] != 'test-bot']
    return result

def respond(message):
    # print message
    if message['type'] == 'private' and message['sender_email'] != 'katzbot-bot@students.hackerschool.com':
        msg_id = message['id']
        sender = message['sender_email']
        messages = get_messages(msg_id, 100, sender)
        while len(messages) < 100:
            print len(messages)
            msg_id = msg_id - 100
            messages.extend(get_messages(msg_id, 100, sender))
            print 'looking for messages from %d to %d'%(msg_id, msg_id-100)
        client.send_message({
                            'type': 'private',
                            'to': sender,
                            'subject': 'This is what you sound like',
                            'content': bigram_gen.gen(messages)
                            })

client.call_on_each_message(respond)