import os
import json

rootdir_messages = './data/messages/inbox'
user_name = 'Justin Kreiner'

'''
[
	{
		'conv_name': string,
		'participants': { [ { 'name':string } ] },
		'statistics': {
			'message_count': int
		}
	}
]
'''
conversation_data = list()

for subdir, dirs, files in os.walk(rootdir_messages):
	if ('message_1.json' not in files):
		continue

	path = subdir + '/message_1.json'
	with open(path) as json_file:
		conversation = json.load(json_file)

		obj = dict()
		conv_name = conversation['thread_path'].split('/')[1]
		obj['conv_name'] = conv_name
		obj['participants'] = conversation['participants']
		stats = dict()
		stats['message_count'] = len(conversation['messages'])
		obj['statistics'] = stats
		
		conversation_data.append(obj)

print(conversation_data)
	