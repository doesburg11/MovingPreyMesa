"""
Predator-Prey Model

Adjustment of:
1.    Wilensky, U. (1997). NetLogo Predator Prey model
2.    Olsen(2015)

"""

import mesa

from predator_prey.scheduler import RandomActivationByTypeFiltered, RandomActivationByAllAgents

from predator_prey.agents import Prey, Predator, GrassPatch

class PredatorPrey(mesa.Model):
    height = 10
    width = 10

    initial_prey = 10
    initial_predators = 5

    prey_reproduce = 0.04
    predator_reproduce = 0.05

    predator_gain_from_food = 20

    grass = False
    prey_gain_from_food = 4
    max_energy_grass = 20
    min_energy_grass_regrowth = 5
    """
        max_energy_grass: the maximum energy level of grass
        min_energy_grass_regrowth: when grass eaten below min_energy_grass_regrowth, grass regrowth will not occur
    """
    grass_regrowth_rate = 1.0  # pd

    verbose_0 = False  # agent count
    verbose_1 = False  # agent_id activation
    verbose_2 = False  # agent death
    verbose_3 = False  # agent birth
    verbose_4 = False  # agent life span table
    verbose_5 = False  # agent life span average

    is_per_type_random_activated = False
    """
    False: agent are all random activated regardless of type,
    if True agents are random per agent type and random per class
    """
    description = (
        "A model for simulating Predator-Prey  modelling."
    )

    def __init__(
            self,
            width=10,
            height=10,
            initial_prey=10,
            initial_predators=5,

            prey_reproduce=0.04,
            predator_reproduce=0.05,
            predator_gain_from_food=20,

            grass=True,
            grass_regrowth_rate=1.0,
    ):
        """
        Create a new Predator-Prey model with the given parameters.

        Args:
            initial_prey: Number of prey to start with
            initial_predators: Number of predators to start with
            prey_reproduce: Probability of each prey reproducing each step
            predator_reproduce: Probability of each predator reproducing each step
            predator_gain_from_food: Energy a predator gains from eating a prey
            grass: Whether to have the prey eat grass for energy
            grass_regrowth_rate: Increase in energy per model step du to regrowth GrassPatch
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_prey = initial_prey
        self.initial_predators = initial_predators
        self.prey_reproduce = prey_reproduce
        self.predator_reproduce = predator_reproduce
        self.predator_gain_from_food = predator_gain_from_food
        self.grass = grass
        self.grass_regrowth_rate = grass_regrowth_rate

        self.schedule = RandomActivationByTypeFiltered(self) if self.is_per_type_random_activated else \
            RandomActivationByAllAgents(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Predators": lambda m: m.schedule.get_type_count(Predator),
                "Prey": lambda m: m.schedule.get_type_count(Prey),
                "GrassPatches": lambda m: m.schedule.get_type_count(GrassPatch, lambda g: g.fully_grown),
                "Predators_energy": lambda m: m.schedule.get_energy_count(Predator),
                "Prey_energy": lambda m: m.schedule.get_energy_count(Prey),
                "GrassPatch_energy": lambda m: m.schedule.get_energy_count(GrassPatch),
            },
            tables={
                "Lifespan_Predators": ["predator_id", "life_span"],
                "Lifespan_Prey": ["prey_id", "life_span", "killed"],
            },
        )

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():
                fully_grown = True
                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, self.max_energy_grass)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        # Create predators
        for i in range(self.initial_predators):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.predator_gain_from_food)
            predator = Predator(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(predator, (x, y))
            self.schedule.add(predator)

        # Create prey:
        for i in range(self.initial_prey):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.prey_gain_from_food)
            prey = Prey(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(prey, (x, y))
            self.schedule.add(prey)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose_0:
            print(self.datacollector.get_model_vars_dataframe())
        if self.verbose_4:
            print("tables:  ")
            # print(self.datacollector.get_table_dataframe("Lifespan_Prey")["life_span"])
            print(self.datacollector.get_table_dataframe("Lifespan_Predators"))
            print(self.datacollector.get_table_dataframe("Lifespan_Prey"))
            print("model_reporters:")
            print(self.datacollector.get_model_vars_dataframe())

        if self.verbose_5:
            print("Average life time Prey: ", end="")
            print(self.datacollector.get_table_dataframe("Lifespan_Prey")["life_span"].mean())
        if self.verbose_5:
            print("Average life time Predators: ", end="")

            print(self.datacollector.get_table_dataframe("Lifespan_Predators")["life_span"].mean())

        if self.verbose_0:
            print([self.schedule.time,
                   self.schedule.get_type_count(Predator),
                   self.schedule.get_type_count(Prey),
                   self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown)])

    def run_model(self, step_count=200):
        if self.verbose_0:
            print("Initial number predators: ", self.schedule.get_type_count(Predator))
            print("Initial number prey: ", self.schedule.get_type_count(Prey))
            print("Initial number grass: ",
                  self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown))

        for i in range(step_count):
            self.step()

        if self.verbose_0:
            print("")
            print("Final number predators: ", self.schedule.get_type_count(Predator))
            print("Final number prey: ", self.schedule.get_type_count(Prey))
            print("Final number grass: ",
                  self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
                  )
