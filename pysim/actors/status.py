from typing import TypeVar, Generic, List
from threading import Condition


T = TypeVar('T')

class Status(Generic[T]):
    def __init__(self, initial_status : T):
        self.__status = initial_status
        self.__condition = Condition()

    def set(self, status : T) -> None:
        '''
        Sets the status value. All waiting threads are notified.
        '''
        with self.__condition:
            self.__status = status
            self.__condition.notifyAll()

    def wait(self, *wait_for : T) -> T:
        with self.__condition:
            self.__condition.wait_for(lambda: self.__status in wait_for)
            return self.__status
