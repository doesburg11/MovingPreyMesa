import mesa
from predator_prey.random_walk import RandomWalker


class Prey(RandomWalker):
    name = "prey"

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0

    def step(self):
        """
        A model step. Moves, ages, then eats grass or gets eaten or reproduce.
        """
        if self.model.verbose_1:
            print("-----------------------------------------------------------")
            print("prey_" + str(self.unique_id) + " moves [E:" + str(round(self.energy, 1)) + "]: " + str(
                self.pos) + "=>",
                  end="")
        self.random_move()
        # Reduce energy because of step
        self.energy -= 1
        self.age += 1
        if self.model.verbose_1:
            print(str(self.pos) + " [E:" + str(round(self.energy, 1)) + "]")

        # If there is grass available in cell, eat it
        agents_list_in_cell = self.model.grid.get_cell_list_contents([self.pos])

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False
            if self.model.verbose_2:
                print("*   prey_" + str(self.unique_id) + " dies at age " + str(self.age) + " of starvation")
        else:
            # creation lottery
            if self.random.random() < self.model.prey_reproduce:
                # Create a new prey:
                new_energy_mother = self.energy / 2
                new_energy_child = self.energy - new_energy_mother
                created_id = self.model.next_id()
                if self.model.verbose_3:
                    print("prey_" + str(self.unique_id) + " creates prey_" + str(created_id) +
                          " [E:" + str(round(new_energy_child, 1)) + "] at age " + str(self.age) +
                          " [E:" + str(round(self.energy, 1)) + "]=>[E:" + str(round(new_energy_mother, 1)) + "]")
                self.energy = new_energy_mother
                created_prey = Prey(
                    created_id, self.pos, self.model, self.moore, new_energy_child
                )
                self.model.grid.place_agent(created_prey, self.pos)
                self.model.schedule.add(created_prey)


class Predator(RandomWalker):
    name = "predator"

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0

    def step(self):
        if self.model.verbose_1:
            print("-----------------------------------------------------------")
            print("predator_" + str(self.unique_id) + " moves [E:" + str(round(self.energy, 1)) + "]: " + str(
                self.pos) + "=>",
                  end="")
        self.random_move()
        self.age += 1
        self.energy -= 1
        if self.model.verbose_1:
            print(str(self.pos) + " [E:" + str(round(self.energy, 1)) + "]")

        # If there are prey present, eat one at random
        agents_list_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        prey_list_in_cell = [obj for obj in agents_list_in_cell if isinstance(obj, Prey)]
        if len(prey_list_in_cell) > 0:  # if is_prey_list_in_cell
            # eat random prey
            prey_in_cell_to_eat = self.random.choice(prey_list_in_cell)

            if self.energy < self.model.max_energy_predators - prey_in_cell_to_eat.energy:
                new_energy_predator = self.energy + prey_in_cell_to_eat.energy
            else:
                new_energy_predator = self.model.max_energy_predators

            if self.model.verbose_1:
                print("predator_" + str(self.unique_id) + " eats [E:" + str(round(self.energy, 1)) + "]=>[" + str(
                    round(new_energy_predator, 1)) + "]")
                print("prey_" + str(prey_in_cell_to_eat.unique_id) + " eaten " + str(
                    prey_in_cell_to_eat.pos) + " [E:" + str(round(prey_in_cell_to_eat.energy, 1)) + "]=>", end="")

            # Kill the prey
            self.energy = new_energy_predator
            self.model.grid.remove_agent(prey_in_cell_to_eat)
            self.model.schedule.remove(prey_in_cell_to_eat)
            if self.model.verbose_1:
                print("killed and removed")
            if self.model.verbose_2:
                print("prey_" + str(prey_in_cell_to_eat.unique_id) + " dies at age " + str(prey_in_cell_to_eat.age) +
                      " of being eaten by predator_" + str(self.unique_id))

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            if self.model.verbose_2:
                print("*   predator_" + str(self.unique_id) + " dies at age " + str(self.age) + " of starvation")
        else:
            # creation lottery
            if self.random.random() < self.model.predator_reproduce:
                # Create a new predator
                new_energy_mother = self.energy / 2
                new_energy_child = self.energy - new_energy_mother
                created_id = self.model.next_id()
                if self.model.verbose_3:
                    print("predator_" + str(self.unique_id) + " creates predator_" + str(created_id) +
                          " [E:" + str(round(new_energy_child, 1)) + "] at age " + str(self.age) +
                          " [E:" + str(round(self.energy, 1)) + "]=>[E:" + str(round(new_energy_mother, 1)) + "]")
                self.energy = new_energy_mother
                created_predator = Predator(
                    created_id, self.pos, self.model, self.moore, new_energy_child
                )
                self.model.grid.place_agent(created_predator, self.pos)
                self.model.schedule.add(created_predator)
