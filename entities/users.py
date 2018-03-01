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


class Administrator(User):
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


class ContentCreator(User):
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


class DataAnalyst(User):
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


class Learner(User):
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
