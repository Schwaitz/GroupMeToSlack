# GroupMeToSlack
Get GroupMe data, send to Slack


### TODO

* Add support for Slack -> GroupMe
  * Automatic bot creation through GroupMe API
* Handle links / attachments
  * Slack has particular JSON parameters for links
  * Pretty easy to do
* Potentially scrape data for profile pictures
  * Not feeling confident on this
  
  
  
### Setup

* Make sure you are running Python 3.x
  * You can use python --version to check
  * Sometimes installations require "python3"
* Install requirements with pip
  * *pip install -r requirements.txt*
  * Similar to above, sometimes you need to use pip3
* Create a file called 'url.txt'
  * Put your Slack Outgoing Webhook url here on a single line
* Command line usage:
  * python GMToSlack.py \<port\>
  * The port should be the one that your callback url on GroupMe is set to
    * It is the port that your WebServer is served on
* Note:
  * My paths to the files 'log.txt' and 'url.txt' use the prefix '/home/ubuntu/GMTS/\<file\>
  * Make sure to change your paths to your particular setup
