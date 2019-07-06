from slacker import Slacker
from config import config

API_KEY = None
CHANNEL = None
slacker = None

if 'slack' in config.keys():
    API_KEY = config['slack']['API_KEY']
    CHANNEL = config['slack']['CHANNEL']
    slacker = Slacker(API_KEY)


def post_slack(_str=None, file_title=None, file_path=None, image_url=None, channel=None,):
    print('post_slack', _str)
    if slacker is None:
        print('slacker is None')
        return

    if channel is None:
        channel = CHANNEL


    if file_path:
        slacker.files.upload(
            file_path,
            channels=[channel],
            title=file_title,
            initial_comment=_str,
        )
    elif _str:
        slacker.chat.post_message(channel,
                                  _str,
                                  icon_emoji=':thomas_bayes:',
                                  username='librarian',
                                  attachments=[
                                      {
                                          "image_url": image_url
                                      }
                                  ])