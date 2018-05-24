from hashlib import sha224
from json import dumps
from azure.cosmosdb.table import EntityProperty as ep
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import EdmType
import message_pb2


"""
Author: Rafal Marguzewicz
Email: info@pceuropa.net
Github: https://github.com/pceuropa/
Description: App need Azure account name and key to run correctly on http://127.0.0.1:5000/
"""


ACCOUNT_NAME = 'account_name'
ACCOUNT_KEY = 'acount_key'
USER_TABLE_NAME = 'users'
MESSAGE_TABLE_NAME = 'message'
email = 'test@email.net'
row_key = '001'


class Db(object):

    ts = None

    def __init__(self):
        """Init connection with cosmosdb"""
        self.ts = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

    def migrate(self):
        """ Create tabel if not exists"""
        if not self.ts.exists(USER_TABLE_NAME):
            self.ts.create_table(USER_TABLE_NAME)

        if not self.ts.exists(MESSAGE_TABLE_NAME):
            self.ts.create_table(MESSAGE_TABLE_NAME)

    def get_all_users(self):
        """select email from user"""
        return [i['PartitionKey'] for i in self.ts.query_entities(USER_TABLE_NAME)]

    def create_user(self, data=None):
        bjson = ep(EdmType.BINARY, dumps({
            'email': data['email'],
            'password': sha224(bytes(data['password'], encoding='utf-8')).hexdigest(),
            'full_name': data['full_name']
        }))

        user = {
            'PartitionKey': data['email'],
            'RowKey': row_key,
            'info': bjson
        }

        if (self.ts.insert_or_replace_entity(USER_TABLE_NAME, user)):
            return {'success': True}

    def delete_user(self, email=None):
        if (self.ts.delete_entity(USER_TABLE_NAME, email, row_key)):
            return {'success': True}

    def create_message(self, email=None, message=None):
        """ Create message in protobuf"""
        proto_message = message_pb2.Message()
        proto_message.title = message['title']
        proto_message.content = message['content']
        proto_message.magic_number = message['magic_number']
        details = ep(EdmType.BINARY, str(proto_message))

        bmessage = {
            'PartitionKey': email,
            'RowKey': row_key,
            'details': details,
        }

        if (self.ts.insert_or_replace_entity(MESSAGE_TABLE_NAME, bmessage)):
            return {'success': True}

    def get_user(self, email=''):
        return self.ts.get_entity(USER_TABLE_NAME, email, row_key)

    def get_message(self, email=''):
        return self.ts.get_entity(MESSAGE_TABLE_NAME, email, row_key)

    def get_messages(self):
        messages = self.ts.query_entities(MESSAGE_TABLE_NAME)
        return list(messages)
