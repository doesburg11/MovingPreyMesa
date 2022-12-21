import mesa

from predator_prey.agents import Predator, Prey, GrassPatch
from predator_prey.model import PredatorPrey

grid_with = 5
grid_height = 5
initial_prey = 5
initial_predators = 3


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
        portrayal["text"] = agent.unique_id
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
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "black"

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
        portrayal["w"] = 1
        portrayal["h"] = 1

        # tooltip content Prey
        portrayal["type"] = "Grass"
        portrayal["id"] = agent.unique_id
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["regrowth rate"] = round(agent.regrowth_rate, 2)
        portrayal["Layer"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    predator_prey_portrayal,
    grid_with,
    grid_height,
    500,
    500)

chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Predators", "Color": "#AA0000"},
        {"Label": "Prey", "Color": "#666666"},
        {"Label": "GrassPatches", "Color": "#00AA00"},
    ]
)

chart_element1 = mesa.visualization.ChartModule(
    [
        {"Label": "Predators_energy", "Color": "#AA0000"},
        {"Label": "Prey_energy", "Color": "#0000FF"},
        {"Label": "GrassPatch_energy", "Color": "#00AA00"},

    ]
)

chart_element2 = mesa.visualization.ChartModule(
    [
        {"Label": "Prey_energy", "Color": "#0000FF"},
    ]
)

chart_element3 = mesa.visualization.ChartModule(
    [
        {"Label": "GrassPatch_energy", "Color": "#00AA00"},
    ]
)

model_params = {
    "title": mesa.visualization.StaticText(
        "Parameters:"
    ),  # StaticText.
    "initial_predators": mesa.visualization.Slider(
        "Initial predator Population",
        initial_predators,
        0,
        300
    ),
    "initial_prey": mesa.visualization.Slider(
        "Initial prey Population",
        initial_prey,
        0,
        300
    ),

    "prey_reproduce": mesa.visualization.Slider(
        "prey Reproduction Rate",
        0.04,
        0.01,
        1.0,
        0.01
    ),
    "predator_reproduce": mesa.visualization.Slider(
        "predator Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which predator agents reproduce.",
    ),
    "grass_regrowth_rate": mesa.visualization.Slider(
        "Grass Regrowth Rate",
        1.0,
        0.1,
        5.0,
        0.1,
        description="Energy increase of a GrassPatch per step due to regrowth"
    ),
}

server = mesa.visualization.ModularServer(
    PredatorPrey,
    [canvas_element, chart_element, chart_element1],
    "Predator Prey Model",
    model_params
)
server.port = 8521
