<<<<<<< HEAD
from json import dumps
from flask import Flask, request
from datetime import datetime
=======
"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
>>>>>>> master
import hashlib
import jwt
import re
import copy
import time

<<<<<<< HEAD

APP = Flask(__name__)

#GLOBAL VARIABLES
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
SECRET = "daenerys"
data = {
    'users' : [], # should have a dictionary for each user
    'channels' : [] #shoudl have a dictionary for each channel

    # e.g. {email, password, name_first, name_last, u_id, permission_id, handle, token, profile, is_logged}

    #e.g {'channel_id' : 1234 , 'name' : channelname, 'owners' : [u_id1, u_id2...], members : [u_id, u_id2....], 'ispublic': True }
}

#check if email is valid
def valid_email(email):
    if(re.search(regex,email)):
        return True
    else:
        return False

#abstraction for returning global data
def get_data():
    global data
    return data

#abstraction for returning json string
def send_sucess(data):
    return dumps(data)

def send_error(message):
    return dumps({
        '_error': message
    })

#encodes token given string and SECRET
def generate_token(string):
    global SECRET
    return jwt.encode({'string' : string, 'time' : time.time()}, SECRET, algorithm='HS256').decode('utf-8')

#decodes token given string and SECRET
def decode_token(token):
    global SECRET
    decoded = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
    return decoded['string']

#generates hash for string
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_logged_in(token):

    u_id = decode_token(token)
    user = user_dict(u_id)
    if user == None:
        return False
    if token in user['tokens']:
        return True
    else:
        return False

