from abc import ABC, abstractmethod
from enum import Enum


class UserType(Enum):
    ADMINISTRATOR = 'Administrator'
    CONTENT_CREATOR = 'Content Creator'
    DATA_ANALYST = 'Data Analyst'
    LEARNER = 'Learner'


class User(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def last_name(self):
        pass

    @property
    @abstractmethod
    def email(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass


class Administrator(User, ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def last_name(self):
        pass

    @property
    @abstractmethod
    def email(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    def type(self):
        return UserType.ADMINISTRATOR


class ContentCreator(User, ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def last_name(self):
        pass

    @property
    @abstractmethod
    def email(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    def type(self):
        return UserType.CONTENT_CREATOR


class DataAnalyst(User, ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def last_name(self):
        pass

    @property
    @abstractmethod
    def email(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    def type(self):
        return UserType.DATA_ANALYST


class Learner(User, ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def last_name(self):
        pass

    @property
    @abstractmethod
    def email(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    def type(self):
        return UserType.LEARNER
