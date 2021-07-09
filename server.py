from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model import *
import json

colors = {"S": "green",
    "E": "orange",
    "I": "red",
    "R": "violet",
    "D": "grey",
    "V": "blue"}
layers = {"S": 0, "E": 1, "I": 2, "R": 3, "D": 4, "V": 5}
r = {"S": 0.9, "E": 0.8, "I": 0.7, "R": 0.6, "D": 0.5, "V": 0.4}

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Color": colors[agent.state],
        "Layer": layers[agent.state],
        "r": r[agent.state]
    }
    return portrayal

def parse_json(filename):
    content = {}
    with open(filename) as file:
        content = json.load(file)
    return content

grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
series = [{"Label": "S", "Color": "Green"},
    {"Label": "E", "Color": "Yellow"},
    {"Label": "I", "Color": "Red"},
    {"Label": "D", "Color": "Grey"},
    {"Label": "R", "Color": "Blue"}]
chart = ChartModule(series, 125, 300, "data_collector")
server = ModularServer(Covid19Model,
    [grid, chart],
    "Covid-19 Model",
    {
        "variable_params": parse_json("variable_params.json"),
        "fixed_params": parse_json("fixed_params.json")
    })
server.port = 8521 # default
server.launch()