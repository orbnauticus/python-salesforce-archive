"""

"""


import datetime


class reference:
    def __init__(self, table):
        self.table = table

    def __call__(self, value):
        return value


class identifier(str):
    pass


def DateTime(value):
    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


schema = {
    "Attachment": {
        'Id': 'Id',
        'Title': 'Name',
        'File': 'Attachments/{Id}',
        'DataTypes': {
            'IsPrivate': bool,
            'Description': str,
            'OwnerId': reference('User'),
            'CreatedById': reference('User'),
            'BodyLength': int,
            'CreatedDate': DateTime,
            'Name': str,
            'Id': identifier,
            'FeedItemId': identifier,
            'LastModifiedDate': DateTime,
            'BodyLengthCompressed': int,
            'ContentType': str,
            'LastModifiedById': reference('User'),
            'AccountId': reference('Account'),
            'SystemModstamp': DateTime,
            'ParentId': identifier,
            'IsDeleted': bool,
        },
    }
}

get = schema.get
