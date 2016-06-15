#!/usr/bin/python

from slack_messenger import SlackMessenger

slack_config = {
                "BotName"     : "bugbot",
                "ChannelName" : "debugging",
                "NotifyUser"  : "jay",
                "Token"       : "xoxb-51351043345-RQED5EaegVpatE6f1lApeHqR",
                "EnvName"     : "LocalDev"
             }

slack_msg = SlackMessenger(slack_config)

try:
    print "Testing an Exception that shows up in Slack"
    testing_how_this_looks_from_slack
except Exception,k:
    print "Sending an error message to Slack for the expected Exception(" + str(k) + ")"
    slack_msg.handle_send_slack_internal_ex(k)
# end of try/ex

print "Done"

