from model import *
import json
import pickle
from progress.spinner import Spinner
from progress.bar import Bar
import copy

def batchrun(iterations, steps, simulation_id, variable_params, fixed_params, contact_matrix):
    for i in range(iterations):
        print("Iteration: %i/%i" % ((i+1), iterations))

        model = Covid19Model(copy.deepcopy(variable_params), fixed_params, contact_matrix)

        progress = Bar("Running model", max=steps)
        for j in range(steps):
            model.step()
            progress.next()
        progress.finish()

        output = {
            "seirdv_total_time_series": model.data_collector_total.get_model_vars_dataframe(),
            "seirdv_age_time_series": model.data_collector_age.get_model_vars_dataframe(),
            "seirdv_total_final": model.total
        }

        output_filename = "output/sim_%s_iter_%i.pkl" % (simulation_id, i)
        with open(output_filename, "wb") as output_file:
            pickle.dump(output, output_file, -1) # -1 specifies highest binary protocol
            print("File saved: %s" % (output_filename))

        del output
        del model

    print("Batch run finished.")

def parse_json(filename):
    content = {}
    with open(filename) as file:
        content = json.load(file)
    return content

iterations = 10
steps = 100
fixed_params = parse_json("fixed_params.json")
variable_params = parse_json("variable_params.json")
contact_matrix_100 = parse_json("contact_matrix_100_1.json")
contact_matrix_50 = parse_json("contact_matrix_50_1.json")

# batchrun(iterations, steps, "100schoolwork", variable_params, fixed_params, contact_matrix_100)
batchrun(iterations, steps, "50schoolwork", variable_params, fixed_params, contact_matrix_50)