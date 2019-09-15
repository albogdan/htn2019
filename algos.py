import os
import json
import importlib
import profanity_check


def message_counter():
    """
    Goes thru the JSON of the messages and counts the number of times you have messaged that person
    """
    rootdir_messages = './application/data/messages/inbox'
    temp_file_dir = './application/visualizer/temp_data.json'
    temp_file_dir_profanity = './application/visualizer/temp_data_profanity.json'
    temp_file_dir_abbreviation = './application/visualizer/temp_data_abbreviation.json'

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
    wrapper = dict() 
    wrapper['max_total_msgs'] = 0
    conversation_data = list()
    for subdir, dirs, files in os.walk(rootdir_messages):
        if ('message_1.json' not in files):
            continue
        path = subdir + '/message_1.json'
        with open(path) as json_file:
            # Load the conversation (messages or group chat)
            conversation = json.load(json_file)

            # Create a dict for this message thread
            message_thread = dict()
            conv_name = conversation['title']
            message_thread['conv_name'] = conv_name

            # Add the number of participants
            message_thread['participant_count'] = len(
                conversation['participants'])
            message_thread['participants'] = dict()
            for participant in conversation['participants']:
                name = participant['name']
                message_thread['participants'][name] = {'sent_msg_count': 0, 'profanity_count': 0, 'abbreviation_count': 0}
                #print(name)

            # Create a dict for the statistics
            stats = dict()
            stats['total_msg_count'] = len(conversation['messages'])
            stats['total_profanity_count'] = 0
            stats['total_abbreviation_count'] = 0
            if int(stats['total_msg_count']) > int(wrapper['max_total_msgs']):
                wrapper['max_total_msgs'] = stats['total_msg_count']

						# Analyze messages in conversation
            for msg in conversation['messages']:
                sender = msg['sender_name']

				# Get sent message count of each user
                if (sender not in message_thread['participants']):
                    message_thread['participants'][sender] = {'sent_msg_count': 0, 'profanity_count': 0, 'abbreviation_count': 0}

                message_thread['participants'][sender]['sent_msg_count'] += 1
                if ('content' in msg.keys()):
                    message_thread['participants'][sender]['profanity_count'] += int(profanity_check.predict([msg['content']])) # Profanity count
                    stats['total_profanity_count'] += int(profanity_check.predict([msg['content']]))
                    message_thread['participants'][sender]['abbreviation_count'] += int(countAbbreviations(str([msg['content']])))
                    stats['total_abbreviation_count'] += int(countAbbreviations(str([msg['content']])))

            message_thread['statistics'] = stats
            
            conversation_data.append(message_thread)

            # print(conversation_data)
    
    # Sort conversation_data by total_msg_count
    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_msg_count'], reverse = True)
    
    wrapper['conversation_data'] = conversation_data

    with open(temp_file_dir, 'w') as temp_file:
        temp_file.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_profanity_count'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_profanity, 'w') as temp_file:
        temp_file.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_abbreviation_count'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_abbreviation, 'w') as temp_file:
        temp_file.write(json.dumps(wrapper, indent=4))

    return conversation_data

def countAbbreviations(str):
    numAbbreviations = 0

    str.lower(); 
    numAbbreviations += str.count('lmao'); 
    numAbbreviations += str.count('lol');
    numAbbreviations += str.count('brb');
    numAbbreviations += str.count('gtg');
    numAbbreviations += str.count('smh');
    numAbbreviations += str.count('lmfao');
    numAbbreviations += str.count('wtf');
    numAbbreviations += str.count('k');
    numAbbreviations += str.count('ttyl');
    numAbbreviations += str.count('cya');
    numAbbreviations += str.count('idk');
    numAbbreviations += str.count('omw');
    numAbbreviations += str.count('btw');
    numAbbreviations += str.count('afaik');
    numAbbreviations += str.count('iirc');
    numAbbreviations += str.count('tba');
    numAbbreviations += str.count('thx');
    numAbbreviations += str.count('omg');
    numAbbreviations += str.count('omfg');
    numAbbreviations += str.count('rofl');
    numAbbreviations += str.count('btw');
    numAbbreviations += str.count('faq');
    numAbbreviations += str.count('ftw');
    numAbbreviations += str.count('idc');
    numAbbreviations += str.count('imo');
    numAbbreviations += str.count('imho');
    numAbbreviations += str.count('wth');
    numAbbreviations += str.count('icymi');
    numAbbreviations += str.count('tyvm');
    numAbbreviations += str.count('ily');
    numAbbreviations += str.count('rsvp');
    numAbbreviations += str.count('ofc');
    numAbbreviations += str.count('lmk');
    numAbbreviations += str.count('tbh');
    numAbbreviations += str.count('hmu');
    numAbbreviations += str.count('jk');

    return numAbbreviations

if __name__ == '__main__':
    conv_data = message_counter()
    #print(conv_data)



# Within each group, each participant needs a msg count
# Within individual msgs

"""
1. Graph of how much each person talks on each chat
    a) Data structure of personal msgs per chat
    For individual chat:
        Iterate through all the people they talk to and see how many msgs were sent and received
        Have option to include where it just counts the number of msgs
    For group chats:

2. For each chat, bar(or w/e) graph of how much each person talked on it
    a) Data structure of each chat w/ participants and number of msgs per participant
"""
