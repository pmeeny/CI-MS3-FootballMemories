from mongoengine import Document, IntField, StringField


class Users(Document):
    user_type = StringField(max_length=20, required=True)
    username = StringField(max_length=30, required=True, unique=True)
    password = StringField(max_length=30, required=True)
    first_name = StringField(max_length=30, required=True)
    last_name = StringField(max_length=30, required=True)
    favourite_team = StringField(max_length=50, required=True)
    country = StringField(max_length=50, required=True)


class Tournaments(Document):
    tournament_name = StringField(max_length=50, required=True, unique=True)
    tournament_image = StringField(max_length=100, required=True, unique=True)


class Ratings(Document):
    memory_id = StringField(max_length=30, required=True)
    memory_view_count = IntField(max_length=1, required=True)
    rating_created_by = StringField(max_length=30, required=True)


class Comments(Document):
    memory_id = StringField(max_length=20, required=True)
    comment_text = StringField(max_length=100, required=True)
    comment_date = StringField(max_length=10, required=True)
    comment_created_by = StringField(max_length=30, required=True)


class Memories(Document):
    tournament_image = StringField(max_length=100, required=True, unique=True)
    tournament_name = StringField(max_length=50, required=True)
    memory_name = StringField(max_length=50, required=True)
    memory_description = StringField(max_length=100, required=True)
    memory_date = StringField(max_length=10, required=True)
    memory_stadium = StringField(max_length=50, required=True)
    memory_view_count = IntField(max_length=50, required=True)
    memory_created_by = StringField(max_length=30, required=True)
