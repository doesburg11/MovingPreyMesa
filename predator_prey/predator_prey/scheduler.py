from typing import Type, Callable
from collections import defaultdict

import mesa


class RandomActivationByTypeFiltered(mesa.time.RandomActivationByType):
    """
    A scheduler that overrides the get_type_count method to allow for filtering
    of agents by a function before counting.

    Example:
    >>> scheduler = RandomActivationByTypeFiltered(model)
    >>> scheduler.get_type_count(AgentA, lambda agent: agent.some_attribute > 10)
    """

    def get_type_count(
            self,
            type_class: Type[mesa.Agent],
            filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue that satisfy the filter function.
        """
        count = 0
        for agent in self.agents_by_type[type_class].values():
            if filter_func is None or filter_func(agent):
                count += 1
        return count


# pd: random activator mixing types and counting types
class RandomActivationByAllAgents(mesa.time.RandomActivation):

    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)

    def add(self, agent: mesa.Agent) -> None:
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """
        super().add(agent)
        agent_class: type[mesa.Agent] = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent: mesa.Agent) -> None:
        """
        Remove all instances of a given agent from the schedule.
        """
        del self._agents[agent.unique_id]

        agent_class: type[mesa.Agent] = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]

    def get_type_count(
            self,
            type_class: Type[mesa.Agent],
            filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue that satisfy the filter function.
        """
        count = 0
        for agent in self.agents_by_type[type_class].values():
            if filter_func is None or filter_func(agent):
                count += 1
        return count

    def get_energy_count(
            self,
            type_class: Type[mesa.Agent],
    ) -> float:
        """
        Returns the current number of agents of certain type in the queue that satisfy the filter function.
        """
        energy = 0
        for agent in self.agents_by_type[type_class].values():
            energy += agent.energy
        return energy



