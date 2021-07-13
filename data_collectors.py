# data_collectors.py

def get_sum_getter(state):
    def get_sum(model):
        return sum(model.summary[state])
    return get_sum

def get_state_getter(state):
    def get_state(model):
        return model.summary[state]
    return get_state