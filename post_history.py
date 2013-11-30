import zulip

#katzbot needs to subscribe to all streams



#user PMs katzbot

#katzbot looks up PM-er's previous (say) 500 posts
#   right now it just finds posts in streams that katzbot is subscribed to (i.e. just test-bot), not the ones it sent
#   look at get-old-messages request
#   how do I 

#generate hilarious bigram text from text of posts

# response = requests.get('https://zulip.com/api/v1/messages',
#                         auth=('katzbot-bot@students.hackerschool.com', 'u1EOyeyNqVaPrfuuN0qqeVVhrsT6SFmi'),
#                         params={'anchor':'13374416', 'num_before':'100', 'num_after':'0'})
# # import pdb
# # pdb.set_trace()
# resp_json = json.loads(response.text)

client = zulip.Client()
resp = client.do_api_query({'anchor': '13377010',
                            'num_before': '100',
                            'num_after': '0',
                            # 'narrow': [['sender', 'katz.stephenj@gmail.com']]
                            },
                           'https://zulip.com/api/v1/messages',
                           method='GET')


msgs = [msg['content'] for msg in resp['messages']]
#  
