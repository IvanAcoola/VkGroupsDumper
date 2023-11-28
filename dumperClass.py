import os
import vk_api
import sqlite3
import datetime


class VkGroupDumper:
    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.gr_info = self.session.method("groups.getById", {})
        if os.path.exists(f'{self.gr_info[0]["screen_name"]}.db'):
            print(f'[ Group-Dumper ] CRITICAL-ERROR: .db already exists')
            exit(-1)
        self.sqlite = sqlite3.connect(f'{self.gr_info[0]["screen_name"]}.db')
        self.db = self.sqlite.cursor()
        print(f'[ Group-Dumper ] created {self.gr_info[0]["screen_name"]}.db')

    def get_admins(self):
        start = self.session.method("groups.getMembers",
                                    {'count': 200, 'group_id': self.gr_info[0]["id"], 'filter': 'managers'})
        total = start['count']
        now = 200
        admins = start['items']
        while total > now:
            temp = self.session.method("groups.getMembers",
                                       {'count': 200, 'group_id': self.gr_info[0]["id"],
                                        'filter': 'managers', 'offset': now})
            admins += temp['items']
            now += 200
        return admins

    def get_subs(self):
        start = self.session.method("groups.getMembers",
                                    {'count': 200, 'group_id': self.gr_info[0]["id"]})
        total = start['count']
        now = 200
        subs = start['items']
        while total > now:
            temp = self.session.method("groups.getMembers",
                                       {'count': 200, 'group_id': self.gr_info[0]["id"], 'offset': now})
            subs += temp['items']
            now += 200
        return subs

    def get_all_conversations(self):
        start = self.session.method("messages.getConversations", {'count': 200})
        total = start['count']
        now = 200
        conversations = start['items']
        while total > now:
            temp = self.session.method("messages.getConversations", {'count': 200, 'offset': now})
            conversations += temp['items']
            now += 200
        return conversations

    def get_all_messages(self, user_id):
        start = self.session.method("messages.getHistory", {'count': 200, 'user_id': user_id})
        total = start['count']
        now = 200
        messages = start['items']
        while total > now:
            temp = self.session.method("messages.getHistory", {'count': 200, 'user_id': user_id, 'offset': now})
            messages += temp['items']
            now += 200
        return messages

    def get_banned(self):
        start = self.session.method("groups.getBanned", {'count': 200, 'group_id': self.gr_info[0]["id"]})
        total = start['count']
        now = 200
        banned = start['items']
        while total > now:
            temp = self.session.method("groups.getBanned",
                                       {'count': 200, 'group_id': self.gr_info[0]["id"], 'offset': now})
            banned += temp['items']
            now += 200
        return banned

    def dump_all(self):
        self.db.execute(f"""CREATE TABLE members (vk_id integer)""")
        self.sqlite.commit()
        for member in self.get_subs():
            self.db.execute(f"""INSERT INTO members VALUES ({member})""")
            self.sqlite.commit()
        self.db.execute(f"""CREATE TABLE admins (vk_id integer, role text)""")
        self.sqlite.commit()
        print(f'[ Group-Dumper ] dumped members')
        for admin in self.get_admins():
            self.db.execute(f"""INSERT INTO admins VALUES ({admin["id"]}, "{admin["role"]}")""")
            self.sqlite.commit()
        self.db.execute(f"""CREATE TABLE banned (vk_id integer, comment text)""")
        self.sqlite.commit()
        print(f'[ Group-Dumper ] dumped admins')
        for banned in self.get_banned():
            self.db.execute(f"""INSERT INTO banned VALUES 
            ({banned["profile"]["id"]}, "{banned["ban_info"]["comment"]}")""")
            self.sqlite.commit()
        print(f'[ Group-Dumper ] dumped ban-list')
        for conv in self.get_all_conversations():
            self.db.execute(f"""CREATE TABLE id{conv['conversation']['peer']['id']} 
            (vk_id integer, messagetext text,mtime text)""")
            self.sqlite.commit()
            print(f"[ Group-Dumper ] dumping dialog with id {conv['conversation']['peer']['id']}")
            for mess in self.get_all_messages(conv['conversation']['peer']['id'])[::-1]:
                try:
                    self.db.execute(
                        f"""INSERT INTO id{conv['conversation']['peer']['id']} VALUES 
                        ({mess["from_id"]}, 
                        "{mess["text"].replace('"', '.').replace("(", "{").replace(")", "}")}", 
                        "{str(datetime.datetime.fromtimestamp(mess["date"]).strftime("%d-%m-%Y %H:%M:%S"))}")""")
                    self.sqlite.commit()
                except Exception as exc:
                    print(f'[ Group-Dumper ] #error {exc}')
        self.sqlite.close()