def user_dict(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    return None

def channel_dict(channel_id):
    data = get_data()
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None

=======
from backend.functions.data import *
from backend.functions.channel_functions import *

APP = Flask(__name__)

>>>>>>> master
#########################   AUTH FUNCTIONS  ###########################

#REGISTER
@APP.route('/auth/register', methods = ['POST'])
def create():

    email = request.form.get('email') #get email
    password = request.form.get('password') # get password
    name_first = request.form.get('name_first') #get first name
    name_last = request.form.get('name_last') #get last name


    data = get_data()
    #check if email already exist
    if valid_email(email) == True:
        for user in data['users']:
            if email == user['email']:
                return send_error('already used email')
    else:
        return send_error('invalid email')

    if len(password) < 6: #rules for length of pasword
        return send_error('password too short')


    if len(name_first) < 1 or len(name_first) > 50 or len(name_last) < 1 or len(name_last) > 50: #rules for length of name (first and last)
        return send_error('names too long/short')

    handle = ''.join((name_last, name_last))
    for user in data['users']:
        if handle == user['handle']:
            handle += str(1 + len(data['users']))

    hashedPassword = hash_password(password)
    u_id = 101 + len(data['users'])
    token = generate_token(u_id)

    if len(data['users']) == 0:
        permission_id = 1
    else:
        permission_id = 3


    #append all relevant information to users dictionary
    data['users'].append({
        'email' : email,
        'password' : hashedPassword,
        'name_first' : name_first,
        'name_last' : name_last,
        'u_id': u_id,
        'permission_id' : permission_id,
        'handle' : handle,
        'tokens'  : [],
        'profile' : None
    })
<<<<<<< HEAD
    return send_sucess({
=======
    return send_success({
>>>>>>> master
        'u_id': u_id,
        'token' : token
    })

#LOGIN
@APP.route('/auth/login', methods = ['PUT'])
def connect():

    email = request.form.get('email') #get email
    password = request.form.get('password') #get password

    data = get_data()
    if valid_email(email) == False: #check valid email
        return send_error('invalid email')

    #check if email exists and if so check if password matches
    for user in data['users']:
        if user['email'] == email and user['password'] == hash_password(password):
            u_id = user['u_id']
            token = generate_token(u_id)
            user['tokens'].append(token)
<<<<<<< HEAD
            return send_sucess({
=======
            return send_success({
>>>>>>> master
                'u_id' : u_id,
                'token': token
            })

    return send_error('email does not exist or password is incorrect')


#INVITE
@APP.route('/channel/invite', methods = ['POST'])
def invite():

    token = request.form.get('token') #get token
    channel_id = request.form.get('channel_id') #get channel_id
    u_id = request.form.get('u_id') #get u_id

    inv_u_id = decode_token(token)

    if u_id == inv_u_id:
        return send_error('cannot invite self')

    channel = channel_dict(channel_id)
    if channel == None:
        return send_error('channel id does not exist')

    for user in channel['members']:
        if u_id == user:
            return send_error('user already part of channel')
    channel['members'].append(u_id)
<<<<<<< HEAD
    return send_sucess({})
=======
    return send_success({})
>>>>>>> master



#JOIN
@APP.route('/channel/join', methods = ['POST'])
def join():

    token = request.form.get('token') #get token
    channel_id = request.form.get('channel_id') #get channel_id

    u_id = decode_token(token)

    channel = channel_dict(channel_id)
    user = user_dict(u_id)
    if user == None or channel == None:
        return send_error('channel id/ user id does not exist')

    if user['permission_id'] != 3:
        channel['members'].append(u_id)
    elif user['permission_id'] == 3 and channel['is_public'] == True:
        channel['members'].append(u_id)
    else:
        return send_error('user does not have rightts')

<<<<<<< HEAD
    return send_sucess({})
=======
    return send_success({})
>>>>>>> master

@APP.route('/auth/logout', methods = ['PUT'])
def logout():

    token = request.form.get('token') #get token
    u_id = decode_token(token)
    user = user_dict(u_id)
    user['tokens'].remove(token)

<<<<<<< HEAD
    return send_sucess({})
=======
    return send_success({})
>>>>>>> master

#########################   CHANNEL FUNCTIONS  ###########################

@APP.route('/channels/create', methods = ['POST'])
<<<<<<< HEAD
def channels_create():
=======
def channel_create():
>>>>>>> master
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    if not is_logged_in(token):
<<<<<<< HEAD
        send_error("User not logged in")
    if len(name) > 20:
        return send_error("Name of channel is longer than 20 characters.")
    data = get_data()
    owner_id = decode_token(token)
    print(owner_id)
    get_user_name(owner_id)
    print(f"owner's name is: {get_user_name(owner_id)}")

    # Give the channel an ID which corresponds to the number created e.g. 1st channel is ID1 ...
    new_channel_id = len(data['channels']) + 1
    # Create a dictionary with all the relevant info and append to data
    dict = {
        'channel_id': new_channel_id,
        'name': name,
        'owners': [owner_id],
        'members': [],
        'is_public': is_public,
        'messages': []
    }
    data['channels'].append(dict)
    print(data['channels'])
    return send_sucess( {
        'channel_id': new_channel_id
    })


def get_user_name(u_id):
    data = get_data()
    for user in data['users']:
        if u_id == user['u_id']:
            return {user['name_first'], user['name_last']}
    return None


@APP.route('/channel/messages', methods = ['GET'])
#input: token, channelid, start
#user must be a member of the channel
def showmessages():
    data = get_data()
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id')) #must be valid channel
    start = int(request.args.get('start')) #cannot be >= no. of messages in channel
    end = start + 50
    messages = []
    #Checking channel_id is valid
    newchannel = {}
    for channel in data['channels']:
        if(channel['channel_id'] == channel_id):
            newchannel.update(channel)
    if not newchannel:
        return send_error('Invalid channel_id')
    #Checking length of messages
    if(start > len(newchannel['messages'])):
        return send_error('Start index is > then amount of messages')
    u_id = decode_token(token)
    #Checking if user is authorised in correct channel
    if(u_id not in newchannel['members'] and u_id not in newchannel['owners']):
        return send_error('user is not in correct channel')
    index = start
    for i in range(index,len(newchannel['messages']) + 1):
        messages.append(newchannel['messages'][i])
    if end > len(newchannel['messages']):
        end = -1
    return dumps({'messages': messages, 'start': start, 'end': end,}, indent=4, sort_keys=True, default=str)

    #given start return end which is start + 50 or -1 if theres no more messages
            
#########################   MESSAGE FUNCTIONS  ###########################
#check valid channel aswell
@APP.route('/message/send', methods = ['POST'])
#input: token,channelid,message
def send():
    #Initialising all data from input
    data = get_data()
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    #The message_id will be 1 + length of messages in a specific channel
    newchannel = {}
    for channel in data['channels']:
        if(channel['channel_id'] == channel_id):
            newchannel.update(channel)
        else:
            print(channel_id)
            print(channel['channel_id'])
    message_id = 1 + len(newchannel['messages'])
    if(len(message) > 1000):
        return send_error('message is more than 1000 characters')
    #Obtaining u_id from token
    u_id = decode_token(token)
    #if user hasn't joined the channel they are sending a message in):
    if(u_id not in newchannel['members'] and u_id not in newchannel['owners']):
        return send_error('user is not in correct channel')
    message_dict = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': datetime.now(),
        'is_unread': True,
        'reacts': [],
        'is_pinned': False,
    }
    for channel in data['channels']:
        if(channel['channel_id'] == channel_id):
            channel['messages'].insert(0, message_dict)
            print(newchannel['messages'])
    return send_sucess({'message_id': message_id})
    
if __name__ == "__main__":
    APP.run(debug=True)
=======
        return send_error(f"User: {decode_token(token)} not logged in")
    return send_success(channels_create(token, name, is_public))


@APP.route('/channels/listall', methods = ['GET'])
def listall():
    token = request.args.get('token')
    if not is_logged_in(token):
        return send_error(f"User: {decode_token(token)} is not logged in")
    return send_success(channels_listall(token))


@APP.route('/channels/list', methods = ['GET'])
def list():
    token = request.args.get('token')
    if not is_logged_in(token):
        return send_error(f"User: {decode_token(token)} is not logged in")
    return send_success(channels_list(token))

@APP.route('/channel/leave', methods = ['POST'])
def leave():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    if not is_logged_in(token):
        return send_error(f"User: {decode_token(token)} is not logged in")
    if not is_joined(token, channel_id):
        return send_error(f"User: {decode_token(token)} has not joined channel: {channel_id} yet")
    if not is_valid_channel(channel_id):
        return send_error(f"Channel ID: {channel_id} is invalid")
    return send_success(channel_leave(token, channel_id))

@APP.route('/channel/addowner', methods = ['POST'])
def addowner():
    token = request.form.get('token')   # person doing promoting
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))     # person being promoted
    if not is_logged_in(token):
        return send_error(f"User: {decode_token(token)} is not logged in")
    #if not is_logged_in(generate_token(u_id)):
    #    return send_error(f"User: {u_id} is not logged in")
    if not is_valid_channel(channel_id):
        return send_error(f"Channel ID: {channel_id} is invalid")
    if is_owner(u_id, channel_id):
        return send_error(f"User: {u_id} is already an owner")
    if not is_owner(decode_token(token), channel_id):
        return send_error(f"User: {decode_token(token)} does not have privileges to promote others")

    return send_success(channel_addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods = ['POST'])
def removeowner():
    token = request.form.get('token')   # person doing demoting
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))     # person being demoted
    if not is_logged_in(token):
        return send_error(f"User: {decode_token(token)} is not logged in")
    #if not is_logged_in(generate_token(u_id)):
    #    return send_error(f"User: {u_id} is not logged in")
    if not is_valid_channel(channel_id):
        return send_error(f"Channel ID: {channel_id} is invalid")
    if not is_owner(u_id, channel_id):
        return send_error(f"User: {u_id} is not an owner")
    if not is_owner(decode_token(token), channel_id):
        return send_error(f"User: {decode_token(token)} does not have privileges to demote others")

    return send_success(channel_removeowner(token, channel_id, u_id))


if __name__ == "__main__":
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
>>>>>>> master
