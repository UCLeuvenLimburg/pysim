from __future__ import annotations
from pysim.actors.channel import create_channel, RequestSender, RequestReceiver
from pysim.actors.actor import Actor
from pysim.simulation.vector import Vector, NORTH
from typing import Tuple, List
from threading import Thread



class SimulationState:
    __car_positions : List[Vector]

    def __init__(self, car_positions : List[Vector]):
        self.__car_positions = car_positions

    def forward(self, car_index : int) -> SimulationState:
        car_positions : List[Vector] = [ *self.__car_positions ]
        car_positions[car_index] += NORTH
        return SimulationState(car_positions)


class Simulation:
    __state : SimulationState

    def __init__(self):
        self.__state = SimulationState( [Vector(0,0), Vector(0,5)] )

    def perform(actions):
        for action in actions:
            self.__state = action.apply(self.__state)

    @property
    def state(self) -> SimulationState:
        return self.__state



class Simulator:
    __simulation : Simulation
    __actors : List[Actor]

    def __init__(self, simulation, actors):
        self.__simulation = simulation
        self.__actors = actors

    def step(self):
        actions = [ actor.receive() for actor in self.__actors ]
        self.__simulation.perform(actions)
        for actor in self.__actors:
            actor.proceed()



class ForwardAction(Request[None]):
    __id : int

    def __init__(self, id : int):
        self.__id = id

    def apply(self, simulation_state : SimulationState) -> SimulationState:
        return simulation_state.forward(self.__id)


class StopAction(Request[None]):
    pass


code = '''
forward()
'''


def main():
    simulator = Simulator()

    def create_actor(id : int) -> None:
        environment = simulator.create_actor_environment(id)
        def thread_proc() -> None:
            exec(code, environment)
        thread = Thread(target=thread_proc, daemon=True)
        thread.start()

    for id in [0, 1]:
        create_actor(id)

    simulator.step()

main()