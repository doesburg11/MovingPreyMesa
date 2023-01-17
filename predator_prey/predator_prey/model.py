"""
Predator-Moving-Prey Model

"""

import mesa

from predator_prey.scheduler import RandomActivationByTypeFiltered, RandomActivationByAllAgents

from predator_prey.agents import Prey, Predator


class PredatorPrey(mesa.Model):
    n_grid_cells_height = 5
    n_grid_cells_width = 5
    canvas_width = 500
    canvas_height = canvas_width * (n_grid_cells_height / n_grid_cells_width)
    # Predators
    initial_predators = 1
    initial_energy_predators = 20.0
    max_energy_predators = 50
    homeostatic_energy_predator = 1.0
    """TODO implement; energy loss due to homeostasis"""
    """for simplicity reason we translate evolutionary fitness into energy"""
    predator_reproduce = 0.0

    # Prey
    initial_prey = 1
    initial_energy_prey = 15.0
    max_energy_prey = 30.0
    homeostatic_energy_prey = 1.0
    prey_reproduce = 0.0

    verbose_0 = True  # agent count
    verbose_1 = True  # agent_id activation move and eat
    verbose_2 = True  # agent death
    verbose_3 = True  # agent birth
    verbose_4 = False  # agent life span table
    verbose_6 = False  # table agent count and cumulative energy per type

    is_per_type_random_activated = False
    """
    False: agent are all random activated regardless of type,
    if True agents are random per agent type and random per class
    """
    description = (
        "A model for simulating Predator-Prey behavior."
    )

    def __init__(
            self,
            n_grid_cells_width=n_grid_cells_width,
            n_grid_cells_height=n_grid_cells_height,
            initial_prey=initial_prey,
            initial_predators=initial_predators,
            prey_reproduce=prey_reproduce,
            predator_reproduce=predator_reproduce,
            initial_energy_predators=initial_energy_predators,
            initial_energy_prey=initial_energy_prey,
            max_energy_predators=max_energy_predators,
            max_energy_prey=max_energy_prey,

    ):
        """
        Create a new Predator-Prey model with the given parameters.

        Args:
            initial_prey: Number of prey to start with
            initial_predators: Number of predators to start with
            prey_reproduce: Probability of each prey reproducing each step
            predator_reproduce: Probability of each predator reproducing each step
        """
        super().__init__()
        # Set parameters
        self.n_grid_cells_width = n_grid_cells_width
        self.n_grid_cells_height = n_grid_cells_height

        self.initial_prey = initial_prey
        self.initial_predators = initial_predators
        self.prey_reproduce = prey_reproduce
        self.predator_reproduce = predator_reproduce

        self.initial_energy_predators = initial_energy_predators
        self.initial_energy_prey = initial_energy_prey
        self.max_energy_predators = max_energy_predators
        self.max_energy_prey = max_energy_prey
        self.schedule = RandomActivationByTypeFiltered(self) if self.is_per_type_random_activated else \
            RandomActivationByAllAgents(self)
        self.grid = mesa.space.MultiGrid(self.n_grid_cells_width, self.n_grid_cells_height, torus=True)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Predators": lambda m: m.schedule.get_type_count(Predator),
                "Prey": lambda m: m.schedule.get_type_count(Prey),
                "Predators_energy": lambda m: m.schedule.get_energy_count(Predator),
                "Prey_energy": lambda m: m.schedule.get_energy_count(Prey),
            },
        )

        # Create predators
        for i in range(self.initial_predators):
            x = self.random.randrange(self.n_grid_cells_width)
            y = self.random.randrange(self.n_grid_cells_height)
            energy = self.initial_energy_predators
            predator = Predator(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(predator, (x, y))
            self.schedule.add(predator)

        # Create prey:
        for i in range(self.initial_prey):
            x = self.random.randrange(self.n_grid_cells_width)
            y = self.random.randrange(self.n_grid_cells_height)
            energy = self.initial_energy_prey
            prey = Prey(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(prey, (x, y))
            self.schedule.add(prey)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()

        # collect data
        self.datacollector.collect(self)
        if self.verbose_6:
            print(self.datacollector.get_model_vars_dataframe())
        if self.verbose_4:
            print("tables:")
            # print(self.datacollector.get_table_dataframe("Lifespan_Prey")["life_span"])
            print(self.datacollector.get_table_dataframe("Lifespan_Predators"))
            print(self.datacollector.get_table_dataframe("Lifespan_Prey"))

        if self.verbose_6:
            print([self.schedule.time,
                   self.schedule.get_type_count(Predator),
                   self.schedule.get_type_count(Prey),
                   self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown)])
        df_predators = self.datacollector.get_model_vars_dataframe()["Predators"]
        df_prey = self.datacollector.get_model_vars_dataframe()["Prey"]
        if df_predators.iloc[-1] == 0 and df_predators.iloc[-1] == 0:
            # https://stackoverflow.com/questions/34166030/obtaining-last-value-of-dataframe-column-without-index
            self.running = False
            # stops simulation when both agents are dead
            # todo: make batches to record the average length of the simulation with parameter changes
        """
        print(self.datacollector.get_model_vars_dataframe())
        print(self.datacollector.get_model_vars_dataframe()["Predators"])
        print(self.datacollector.get_model_vars_dataframe()["Prey"])
        print(df_predators.iloc[-1])
        print(df_prey.iloc[-1])
        """
