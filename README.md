Wtp
=======

Wtp is a tool for analyze Whatsapp chats.

This tool uses the chat histoty (that can be acquired by the Whatsapp option 'Export chat') and displays in graphs information such as:

- number of sent messages by each user
- number of sent characters by each user
- number of sent messages every hour.
- etc

![chat](/docs/imgs/Figure_1.png)

Example
-------

```python
from Wtp import *

wtp = Wtp("path\\to\\WhatsApp Chat with Some Group or Someone.txt")
wtp.plot_msgs_by_users()
```
![out](/docs/imgs/Figure_3.png)

Installation
------------

```
> pip install Wtp
```

There is an option to download the Wtp.py file and run:

```
> python Wtp.py [-h] -f FILE [-i] [-e] [-u USERS] [-r HIDE] [-m_users] [-w_users] [-c_users] [-m_user_w MSGS_USER_W] [-m_users_w] [-m_chat] [-m_chat_w]
```

Documentation
-------------

- Common methods flags:
    - _path_chat_: path to the chat file (.txt);
    - _path_import_: path to the JSON file;
    - _i_: When True, initialize the object by the given JSON file. Default=False;
    - _\_u\__: number of users to show in graph. Default:all;
    - _hide_: When True, display name/number of users in graph. Default=False.

- Methods:
    - plot_msgs_by_users(\_u\_=None, hide=True): Plot # of msgs by each user.
    - plot_words_by_users(\_u\_=None, hide=True): Plot # of words by each user.
    - plot_charac_by_users(\_u\_=None, hide=True): Plot # of characters by each user.
    - plot_user_msgs_by_weekday(id, hide=True, t="u: 1"): Plot # of msgs of a given _id_ by weekdays.
    - plot_users_msgs_by_weekday(\_u\_=None, hide=True): Plot # of msgs by each user by weekdays.
    - plot_chat_msgs_by_weekday(): Plot # of msgs by weekdays.
    - plot_chat_msgs_by_hour(): Plot # of msgs by hour.
    - export(name = "data.json", use_pprint = False): Export all data into a JSON file.
    - import_data(name = "data.json"): Import all data from a given JSON file.