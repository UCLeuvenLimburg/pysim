from pysim.actors.channel import RequestSender, RequestReceiver, create_channel
from threading import Thread
from typing import Callable, TypeVar, Generic, Tuple


T = TypeVar('T')

class Actor(Generic[T]):
    __receiver : RequestReceiver[T]

    def __init__(self, soul : Callable[[RequestSender], None]):
        pair : Tuple[RequestSender[T], RequestReceiver[T]] = create_channel()
        sender, self.__receiver = pair
        thread = Thread(target=lambda: soul(sender), daemon=True)
        thread.start()

    def receive_request(self) -> T:
        return self.__receiver.receive()

    def proceed(self) -> None:
        self.__receiver.release()