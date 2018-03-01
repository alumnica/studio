from abc import ABC
from enum import Enum


class UserType(Enum):
    ADMINISTRATOR = 'Administrator'
    CONTENT_CREATOR = 'Content Creator'
    DATA_ANALYST = 'Data Analyst'
    LEARNER = 'Learner'


class User:
    @property
    def name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def email(self):
        pass

    @property
    def password(self):
        pass

    @property
    def type(self):
        pass


class Administrator(User, ABC):
    @property
    def name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def email(self):
        pass

    @property
    def password(self):
        pass

    @property
    def type(self):
        return UserType.ADMINISTRATOR


class ContentCreator(User, ABC):
    @property
    def name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def email(self):
        pass

    @property
    def password(self):
        pass

    @property
    def type(self):
        return UserType.CONTENT_CREATOR


class DataAnalyst(User, ABC):
    @property
    def name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def email(self):
        pass

    @property
    def password(self):
        pass

    @property
    def type(self):
        return UserType.DATA_ANALYST


class Learner(User, ABC):
    @property
    def name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def email(self):
        pass

    @property
    def password(self):
        pass

    @property
    def type(self):
        return UserType.LEARNER
