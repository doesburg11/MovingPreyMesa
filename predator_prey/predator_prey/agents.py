import mesa
from predator_prey.random_walk import RandomWalker


class Prey(RandomWalker):
    """
    A prey that walks around, reproduces (asexually), eats grass and gets eaten by predators.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0

    def step(self):
        """
        A model step. Moves, ages, then eats grass or gets eaten or reproduce.
        """
        if self.model.verbose_1:
            print("prey_" + str(self.unique_id) + " moves [E:" + str(self.energy) + "]: " + str(self.pos) + "=>",
                  end="")
        self.random_move()
        # Reduce energy because of step
        self.energy -= 1  # TODO: energy loss depend on step size
        self.age += 1
        living = True
        if self.model.verbose_1:
            print(str(self.pos) + " [E:" + str(self.energy) + "]")

        # If there is grass available in cell, eat it
        agents_list_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patches_list_in_cell = [obj for obj in agents_list_in_cell if isinstance(obj, GrassPatch)]
        is_grass_patch_in_cell = len(grass_patches_list_in_cell) > 0
        if is_grass_patch_in_cell:
            grass_patch_in_cell_to_eat = [obj for obj in agents_list_in_cell if isinstance(obj, GrassPatch)][0]
            new_energy_prey = self.energy + grass_patch_in_cell_to_eat.energy
            if self.model.verbose_1:
                print("prey_" + str(self.unique_id) + " eats [E:" + str(self.energy) + "]=>[" + str(
                    new_energy_prey) + "]")
                print("grass_" + str(grass_patch_in_cell_to_eat.unique_id) + " eaten " + str(
                    grass_patch_in_cell_to_eat.pos) + " [E:" + str(grass_patch_in_cell_to_eat.energy) + "]=>", end="")
            if grass_patch_in_cell_to_eat.energy < self.model.min_energy_grass_regrowth:
                self.energy = new_energy_prey
                self.model.grid.remove_agent(grass_patch_in_cell_to_eat)
                self.model.schedule.remove(grass_patch_in_cell_to_eat)
                if self.model.verbose_1:
                    print("killed and removed")
            else:
                self.energy = new_energy_prey
                grass_patch_in_cell_to_eat.fully_grown = False
                grass_patch_in_cell_to_eat.energy = 0
                if self.model.verbose_1:
                    print("[E:" + str(grass_patch_in_cell_to_eat.energy) + "]")

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False
            if self.model.verbose_2:
                print("*   prey_" + str(self.unique_id) + " dies at age " + str(self.age) + " of starvation")
            self.model.datacollector.add_table_row(
                "Lifespan_Prey", {
                    "prey_id": self.unique_id,
                    "life_span": self.age,
                    "killed": False,
                }
            )
        else:
            # creation lottery
            if self.random.random() < self.model.prey_reproduce:
                # Create a new prey:
                if self.model.verbose_3:
                    print("*   prey_" + str(self.unique_id) + " creates at age " + str(self.age) + "[E:"+str(self.energy)+"]=>", end="")
                self.energy /= 2
                if self.model.verbose_3:
                    print("["+str(self.energy)+"]")
                created_id = self.model.next_id()
                created_prey = Prey(
                    created_id, self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(created_prey, self.pos)
                self.model.schedule.add(created_prey)
                if self.model.verbose_3:
                    print("*   prey_" + str(self.unique_id) + " creates at age " + str(self.age) + "[E:"+str(self.energy)+"]=> prey_"
                          + str(created_id) + " at " + str(self.pos))


class Predator(RandomWalker):
    """
    A predator that walks around, reproduces (asexually) and eats prey.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0

    def step(self):
        if self.model.verbose_1:
            print("predator_" + str(self.unique_id) + " moves [E:" + str(self.energy) + "]: " + str(self.pos) + "=>",
                  end="")
        self.random_move()
        self.age += 1
        self.energy -= 1
        if self.model.verbose_1:
            print(str(self.pos) + " [E:" + str(self.energy) + "]")

        # If there are prey present, eat one at random
        # TODO: eat prey with most energy
        agents_list_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        prey_list_in_cell = [obj for obj in agents_list_in_cell if isinstance(obj, Prey)]
        is_prey_in_cell = len(prey_list_in_cell) > 0
        if is_prey_in_cell:
            # eat random prey
            # TODO: eat prey with most energy or weakest prey if prey can resist?
            prey_in_cell_to_eat = self.random.choice(prey_list_in_cell)
            new_energy_predator = self.energy + prey_in_cell_to_eat.energy
            if self.model.verbose_1:
                print("predator_" + str(self.unique_id) + " eats [E:" + str(self.energy) + "]=>[" + str(
                    new_energy_predator) + "]")
                print("prey_" + str(prey_in_cell_to_eat.unique_id) + " eaten " + str(
                    prey_in_cell_to_eat.pos) + " [E:" + str(prey_in_cell_to_eat.energy) + "]=>", end="")

            # Kill the prey
            self.energy = new_energy_predator
            self.model.grid.remove_agent(prey_in_cell_to_eat)
            self.model.schedule.remove(prey_in_cell_to_eat)
            if self.model.verbose_1:
                print("killed and removed")
            if self.model.verbose_2:
                print("*   prey_" + str(prey_in_cell_to_eat.unique_id) + " dies at age " + str(prey_in_cell_to_eat.age) +
                      " of being eaten by predator_" + str(self.unique_id))
            self.model.datacollector.add_table_row(
                "Lifespan_Prey", {
                    "prey_id": prey_in_cell_to_eat.unique_id,
                    "life_span": prey_in_cell_to_eat.age,
                    "killed": True,
                }
            )

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            if self.model.verbose_2:
                print("*   predator_" + str(self.unique_id) + " dies at age " + str(self.age) + " of starvation")
            self.model.datacollector.add_table_row(
                "Lifespan_Predators", {
                    "predator_id": self.unique_id,
                    "life_span": self.age,
                }
            )
        else:
            # creation lottery
            if self.random.random() < self.model.predator_reproduce:
                # Create a new predator
                self.energy /= 2
                created_id = self.model.next_id()
                created_predator = Predator(
                    created_id, self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(created_predator, self.pos)
                self.model.schedule.add(created_predator)
                if self.model.verbose_3:
                    print("*   predator_" + str(self.unique_id) + " creates at age " + str(self.age) + " predator_"
                          + str(created_id) + " at " + str(self.pos))


class GrassPatch(mesa.Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by prey
    """

    def __init__(self, unique_id, pos, model, fully_grown, energy):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.pos = pos
        self.energy = energy
        self.regrowth_rate = self.model.grass_regrowth_rate

    def step(self):
        # print("grass_" + str(self.unique_id))
        if self.energy < self.model.max_energy_grass - self.model.grass_regrowth_rate:
            self.energy += self.model.grass_regrowth_rate  # grass_regrowth_rate = 1
        else:
            self.energy = self.model.max_energy_grass
            self.fully_grown = True
