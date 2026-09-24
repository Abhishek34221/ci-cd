from mongoengine import (
    Document,
    StringField,
    FloatField,
    BooleanField
)


class Destination(Document):

    name = StringField(required=True)

    country = StringField(required=True)

    rating = FloatField(
        min_value=0,
        max_value=5,
        default=0
    )

    price = StringField(required=True)

    status = StringField(
        default="active"
    )

    code = StringField(
        default=""
    )

    image = StringField(
        required=True
    )

    description = StringField(
        required=True
    )

    favorite = BooleanField(
        default=False
    )

    meta = {
        "collection": "destinations"
    }