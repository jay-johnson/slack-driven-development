========================
Slack Driven Development
========================
Date: **2016-06-15**

Since I am always sitting in a slack channel, I wanted to share a tool I use to track exceptions across my cloud and other environments.

This repository_ is an example for posting: exceptions, tracking environment errors, and sending targeted debugging messages to a Slack channel to help decrease time spent finding + fixing bugs.

I built this because I was tired of tail-ing and grep-ing through logs. Now I just wait for exceptions and errors to be published into a **debugging** Slack channel so I can quickly view: what ``environment`` had the error, the ``associated message``, and the ``source code line number``.

.. _repository: https://github.com/jay-johnson/slack-driven-development
.. role:: bash(code)
         :language: bash

Setup
-----

This repository only works with Python 2.

1. Install the official Slack Python API 

   .. note:: Please refer to the official `Slack repository`_ for more information

   ::

        sudo pip install slackclient

.. _Slack repository: https://github.com/slackhq/python-slackclient

Getting Started
---------------

#. Create a Slack channel for debugging messages

   This demo uses a channel with the name: ``#debugging``

#. Create a named Slack bot if you do not have one already

   This demo uses a bot with the name: ``bugbot``

#. Record the Slack bot's API Token

   This demo uses a bot with an API token: ``xoxb-51351043345-oHKTiT5sXqIAlxwYzQspae54``
    
#. Invite the Slack bot to your debugging channel

   Type this into the debugging channel and hit enter: 
    
   ::
        
        /invite bugbot

   .. warning:: If you do not invite the bot into the channel it can be difficult to debug

#. Edit the configuration for your needs

   The example file slack_driven_development.py_ uses a configuration `dictionary object`_ where you can assign these keys based off your needs:

   +-----------------+------------------------------------------------------------+
   | Key Name        | Purpose and Where to find the Value                        |
   +=================+============================================================+
   | **BotName**     | Name of the Slack bot that will post messages              |
   +-----------------+------------------------------------------------------------+
   | **ChannelName** | Name of the channel where messages are posted              |
   +-----------------+------------------------------------------------------------+
   | **NotifyUser**  | Name of the Slack user that gets notified for messages     |
   +-----------------+------------------------------------------------------------+
   | **Token**       | Slack API Token for the bot                                |
   +-----------------+------------------------------------------------------------+
   | **EnvName**     | A logical name for showing which environment had the error |
   +-----------------+------------------------------------------------------------+

#. Test the bot works

   The included slack_driven_development.py_ file will throw an exception that will report the exception into the channel using the bot based off the simple dictionary configuration in the file.

   ::

        $ ./slack_driven_development.py 
        Testing an Exception that shows up in Slack
        Sending an error message to Slack for Exception(name 'testing_how_this_looks_from_slack' is not defined)
        Done
        $

#. Confirm the debugging message shows up in Slack channel

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/07SlackDrivenDevelopmentExample.png

.. _dictionary object: https://github.com/jay-johnson/slack-driven-development/blob/78ced381ce1a1594e735943a8a9ab145425fe7d1/slack_driven_development.py#L5-L11
.. _slack_driven_development.py: https://github.com/jay-johnson/slack-driven-development/blob/master/slack_driven_development.py



Screenshots for Getting Started
-------------------------------

Here are the screenshots (as of **06-15-2016**) for getting this demo integrated with your Slack channel and bot:

**1. Create a new Slack App Integration**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/01SlackAddANewIntegration.png


**2. Build a new Integration**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/02SlackBuild.png
    

**3. Make a Custom Integration**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/03SlackMakeCustomIntegration.png


**4. Create a new Bot**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/04SlackBotCreateNewBot.png
    

**5. Name and Add Bot**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/05SlackNameAndAddBot.png
    

**6. Record the Bot API Token in the Dictionary Configuration**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/06SlackRecordBotAPIToken.png
    

**7. Run the Slack Driven Development Demo**

.. image:: https://raw.githubusercontent.com/jay-johnson/slack-driven-development/master/images/07SlackDrivenDevelopmentExample.png


How does this work?
-------------------

1. By using a `try/catch block`_ we can capture the exception, and pass it into a `handler method`_.

   .. code-block:: python
      :linenos:

      try:
          print "Testing an Exception that shows up in Slack"
          testing_how_this_looks_from_slack
      except Exception,k:
          print "Sending an error message to Slack for the expected Exception(" + str(k) + ")"
          slack_msg.handle_send_slack_internal_ex(k)
      # end of try/ex

.. _try/catch block: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_driven_development.py#L15-L21
.. _handler method: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L19-L33

2. `Prepare the exception`_

.. _Prepare the exception: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L19-L33

3. `Inspect the exception`_

   Python has a great little feature where it can `inspect the stacktrace`_ from an exception outside of the calling objects and even files. Once the file with the exception has been found, we can open the file and goto the `exact line that caused the exception`_ and `build an error report with the source code and the line number`_.

   .. code-block:: python
      :linenos:

      def get_exception_error_message(self, ex, exc_type, exc_obj, exc_tb):

          path_to_file = str(exc_tb.tb_frame.f_code.co_filename)
          last_line = int(exc_tb.tb_lineno)
          gh_line_number = int(last_line) - 1
          file_name = str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
          path_to_file = str(exc_tb.tb_frame.f_code.co_filename)
          py_file = open(path_to_file).readlines()
          line = ""
          for line_idx,cur_line in enumerate(py_file):
              if line_idx == gh_line_number:
                  line = cur_line
   
          if str(exc_obj.message) != "":
              ex_details_msg = str(exc_obj.message)
          else:
              ex_details_msg = str(ex)
   
          send_error_log_to_slack = ""
          if line != "":
              send_error_log_to_slack = " File: *" + str(path_to_file) + "* on Line: *" + str(last_line) + "* Code: \n```" + str(line) + "``` \n"
          else:
              send_error_log_to_slack = "Error on Line Number: " + str(last_line)
  
          return send_error_log_to_slack
      # end of get_exception_error_message

.. _Inspect the exception: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L36-L61
.. _inspect the stacktrace: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L38-L42
.. _exact line that caused the exception: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L42-L47
.. _build an error report with the source code and the line number: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L54-L58

4. `Send the message to the Slack channel`_

   Post the message to the Slack channel and handle any exceptions.

   .. note:: If your configuration `dictionary object`_ is misconfigured you will likely see an ``unauthorized`` error

.. _Send the message to the Slack channel: https://github.com/jay-johnson/slack-driven-development/blob/3d81ffe3084f91fbdead00218d07f8ec3cc231f5/slack_messenger.py#L70-L76
.. _dictionary object: https://github.com/jay-johnson/slack-driven-development/blob/78ced381ce1a1594e735943a8a9ab145425fe7d1/slack_driven_development.py#L5-L11

License
-------

This repository is licensed under the MIT license.


Want to learn more?
------------------

*  .. raw:: html 

        <a href="mailto:jay.p.h.johnson@gmail.com?Subject=Hello"><i class="fa fa-envelope"></i> Email me</a>

* `Contact Information`_

.. _Contact Information: http://jaypjohnson.com/contact.html

