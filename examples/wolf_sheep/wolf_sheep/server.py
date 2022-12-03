import mesa

from wolf_sheep.agents import Wolf, Sheep, GrassPatch
from wolf_sheep.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Wolf:
        # agent shape
        portrayal["Shape"] = "circle" # "wolf_sheep/resources/wolf.png"
        portrayal["r"] = 0.5
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"

        # tooltip
        portrayal["type"] = "Predator"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        portrayal["text_color"] = "White"
        portrayal["Layer"] = 1

    elif type(agent) is Sheep:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"


        portrayal["type"] = "Prey"
        portrayal["id"] = agent.unique_id
        portrayal["age"] = agent.age
        portrayal["energy"] = round(agent.energy, 2)
        # portrayal["scale"] = 0.9
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


canvas_element = mesa.visualization.CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Sheep", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00AA00"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": mesa.visualization.Slider(
        "Initial Sheep Population", 100, 10, 300
    ),
    "sheep_reproduce": mesa.visualization.Slider(
        "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 50, 10, 300),
    "wolf_reproduce": mesa.visualization.Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": mesa.visualization.Slider(
        "Wolf Gain From Food Rate", 20, 1, 50
    ),
    "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    WolfSheep, [canvas_element, chart_element], "Wolf Sheep Predation", model_params
)
server.port = 8521
