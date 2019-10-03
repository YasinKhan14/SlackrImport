
import pytest

# Provide a list of all channels (and their associated details) that the authorised user is part of
def channels_list(token):
    pass # return {channels} # list of dictionary with {id: ' ', name: ' '}


######################## GLOBAL VARIABLES SETUP ######################

userDict1 = auth_register("person1@gmail.com", "password", "person", "one")
token = userDict1['token']

##########################    END SETUP   ########################


# Empty list of channels if none have been created yet
def test_channels_list_1():
    assert(channels_list(token) == [{}])

# Empty list of channels if some have been created but not joined yet
def test_channels_list_2():
    channel_id1 = channels_create(token, "Name", True)
    assert(channels_list(token) == [{}])

def test_channels_list_3():
    channel_id1 = channels_create(token, "Name1", True)
    channel_id2 = channels_create(token, "Name2", True)
    assert(channels_list(token) == [{}])


# Testing single list of channels if one has been created and joined
def test_channel_list_4():
    channel_id1 = channels_create(token, "Name", True)
    channel_join(token, channel_id1)
    assert(channels_list(token) == [{'id': channel_id1, 'name': "Name"}])

# Expecting single list of channels if multiple have been created, but joined only one
def test_channel_list_5():
    channel_id1 = channels_create(token, "Name1", True)
    channel_id2 = channels_create(token, "Name2", True)
    channel_id3 = channels_create(token, "Name3", True)
    channel_join(token, channel_id1)
    assert(channels_list(token) == [{'id': channel_id1, 'name': "Name1"}])

# Expecting only a few list of channels to be returned if not all have been joined
def test_channel_list_6():
    channel_id1 = channels_create(token, "Name1", True)
    channel_id2 = channels_create(token, "Name2", True)
    channel_id3 = channels_create(token, "Name3", True)
    channel_join(token, channel_id1)
    channel_join(token, channel_id2)
    assert(channels_list(token) == [{'id': channel_id1, 'name': "Name1"},
                                     'id': channel_id2, 'name': "Name2"}])

# Expecting all channels to be returned if all have been created and joined
def test_channel_list_7():
    channel_id1 = channels_create(token, "Name1", True)
    channel_id2 = channels_create(token, "Name2", True)
    channel_id3 = channels_create(token, "Name3", True)
    channel_join(token, channel_id1)
    channel_join(token, channel_id2)
    channel_join(token, channel_id3)
    assert(channels_list(token) == [{'id': channel_id1, 'name': "Name1"},
                                     'id': channel_id2, 'name': "Name2"},
                                     'id': channel_id3, 'name': "Name3"}])
