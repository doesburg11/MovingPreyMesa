import mesa
from predator_prey.random_walk import RandomWalker


class Prey(RandomWalker):
    """
    A prey that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0
        self.life_span: integer = None

    def step(self):
        """
        A model step. Moves, ages, then eat grass and reproduce.
        """
        print("prey_" + str(self.unique_id)+": "+str(self.pos)+"=>", end="")
        self.random_move()
        print(self.pos)
        self.age += 1
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.prey_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False
                print("*   prey_"+str(self.unique_id)+" dies at age "+str(self.age)+" of starvation")

        if living and self.random.random() < self.model.prey_reproduce:
            # Create a new prey:
            if self.model.grass:
                self.energy /= 2
            lamb = Prey(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)
            print("*   prey_"+str(self.unique_id)+" creates at age "+str(self.age)+" new predator at "+str(self.pos))


class Predator(RandomWalker):
    """
    A predator that walks around, reproduces (asexually) and eats prey.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0
        self.life_span: integer = None

    def step(self):
        print("predator_" + str(self.unique_id)+": "+str(self.pos)+"=>", end="")
        self.random_move()
        print(self.pos)
        self.age += 1
        self.energy -= 1

        # If there are prey present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        prey = [obj for obj in this_cell if isinstance(obj, Prey)]
        if len(prey) > 0:
            # eat random prey
            #TODO: eat prey with most energy or weakest prey if prey can resist?
            prey_to_eat = self.random.choice(prey)
            self.energy += self.model.predator_gain_from_food

            # Kill the prey
            prey_to_eat.death_age = prey_to_eat.age #TODO: add death_age to record for prey
            self.model.grid.remove_agent(prey_to_eat)
            self.model.schedule.remove(prey_to_eat)
            print("*   prey_"+str(prey_to_eat.unique_id)+" dies at age "+str(prey_to_eat.age)+
                  " of being eaten by predator_"+str(self.unique_id))


        # Death or reproduction
        if self.energy < 0:
            self.death_age = self.age
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            print("*   predator_"+str(self.unique_id)+" dies at age "+str(self.age)+" of starvation")
        else:
            if self.random.random() < self.model.predator_reproduce:
                # Create a new predator cub
                self.energy /= 2
                cub = Predator(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
                print("*predator_"+str(self.unique_id)+" creates at age "+str(self.age)+" new predator at "+str(self.pos))


class GrassPatch(mesa.Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by prey
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos
        self.age = 0

    def step(self):
        # print("grass_" + str(self.unique_id))
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
