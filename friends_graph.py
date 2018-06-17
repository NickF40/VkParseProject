import json
import logging
# import os
# import time
import matplotlib.pyplot as mp
import networkx as nx

import urllib.request as urllib
# import zipfile
from pprint import pprint as pp
# import vk


metadata = dict(
    __name__="Vk Friends Spy module",
    __version__="1.2",
    __license__="MIT License",
    __author__=u"Nick Yefremov <e_n_k@list.ru>",
    __url__="https://github.com/NickF40/VkSpyProject/",
    __summary__="Software Metadata for Humans",
    __keywords__="Python / 3.5.2, OS independent, software development"
)

globals().update(metadata)

__all__ = metadata.keys()

logfile = 'logs.log'  # 'logs.log', for example
logging.basicConfig(format=u'%(asctime)s | %(message)s',
                    level=logging.CRITICAL, filename=logfile)  # edit log's filename if needed

#               Put your
app_id = ''  # app id here
login = ''  # VK's login
password = ''  # Password for this login
my_id = ''  # VK id here

# open session
# session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
# api = vk.API(session=session)

# Our lovely offline access token (no exact IP required)
access_token = ''

# some string constants
request_url = 'https://api.vk.com/method/'
ac_tkn = '&access_token='

# method names
get_friends_method = 'friends.get'
get_user_method = 'users.get'
friends_links = {}

users_dict = {}


# obvious
def get_friends(user_id):
    get_friends_request = request_url + get_friends_method \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 + '?user_id=' + str(user_id) \
                          + '&order=hints' \
                          + '&fields=city,country,timezone' \
                          + ac_tkn + access_token + '&v=5.78'
    try:
        encrypted_data = urllib.urlopen(get_friends_request).read().decode()
        data = json.loads(encrypted_data).get('response').get('items')
    except AttributeError:
        return {}

    return data


def create_graph():
    for friend in get_friends(my_id):
            users_dict.update({fr.get('id'): fr.get('last_name') for fr in get_friends(friend.get('id'))})
            users_dict.update({friend.get('id'): friend.get('last_name')})
            friends_links[friend.get('id')] = {fr.get('id') for fr in get_friends(friend.get('id'))}

create_graph()

G = nx.Graph()
G.add_nodes_from([val for val in users_dict.values()])
edges = []
for item in friends_links.items():
    for fr in item[1]:
        edges.append((users_dict.get(item[0]), users_dict.get(fr)))
pp(edges)
G.add_edges_from(edges)

options = {
    'node_color': 'black',
    'with_labels': True,
    'node_size': 50,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.1,
}
nx.draw(G, **options)
mp.show()