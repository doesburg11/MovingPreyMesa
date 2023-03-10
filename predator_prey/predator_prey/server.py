import mesa

from predator_prey.agents import Predator, Prey
from predator_prey.model import PredatorPrey


def predator_prey_portrayal(agent):

    def agent_id(_agent):
        if _agent.model.n_grid_cells_width * _agent.model.n_grid_cells_height > 100:
            return ""
        else:
            return agent.unique_id

    if agent is None:
        return

    portrayal = {}

    if type(agent) is Predator:
        # agent layout
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.8
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
        portrayal["text"] = agent.unique_id if PredatorPrey.n_grid_cells_height*PredatorPrey.n_grid_cells_width<100 else ""
        portrayal["text_color"] = "black"

        # tooltip content Predator
        portrayal["type"] = "Predator"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["pos"] = str(agent.pos)
        portrayal["Layer"] = 1

    elif type(agent) is Prey:
        # agent layout
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
        portrayal["text"] = agent.unique_id if PredatorPrey.n_grid_cells_height*PredatorPrey.n_grid_cells_width<100 else ""
        portrayal["text_color"] = "black"

        # tooltip content Prey
        portrayal["type"] = "Prey"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["pos"] = str(agent.pos)
        portrayal["Layer"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    predator_prey_portrayal,
    PredatorPrey.n_grid_cells_width,
    PredatorPrey.n_grid_cells_height,
    PredatorPrey.canvas_width,
    PredatorPrey.canvas_height)

chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Predators", "Color": "#AA0000"},
        {"Label": "Prey", "Color": "#0000FF"},
    ]
)

chart_element1 = mesa.visualization.ChartModule(
    [
        {"Label": "Predators_energy", "Color": "#AA0000"},
        {"Label": "Prey_energy", "Color": "#0000FF"},

    ]
)

model_params = {
    "title": mesa.visualization.StaticText(
        "Parameters:"
    ),  # StaticText.
    "initial_predators": mesa.visualization.Slider(
        "Initial predator Population",
        PredatorPrey.initial_predators,
        0,
        20
    ),
    "initial_prey": mesa.visualization.Slider(
        "Initial Prey Population",
        PredatorPrey.initial_prey,
        0,
        20
    ),

    "prey_reproduce": mesa.visualization.Slider(
        "Prey Reproduction Rate",
        PredatorPrey.prey_reproduce,
        0.0,
        0.1,
        0.005
    ),
    "predator_reproduce": mesa.visualization.Slider(
        "Predator Reproduction Rate",
        PredatorPrey.predator_reproduce,
        0.0,
        0.1,
        0.005,
        description="The rate at which predator agents reproduce.",
    ),
    "initial_energy_predators": mesa.visualization.Slider(
        "Energy Predators at Start",
        PredatorPrey.initial_energy_predators,
        0.0,
        50.0,
        0.1,
        description="Energy a predator inherits by initialization of model"
    ),
    "initial_energy_prey": mesa.visualization.Slider(
        "Energy Prey at Start",
        PredatorPrey.initial_energy_prey,
        0.0,
        50.0,
        0.1,
        description="Energy a prey inherits by initialization of model"
    ),

}

server = mesa.visualization.ModularServer(
    PredatorPrey,
    [canvas_element, chart_element, chart_element1],
    "Moving Prey Model",
    model_params
)
server.port = 8521
