import zulip
import pdb
import sys

client = zulip.Client()
# client.add_subscriptions([{'name': 'test-bot'}])
# client.register(event_types=['message'])
# client.verbose=True

def respond(event):
    if event['type'] == 'message' and event['message']['sender_email'] != 'katzbot-bot@students.hackerschool.com': #if message type = received
        sender = event['message']['sender_full_name']
        content = event['message']['content']
        client.send_message({
                            "type": "stream",
                            "to": 'test-bot',
                            "subject": "I'm violating your privacy!",
                            "content": sender + " just sent me this super-secret PM: " + content
                            })
        # sys.stdout.write(str(event) + '\n')

def analyze(event):
    if 'message' in event:
        if 'content' in event['message']:
            print 'got: ' + event['message']['content']
            if event['message']['content'] == 'katzbot stop listening':
                print 'got some data: ' + repr(data)

client.call_on_each_event(respond)