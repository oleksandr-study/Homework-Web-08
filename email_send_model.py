from mongoengine import connect, Document, StringField, BooleanField

connect(db="homework08", host="mongodb://localhost:27017")


class Email_Send_To_Customer(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    send = BooleanField(default=False)