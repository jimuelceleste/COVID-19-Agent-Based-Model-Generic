# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from data_collectors import *
from agents import *
import random

class Covid19Model(Model):

    def __init__(self, variable_params, fixed_params):
        self.steps = 0
        self.running = True
        self.grid = MultiGrid(50, 50, True)
        self.schedule = RandomActivation(self)
        self.summary = variable_params
        self.transmission_rate = fixed_params["transmission_rate"]
        self.incubation_rate = fixed_params["incubation_rate"]
        self.death_rate = fixed_params["death_rate"]
        self.recovery_rate = fixed_params["recovery_rate"]
        self.average_incubation_period = fixed_params["average_incubation_period"],
        self.average_infectious_period = fixed_params["average_infectious_period"]
        self.wearing_mask = fixed_params["wearing_mask"]
        self.wearing_mask_protection = fixed_params["wearing_mask_protection"]
        self.social_distancing = fixed_params["social_distancing"]
        self.social_distancing_protection = fixed_params["social_distancing_protection"]
        self.handwashing = fixed_params["handwashing"]
        self.handwashing_protection = fixed_params["handwashing_protection"]
        self.min_age_restriction = fixed_params["min_age_restriction"]
        self.max_age_restriction = fixed_params["max_age_restriction"]
        self.agent_movement_range = fixed_params["agent_movement_range"] # grids

        # Instantiating PersonAgent objects
        age_group_size = 5
        age_group_range = lambda x: (x * age_group_size, (x + 1) * age_group_size - 1)
        for state in self.summary:
            for age_group, count in enumerate(self.summary[state]):
                for i in range(count):
                    unique_id = state + str(age_group) + str(i)
                    min_age, max_age = age_group_range(age_group)
                    age = random.randint(min_age, max_age)
                    # days_infected = random.randint(0, self.average_infectious_period) if state == "I" else 0
                    # days_incubating = random.randint(0, self.average_incubation_period) if state == "E" else 0
                    days_infected = 0
                    days_incubating = 0

                    a = PersonAgent(unique_id,
                        self,
                        state,
                        age,
                        age_group,
                        days_infected,
                        days_incubating)
                    self.schedule.add(a)
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    self.grid.place_agent(a, (x, y))

        self.data_collector = DataCollector(
            model_reporters={
                "S": get_sum_getter("S"),
                "E": get_sum_getter("E"),
                "I": get_sum_getter("I"),
                "D": get_sum_getter("D"),
                "R": get_sum_getter("R")})

    def step(self):
        """
        Advances the model by one step
        """
        # print(self.SEIR)
        self.steps += 1
        self.schedule.step()
        self.data_collector.collect(self)
