from mongoengine import Document, StringField, EmailField


class User(Document):

    full_name = StringField(
        required=True,
        max_length=100
    )

    email = EmailField(
        required=True,
        unique=True
    )

    phone = StringField(
        max_length=15,
        default="N/A"
    )

    password = StringField(
        required=True
    )

    meta = {
        "collection": "users"
    }