import os
from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from datetime import datetime

from config import DevelopmentConfig, ProductionConfig, BASE_DIR
# Import form to upload file
from application.home.forms import UploadForm
# Import files for logging in

from werkzeug.utils import secure_filename

#import message_parser
#from message_parser import message_counter, determinePolarity, countAbbreviations
# Import the homepage Blueprint from home/__init__.py
from application.home import home
import uuid

from flask import session
import zipfile
import importlib
import profanity_check
import json
from textblob import TextBlob

UPLOAD_FOLDER_PATH = os.path.join(BASE_DIR, 'uploads')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@home.route('/', methods=['GET', 'POST'])
@home.route('/index', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if(form.validate_on_submit()):
        #filename = secure_filename(form.fileName)
        filename = form.fileName
        print("FILE:", filename.__dict__)
        # print("NAME", filename.data.FileStorage)
        file_path = os.path.join(UPLOAD_FOLDER_PATH, str(uuid.uuid1()))
        zip_path = os.path.join(UPLOAD_FOLDER_PATH, 'zipfile.zip')
        filename.data.save(zip_path)
        session['data_file'] = file_path
        os.mkdir(file_path)
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        
        zip_ref.extractall(file_path)
        zip_ref.close()
        message_counter()
        return redirect('visualizer')
    return render_template('home/index.html', form=form)

# @home.route('uploadFile', methods = ['GET', 'POST'])
# def file_upload():
#     print("file submitted")
# #     return render_template('home/index.html')
#     if(request.method == 'POST'):
#         # check if the post request has the file part
#         print("form", request.form.__dict__)

#         if('file' not in request.files):
#             print("No file part")
#             flash('No file part')
#             return redirect(request.url)
#         print(request.__dict__)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if(file.filename == ''):
#             print("No selected file")
#             flash('No selected file')
#             return redirect(request.url)
#         if(file and allowed_file(file.filename)):
#             print("file allowed")
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return render_template('home/index.html')





def message_counter():
    """
    Goes thru the JSON of the messages and counts the number of times you have messaged that person
    """
    # rootdir_messages = './application/data/messages/inbox'
    # temp_file_dir = './application/visualizer/temp_data.json'
    # temp_file_dir_profanity = './application/visualizer/temp_data_profanity.json'
    # temp_file_dir_abbreviation = './application/visualizer/temp_data_abbreviation.json'
    # temp_file_dir_sentiment = './application/visualizer/temp_data_sentiment.json'
    # temp_file_dir_sentiment_negative = './application/visualizer/temp_data_sentiment_negative.json'
    rootdir_messages = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'], 'messages/inbox')
    temp_file_dir = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'], 'temp_data.json')
    temp_file_dir_profanity = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'],'temp_data_profanity.json')
    temp_file_dir_abbreviation = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'],'temp_data_abbreviation.json')
    temp_file_dir_sentiment = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'],'temp_data_sentiment.json')
    temp_file_dir_sentiment_negative = os.path.join(UPLOAD_FOLDER_PATH, session['data_file'],'temp_data_sentiment_negative.json')

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
                message_thread['participants'][name] = {'sent_msg_count': 0, 'profanity_count': 0, 'abbreviation_count': 0, 'sentiment': 0}
                #print(name)

            # Create a dict for the statistics
            stats = dict()
            stats['total_msg_count'] = len(conversation['messages'])
            stats['total_profanity_count'] = 0
            stats['total_abbreviation_count'] = 0
            stats['total_sentiment'] = 0
            if int(stats['total_msg_count']) > int(wrapper['max_total_msgs']):
                wrapper['max_total_msgs'] = stats['total_msg_count']

						# Analyze messages in conversation
            for msg in conversation['messages']:
                sender = msg['sender_name']

				# Get sent message count of each user
                if (sender not in message_thread['participants']):
                    message_thread['participants'][sender] = {'sent_msg_count': 0, 'profanity_count': 0, 'abbreviation_count': 0, 'sentiment': 0}

                message_thread['participants'][sender]['sent_msg_count'] += 1
                if ('content' in msg.keys()):
                    message_thread['participants'][sender]['profanity_count'] += int(profanity_check.predict([msg['content']])) # Profanity count
                    stats['total_profanity_count'] += int(profanity_check.predict([msg['content']]))
                    message_thread['participants'][sender]['abbreviation_count'] += int(countAbbreviations(str([msg['content']])))
                    stats['total_abbreviation_count'] += int(countAbbreviations(str([msg['content']])))
                    message_thread['participants'][sender]['sentiment'] += float(determinePolarity(str([msg['content']])))
                    stats['total_sentiment'] += float(determinePolarity(str([msg['content']])))

            message_thread['statistics'] = stats
            
            conversation_data.append(message_thread)

            # print(conversation_data)
    
    # Sort conversation_data by total_msg_count
    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_msg_count'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir, 'w') as temp_file:
        print("writing temp file in ", temp_file_dir)
        temp_file.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_profanity_count'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_profanity, 'w') as temp_file_profanity:
        temp_file_profanity.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_abbreviation_count'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_abbreviation, 'w') as temp_file_abbreviation:
        temp_file_abbreviation.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_sentiment'], reverse = True)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_sentiment, 'w') as temp_file_sentiment:
        temp_file_sentiment.write(json.dumps(wrapper, indent=4))

    conversation_data.sort(key=lambda message_thread: message_thread['statistics']['total_sentiment'], reverse = False)
    wrapper['conversation_data'] = conversation_data
    with open(temp_file_dir_sentiment_negative, 'w') as temp_file_sentiment_negative:
        temp_file_sentiment_negative.write(json.dumps(wrapper, indent=4))
        

    return conversation_data


def determinePolarity(str):
    polarity = 0.0

    blob = TextBlob(str)
    for sentence in blob.sentences:
        polarity += sentence.sentiment.polarity; 

    return polarity




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



    
@home.route('/visualize')
def visualizer():
    return redirect('visualizer')

@home.route('/survey')
def survey():
    return redirect('survey')

