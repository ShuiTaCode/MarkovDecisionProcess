# This is a sample Python script.
import numpy as np


class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Transition:
    def __init__(self, state, action, state_succ):
        self.s = state
        self.a = action
        self.s_succ = state_succ

    def get_state(self):
        return self.s

    def get_action(self):
        return self.a

    def get_succ_state(self):
        return self.s_succ


size = 3


def create_set_of_states(size_of_set):
    result = []
    for i in range(size_of_set):
        for j in range(size_of_set):
            result.append(State(i, j))
    return result


init_set_of_states = create_set_of_states(size)
init_set_of_actions = ['up', 'down', 'left', 'right']


def delta_x(state1, state2):
    return np.abs(state1.get_x() - state2.get_x())


def delta_y(state1, state2):
    return np.abs(state1.get_y() - state2.get_y())


def create_set_of_transitions(set_of_states, set_of_actions):
    result = []
    for state in set_of_states:
        for action in set_of_actions:
            for succ_state in set_of_states:
                result.append(Transition(state, action, succ_state))

    filtered_result = []
    for t in result:
        if ((delta_x(t.get_state(), t.get_succ_state()) <= 1) and (
                delta_y(t.get_state(), t.get_succ_state()) <= 1) and not
        (delta_x(t.get_state(), t.get_succ_state()) == 1 and (delta_y(t.get_state(), t.get_succ_state()) == 1))):
            filtered_result.append(t)

    for t in filtered_result:
        print(t.get_state().__dict__, t.get_action(), t.get_succ_state().__dict__, 'dx',
              delta_x(t.get_state(), t.get_succ_state()), 'dy', delta_y(t.get_state(), t.get_succ_state()))

    return filtered_result


init_set_of_transitions = create_set_of_transitions(init_set_of_states, init_set_of_actions)


def calculate_prob(transition):
    left_border = transition.s.x == 0
    right_border = transition.s.x == size - 1
    top_border = transition.s.y == 0
    bottom_border = transition.s.y == size - 1

    if transition.a == init_set_of_actions[0]:  # action = up
        if transition.s_succ == transition.s:  # stay
            p = 0.05
            if top_border:
                p += 0.80
            if bottom_border:
                p += 0.05
            if left_border or right_border:
                p += 0.050
            return p
        if transition.s_succ.x == transition.s.x + 1:  # moving right
            return 0.05
        if transition.s_succ.x == transition.s.x - 1:  # moving left
            return 0.05
        if transition.s_succ.y == transition.s.y - 1:  # moving up
            return 0.80
        if transition.s_succ.y == transition.s.y + 1:  # moving down
            return 0.05

    if transition.a == init_set_of_actions[1]:  # down
        if transition.s_succ == transition.s:
            p = 0.05
            if bottom_border:
                p += 0.80
            if top_border:
                p += 0.05
            if left_border or right_border:
                p += 0.05
            return p
        if transition.s_succ.x == transition.s.x + 1:  # moving right
            return 0.05
        if transition.s_succ.x == transition.s.x - 1:  # moving left
            return 0.05
        if transition.s_succ.y == transition.s.y - 1:  # moving up
            return 0.05
        if transition.s_succ.y == transition.s.y + 1:  # moving down
            return 0.80

    if transition.a == init_set_of_actions[2]:  # left
        if transition.s_succ == transition.s:
            p = 0.05
            if left_border:
                p += 0.80
            if right_border:
                p += 0.05
            if top_border or bottom_border:
                p += 0.05
            return p
        if transition.s_succ.x == transition.s.x + 1:  # moving right
            return 0.05
        if transition.s_succ.x == transition.s.x - 1:  # moving left
            return 0.80
        if transition.s_succ.y == transition.s.y - 1:  # moving up
            return 0.05
        if transition.s_succ.y == transition.s.y + 1:  # moving down
            return 0.05

    if transition.a == init_set_of_actions[3]:  # right
        if transition.s_succ == transition.s:
            p = 0.05
            if right_border:
                p += 0.80
            if left_border:
                p += 0.05
            if top_border or bottom_border:
                p += 0.05
            return p
        if transition.s_succ.x == transition.s.x + 1:  # moving right
            return 0.80
        if transition.s_succ.x == transition.s.x - 1:  # moving left
            return 0.05
        if transition.s_succ.y == transition.s.y - 1:  # moving up
            return 0.05
        if transition.s_succ.y == transition.s.y + 1:  # moving down
            return 0.05


def create_transition_probability(set_of_transitions):
    result = []
    for t in set_of_transitions:
        print(t.get_state().__dict__, t.get_action(), t.get_succ_state().__dict__, round(calculate_prob(t), 2))
        # result.append({'t': triple, 'p': calculate_prob(triple)})
    return result


init_set_of_transitions_probabilities = create_transition_probability(init_set_of_transitions)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# initialStateDistribution = [0.1, 0.05, 0.05, 0.2, 0.4, 0.2]
# initialStateId = np.random.choice(init_set_of_states).id


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    print(init_set_of_transitions_probabilities)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
