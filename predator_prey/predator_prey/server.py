import mesa

from predator_prey.agents import Predator, Prey, GrassPatch
from predator_prey.model import PredatorPrey

#
initial_prey = 10
initial_wolves = 5
grid_with = 10
grid_height = 10


def predator_prey_portrayal(agent):
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

        # tooltip content Predator
        portrayal["type"] = "Predator"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["text_color"] = "White"
        portrayal["pos"] = str(agent.pos)
        portrayal["Layer"] = 1

    elif type(agent) is Prey:
        # agent layout
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"

        # tooltip content Prey
        portrayal["type"] = "Prey"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["pos"] = str(agent.pos)
        portrayal["Layer"] = 1



    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(predator_prey_portrayal, grid_with, grid_height, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Predators", "Color": "#AA0000"},
        {"Label": "Prey", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00AA00"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "initial_wolves": mesa.visualization.Slider("Initial predator Population", initial_wolves, 0, 300),
    "initial_prey": mesa.visualization.Slider(
        "Initial prey Population", initial_prey, 0, 300
    ),
    "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),

    "prey_reproduce": mesa.visualization.Slider(
        "prey Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "predator_reproduce": mesa.visualization.Slider(
        "predator Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which predator agents reproduce.",
    ),
    "predator_gain_from_food": mesa.visualization.Slider(
        "Predator Gain From Food Rate", 20, 1, 50
    ),
    "prey_gain_from_food": mesa.visualization.Slider("Prey Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    PredatorPrey, [canvas_element, chart_element], "Predator Prey Model", model_params
)
server.port = 8521
