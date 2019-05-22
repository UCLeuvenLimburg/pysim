from typing import TypeVar, Generic, Callable, Any, cast, Tuple
from pysim.actors.status import Status
from enum import Enum


class ChannelStatus(Enum):
    WAITING_FOR_REQUEST = 1
    WAITING_FOR_RESPONSE = 2


T = TypeVar('T')

class _Channel(Generic[T]):
    '''
    A channel can be used to send messages between threads.
    This class should remain hidden; only
    RequestSender and RequestReceiver should be exposed.
    '''

    __status : Status[ChannelStatus]
    __request : T

    def __init__(self):
        self.__status = Status[ChannelStatus](ChannelStatus.WAITING_FOR_REQUEST)

    def send(self, request : T) -> None:
        self.__request = request
        self.__status.set(ChannelStatus.WAITING_FOR_RESPONSE)
        self.__status.wait(ChannelStatus.WAITING_FOR_REQUEST)

    def receive(self) -> T:
        self.__status.wait(ChannelStatus.WAITING_FOR_RESPONSE)
        return self.__request

    def release(self) -> None:
        self.__status.set(ChannelStatus.WAITING_FOR_REQUEST)


class RequestSender(Generic[T]):
    __channel : _Channel[T]

    def __init__(self, channel : _Channel[T]):
        self.__channel = channel

    def send(self, request : T) -> None:
        return self.__channel.send(request)


class RequestReceiver(Generic[T]):
    __channel : _Channel[T]

    def __init__(self, channel : _Channel[T]):
        self.__channel = channel

    def receive(self) -> T:
        return self.__channel.receive()

    def release(self) -> None:
        self.__channel.release()


def create_channel() -> Tuple[RequestSender[T], RequestReceiver[T]]:
    channel = _Channel[T]()
    return ( RequestSender(channel), RequestReceiver(channel) )
