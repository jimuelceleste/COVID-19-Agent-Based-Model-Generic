import pandas as pd
import numpy as np
import json

class DOHCovid19DataExtractor:

    def __init__(self, filename):
        # Opens the COVID19 Data file as a Pandas DataFrame
        self.data = pd.read_csv(filename, index_col=0)
        self.filename = filename

    def count_city_data(self, city, age_stratified=True):
        # Initializes the return variable: count
        #  I = infectious, R = recovered, D = died
        count = {"I": [], "R": [], "D": []}

        # Filters the COVID19 data with the CityMunRes column
        data = self.data[self.data['CityMunRes']==city]

        # Generates the age groups; size = 5
        age_groups = self.generate_age_groups(5, 16)
        age_groups.append((80,100)) # Special case: 80 and above

        for min_age, max_age in age_groups:
            # Filters the data with the Age column
            # Age of case must be within the min and max age
            age_group_data = data[data["Age"].between(min_age, max_age, inclusive=True)]

            # Counts the number of recovered, dead, and active
            recovered = len(age_group_data[age_group_data["HealthStatus"]=="RECOVERED"].index)
            dead = len(age_group_data[age_group_data["HealthStatus"]=="DIED"].index)
            active = len(age_group_data.index) - recovered - dead

            # Saves the counts to the return variable
            count["I"].append(active)
            count["R"].append(recovered)
            count["D"].append(dead)

        # Gets the sum of the age_stratified values when the age_stratified parameter is False
        if not age_stratified:
            for key in count: count[key] = sum(count[key])

        return count

    def generate_age_groups(self, size, groups):
        age_range = lambda x: (x * size, (x + 1) * size - 1)
        return [age_range(i) for i in range(groups)]

    def death_rate_city(self, city):
        cases = self.count_city_data(city)
        dead = cases["D"]
        removed = sum(dead) + sum(cases["R"])
        death_rate = [i/removed for i in dead]
        return death_rate

    def recovery_rate_city(self, city):
        cases = self.count_city_data(city)
        recovered = cases["R"]
        removed = sum(recovered) + sum(cases["D"])
        recovery_rate = [i/removed for i in recovered]
        return recovery_rate

    def removal_rate_city(self, city):
        death_rate = self.death_rate_city(city)
        recovery_rate = self.recovery_rate_city(city)
        removal_rate = [death_rate[i] + recovery_rate[i] for i in range(len(death_rate))]
        return {
            "death_rate": death_rate,
            "recovery_rate": recovery_rate,
            "removal_rate": removal_rate
        }

    def case_age_distribution_city(self, city):
        data = self.data[self.data["CityMunRes"]==city]
        age_distribution = []

        age_groups = self.generate_age_groups(5, 16)
        age_groups.append((80,100)) # Special case: 80 and above

        for min_age, max_age in age_groups:
            # Filters the data with the Age column
            # Age of case must be within the min and max age
            age_group_data = data[data["Age"].between(min_age, max_age, inclusive=True)]
            age_distribution.append(len(age_group_data.index))

        return [i / sum(age_distribution) for i in age_distribution]

# Please download the latest file from the DOH COVID19 Tracker
# URL [Instruction for download]: https://doh.gov.ph/covid19tracker
# URL [COVID19 File itself as of 07/07]: https://drive.google.com/drive/folders/1DqPLa6bFPZ6lQmZD0RyJl9X8XhMLX2uF
# Note: Download the "Case Information" file
filename = "DOH COVID Data Drop_ 20210707 - 04 Case Information.csv"
extractor = DOHCovid19DataExtractor(filename)
#
# # Cases in Pasig City
# pasig_city_data = extractor.count_city_data("CITY OF PASIG")
# print(pasig_city_data)
# # Saves count as a json file
# # with open("pasig_cases.json", "w") as file:
# #     json.dump(pasig_city_data, file, indent=4)
#
# pasig_removal_rate = extractor.removal_rate_city("CITY OF PASIG")
# print(pasig_removal_rate)
# with open("pasig_removal_rate.json", "w") as file:
#     json.dump(pasig_removal_rate, file, indent=4)

case_age_distribution = extractor.case_age_distribution_city("CITY OF PASIG")
print(case_age_distribution)
with open("pasig_case_age_distribution.json", "w") as file:
    json.dump(case_age_distribution, file, indent=4)