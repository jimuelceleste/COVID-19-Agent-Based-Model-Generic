# data_collectors.py

def get_sum_getter(state):
    def get_sum(model):
        return sum(model.summary[state])
    return get_sum