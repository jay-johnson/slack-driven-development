## Slack Driven Development

An example for posting: exceptions, tracking environment errors, and sending targeted debugging messages to a Slack channel to help decrease time spent finding + fixing bugs.

I built this because I was tired of tail-ing and grep-ing through logs. Now I just wait for exceptions and errors to be published into a **debugging** Slack channel so I can quickly view: what environment had the error, the associated message, and the source code line number.

### Setup

This repository only works with Python 2.

1. Install the official Slack Python API 

    Please refer to the official [Slack repository](https://github.com/slackhq/python-slackclient) for more information

    ```
    sudo pip install slackclient
    ```

### Getting Started

There are also screenshots below this section to help get started.

1. Create a Slack channel for debugging messages

    This demo uses a channel with the name: ```#debugging```

1. Create a named Slack bot if you do not have one already

    This demo uses a bot with the name: ```bugbot```

1. Record the Slack bot's API Token

    This demo uses a bot with an API token: ```xoxb-51351043345-oHKTiT5sXqIAlxwYzQspae54```
    
1. Invite the Slack bot to your debugging channel

    Type this into the debugging channel and hit enter: ```/invite bugbot```

1. Edit the configuration for your needs

    The example file ```slack_driven_development.py``` uses a configuration [dictionary object](https://github.com/jay-johnson/slack-driven-development/blob/78ced381ce1a1594e735943a8a9ab145425fe7d1/slack_driven_development.py#L5-L11) where you can assign these keys based off your needs:

    | Key Name    | Purpose and Where to find the Value                        |
    | ----------- | ---------------------------------------------------------- |
    | BotName     | Name of the Slack bot that will post messages              |
    | ChannelName | Name of the channel where messages are posted              |
    | NotifyUser  | Name of the Slack user that gets notified for messages     |
    | Token       | Slack API Token for the bot                                |
    | EnvName     | A logical name for showing which environment had the error |

1. Test the bot works

    The included [slack_driven_development.py](https://github.com/jay-johnson/slack-driven-development/blob/master/slack_driven_development.py) file will throw an exception that will report the exception into the channel using the bot based off the simple dictionary configuration in the file.

    ```
    $ ./slack_driven_development.py 
    Testing an Exception that shows up in Slack
    Sending an error message to Slack for Exception(name 'testing_how_this_looks_from_slack' is not defined)
    Done
    $
    ```

1. Confirm the debugging message shows up in Slack channel

    ![Confirm the debugging messages show up in Slack](./images/07SlackDrivenDevelopmentExample.png)

### Screenshots for Getting Started

Here are the screenshots (as of 06-15-2016) for getting this demo integrated with your Slack channel and bot:

1. Create a new Slack App Integration

![Step 1 - Create a new Slack App Integration](./images/01SlackAddANewIntegration.png)


1. Build a new Integration

![Step 2 - Build a new Integration](./images/02SlackBuild.png)


1. Make a Custom Integration

![Step 3 - Make a Custom Integration](./images/03SlackMakeCustomIntegration.png)


1. Create a new Bot

![Step 4 - Create a new Bot](./images/04SlackBotCreateNewBot.png)


1. Name and Add Bot

![Step 5 - Name and Add Bot](./images/05SlackNameAndAddBot.png)


1. Record the Bot API Token in the Dictionary Configuration

![Step 6 - Record the Bot API Token in the Dictionary Configuration](./images/06SlackRecordBotAPIToken.png)


1. Run the Slack Driven Development Demo

![Step 7 - Run the Slack Driven Development Demo](./images/07SlackDrivenDevelopmentExample.png)


### License

MIT - have fun!


