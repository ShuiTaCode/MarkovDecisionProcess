# This is a sample Python script.
import numpy as np


class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y


size = 4


def create_set_of_states(size_of_set):
    result = []
    for i in range(size - 1):
        for j in range(size - 1):
            result.append(State(i, j, ))
    return result




init_set_of_states = create_set_of_states(3)
init_set_of_actions = ['up', 'down', 'left', 'right']


def delta_x(state1, state2):
    return np.abs(state1.x - state2.x)


def delta_y(state1, state2):
    return np.abs(state1.y - state2.y)
def create_set_of_transitions(set_of_states, set_of_actions):
    result = []
    for state in set_of_states:
        for action in set_of_actions:
            for succ_state in set_of_actions:
                result.append({'s': state, 'a': action, 's_succ': succ_state})

    filtered_result = [triple for triple in result if  (delta_x(triple['s'], triple['s_succ']) > 1 or delta_y(triple['s'], triple['s_succ'])) > 1 or (
                delta_x(triple['s'], triple['s_succ']) == 1 or delta_y(triple['s'], triple['s_succ']) == 1)]

    return filtered_result


def calculate_prob(transition):
    left_border = transition.s.x == 0
    right_border = transition.s.x == size - 1
    top_border = transition.s.y = 0
    bottom_border = transition.s.y = size - 1

    if transition.a == init_set_of_actions[0]: #up
        if top_border:
            return 0.8
        else


def create_transition_probability(set_of_transitions):
    result = []
    for triple in set_of_transitions:
        if delta_x(triple.s, triple.s_succ) > 1 or delta_y(triple.s, triple.s_succ) > 1 or (
                delta_x(triple.s, triple.s_succ) == 1 or delta_y(triple.s, triple.s_succ) == 1):
            result.append({'t': triple, 'p': 0})
        else:
            result.append({'t': triple, 'p': calculate_prob(triple)})
    return result


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


initialStateDistribution = [0.1, 0.05, 0.05, 0.2, 0.4, 0.2]
initialStateId = np.random.choice(initialStateDistribution, initialStateDistribution).id


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
