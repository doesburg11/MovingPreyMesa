import mesa
from predator_prey.random_walk import RandomWalker


class Prey(RandomWalker):

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
        if len(grass_patches_list_in_cell) > 0: # is_grass_patch_in_cell
            # eat grass
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
                new_energy_mother = self.energy / 2
                new_energy_child = self.energy - new_energy_mother
                created_id = self.model.next_id()
                if self.model.verbose_3:
                    print("prey_" + str(self.unique_id) + " creates prey_" + str(created_id) +
                          " [E:"+str(new_energy_child)+"] at age " + str(self.age) +
                          " [E:"+str(self.energy)+"]=>[E:"+str(new_energy_mother)+"]")
                self.energy = new_energy_mother
                created_prey = Prey(
                    created_id, self.pos, self.model, self.moore, new_energy_child
                )
                self.model.grid.place_agent(created_prey, self.pos)
                self.model.schedule.add(created_prey)


class Predator(RandomWalker):

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
        if len(prey_list_in_cell) > 0:  # if is_prey_list_in_cell
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
                print("prey_" + str(prey_in_cell_to_eat.unique_id) + " dies at age " + str(prey_in_cell_to_eat.age) +
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
                new_energy_mother = self.energy / 2
                new_energy_child = self.energy - new_energy_mother
                created_id = self.model.next_id()
                if self.model.verbose_3:
                    print("predator_" + str(self.unique_id) + " creates predator_" + str(created_id) +
                          " [E:"+str(new_energy_child)+"] at age " + str(self.age) +
                          " [E:"+str(self.energy)+"]=>[E:"+str(new_energy_mother)+"]")
                self.energy = new_energy_mother
                created_predator = Predator(
                    created_id, self.pos, self.model, self.moore, new_energy_child
                )
                self.model.grid.place_agent(created_predator, self.pos)
                self.model.schedule.add(created_predator)


class GrassPatch(mesa.Agent):

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
