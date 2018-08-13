# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient

import os
import threading
import time

# Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# SlackClient for your bot to use for Web API requests. It's Nemesys bot!
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)

# Make a dict with all team's users
members = CLIENT.api_call("users.list")
members = members["members"]
dict_members = {}
for member in members:
	dict_members[member['id']] = member['profile']['real_name']

# Make a dict with all team's channels. For a while, it's getting only public channels
open_channels = CLIENT.api_call("channels.list", exclude_members=True, exclude_archived=True)
open_channels = open_channels["channels"]
dict_channels = {}

for open_channel in open_channels:
	dict_channels[open_channel['id']] = open_channel["name_normalized"]

'''
Check for members that didn't react to oficial communicate
Wait for 24 hours, catch all usernames that has been reacted to a message. Send it as a bot message

ps:This method is run in a thread!  

Params:
	- channel -> Channel's id
	- ts -> message's timestamp 

Return: NONE
'''
def check_reactions(channel, ts):
	time.sleep(20)
	# Get all reactions from a message
	reactions = CLIENT.api_call("reactions.get", channel=channel,timestamp=ts)
	result = reactions["message"]["reactions"]
	aux_dict = dict_members

	# Members that has been reacted
	for reaction in result:
		for user in reaction["users"]:
			del aux_dict[user]

	message = "Não deixaram a reaction:\n"

	# Concat message with @user1, @user2, ..., @usern
	for user_id, user_name in aux_dict.iteritems():
		message += "	<@" + user_id + ">;\n"
	
	# Make a reply
	CLIENT.api_call("chat.postMessage", channel=channel, text=message, thread_ts=ts)

'''
Message event handler.
Subscribed Workspace Events: message.channels, message.im, message.mpim, message.groups
'''
@slack_events_adapter.on("message")
def handle_message(event_data):
	message = event_data["event"]
	channel = message["channel"]
	ts = message["ts"]

	# Pick messages that contains "@channel" in a specific channel (e.g. 'abobrinha') and throws timer on message with given timestamp
	if channel == str(dict_channels.keys()[dict_channels.values().index('abobrinha')]) and "<!channel>" in message.get('text'):
		t = threading.Thread(target=check_reactions,args=(channel,ts))
		t.start()

		
	# If the incoming message contains "hi", then respond with a "Hello" message
	# ISSUE: bot response working only inside app chat (in dm isn't works)
	elif message.get("subtype") is None and "hi" in message.get('text'):
		message = "Hello <@%s>! :tada:" % message["user"]
		CLIENT.api_call("chat.postMessage", channel=channel, text=message, thread_ts=ts)

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3001
slack_events_adapter.start(port=3001)
