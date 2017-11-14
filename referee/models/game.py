from datetime import datetime

from peewee import (BigIntegerField, BooleanField, CharField, DateTimeField,
                    IntegerField, SmallIntegerField, TextField)

from referee.db import BaseModel
from referee.util.input import parse_duration


@BaseModel.register
class Game(BaseModel):
    """Game Object"""
    name = CharField()
    desc = TextField()
    a_channel = BigIntegerField(null=True)
    a_message = CharField(null=True)
    next_announcement = DateTimeField(null=True)
    last_announcement = DateTimeField()
    interval = CharField(null=True)

    class Meta:
        db_table = 'games'

    def set_announcement_channel(self, a_channel):
        query = Game.update(a_channel=a_channel)
        query.where(Game.name == self.name).execute()

    def set_announcement_message(self, message):
        query = Game.update(a_message=message)
        query.where(Game.name == self.name).execute()

    def clear_interval(self):
        query = Game.update(next_announcement=None, interval=None)
        query.where(Game.name == self.name).execute()

    def set_interval(self, interval):
        try:
            next_announcement = parse_duration(interval)
        except:
            print 'Ermahgerd! Something sploded'
        query = Game.update(next_announcement=next_announcement, interval=interval)
        query.where(Game.name == self.name).execute()

    @classmethod
    def new(cls, name, desc, ac=None):
        return cls.create(
            name=name,
            desc=desc,
            a_channel=ac,
            a_message=None,
            interval=None,
            last_announcement=datetime.utcnow(),
            next_announcement=None
        )

    @classmethod
    def get_game_by_name(cls, name):
        try:
            return Game.select().where(
                Game.name == name
            ).limit(1).get()
        except Game.DoesNotExist:
            return None