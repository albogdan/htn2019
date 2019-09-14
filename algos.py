import os
import json

def message_counter():
    """
    Goes thru the JSON of the messages and counts the number of times you have messaged that person
    """
    rootdir_messages = './application/data/messages/inbox'

    '''
    [
        {
            'conv_name': string,
            'participants': { [ { 'name':string } ] },
            'statistics': {
                'message_count': int,
                <more statistics as we need them>
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
    
    return conversation_data


if __name__ == '__main__':
    conv_data = message_counter()
    print(conv_data)