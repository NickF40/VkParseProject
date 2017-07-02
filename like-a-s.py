import json
import logging
import os
import time
import urllib.request as urllib
import zipfile

import vk

metadata = dict(
    __name__="Vk Friends Spy module",
    __version__="1.2",
    __license__="MIT License",
    __author__=u"Nick Yefremov <e_n_k@list.ru>",
    __url__="",
    __summary__="Software Metadata for Humans",
    __keywords__="Python / 3.5.2, OS independent, software development"
)

globals().update(metadata)

__all__ = metadata.keys()

logfile = ''  # 'logs.log', for example
logging.basicConfig(format=u'%(asctime)s | %(message)s',
                    level=logging.CRITICAL, filename=logfile)  # edit log's filename if needed

#               Put your
app_id = ''  # app id here
login = ''  # VK's login
password = ''  # Password for this login
my_id = ''  # VK id here

# open session
session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
api = vk.API(session=session)

# Our lovely offline access token (no exact IP required)
access_token = 'e4d4d64bf45e2fe82f5190309fd1f927fe15210654ece48f5a0c9dd509866784a191b0b0e7803b0389047'

# some string constants
request_url = 'https://api.vk.com/method/'
ac_tkn = '&access_token='
# method names
messages_get_method = 'messages.get'
mark_as_read_method = 'messages.markAsRead'
send_message_method = 'messages.send'
get_friends_method = 'friends.get'
get_user_method = 'users.get'


# obvious
def get_friends():
    get_friends_request = request_url + get_friends_method \
                          + '?user_id=' + my_id \
                          + '&order=hints' \
                          + '&fields=online,last_seen' \
                          + ac_tkn + access_token
    encrypted_data = urllib.urlopen(get_friends_request).read().decode()
    data = json.loads(encrypted_data).get('response')
    for user in data:
        if 'deactivated' in user.keys():
            continue
        if user.get('online') == 0:
            logging.log(logging.CRITICAL,
                        ' - '.join([str(user.get('user_id')), str(user.get('last_seen').get('time')), '2']))
        else:
            if 'online_mobile' in user.keys():
                logging.log(logging.CRITICAL, ' - '.join([str(user.get('user_id')), str(int(time.time())), '1']))
            else:
                logging.log(logging.CRITICAL, ' - '.join([str(user.get('user_id')), str(int(time.time())), '0']))


# logs look like this:
# '2017-06-14 17:22:23,560 | 426541359 - 1497444909 - 2'
#  date       time         | id        - last_seen  - code
#  code description:
#    2: Offline
#    1: Online, Mobile v.
#    2: Online, PC v.

while True:
    get_friends()
    if os.path.getsize('./' + logfile) > 1000000:  # ~ 1Mb
        to_zip = zipfile.ZipFile('./' + str(logfile.split('.')[0]) + str(time.gmtime(time.time()).tm_year) + '-' + str(
            time.gmtime(time.time()).tm_mon) + '-' + str(time.gmtime(time.time()).tm_mday) + '-' + str(
            time.gmtime(time.time()).tm_hour) + '-' + str(time.gmtime(time.time()).tm_min) + '-' + str(
            time.gmtime(time.time()).tm_sec) + '.zip', 'w')
        to_zip.write('./' + logfile, compress_type=zipfile.ZIP_DEFLATED)
        to_zip.close()
        open(logfile, 'w').close()
    time.sleep(3)
