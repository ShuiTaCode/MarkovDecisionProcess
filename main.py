import numpy as np
from tkinter import *
from numpy import random
from numpy.random import normal
from numpy import mean
from numpy import std
from scipy.stats import norm


class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = False
        self.end = False
        self.penalty = False
        self.value = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_start(self):
        return self.start

    def set_start(self, start):
        self.start = start

    def get_end(self):
        return self.end

    def set_end(self, end):
        self.end = end

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = round(value, 2)

    def set_penalty(self, penalty):
        self.penalty = penalty

    def get_penalty(self):
        return self.penalty


class Transition:
    def __init__(self, state, action, state_succ):
        self.s = state
        self.a = action
        self.s_succ = state_succ
        self.prob = 0
        self.reward = 0

    def get_state(self):
        return self.s

    def get_action(self):
        return self.a

    def get_succ_state(self):
        return self.s_succ

    def set_prob(self, prob):
        self.prob = prob

    def set_reward(self, reward):
        self.reward = reward

    def get_prob(self):
        return self.prob

    def get_reward(self):
        return self.reward


def create_set_of_states(size_of_set):
    result = []
    for i in range(size_of_set):
        for j in range(size_of_set):
            result.append(State(i, j))
    return result


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

    return filtered_result


def calculate_prob(transition, set_of_actions):
    left_border = transition.s.x == 0
    right_border = transition.s.x == size - 1
    top_border = transition.s.y == 0
    bottom_border = transition.s.y == size - 1

    if transition.a == 'exit':
        if transition.s == end_state:
            return 1
        elif transition.s == penalty_state:
            return 1
        else:
            return 0

    if transition.a == set_of_actions[0]:  # action = up
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

    if transition.a == set_of_actions[1]:  # down
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

    if transition.a == set_of_actions[2]:  # left
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

    if transition.a == set_of_actions[3]:  # right
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


def create_transition_probability(set_of_transitions, set_of_actions):
    result = []
    for t in set_of_transitions:
        t.set_prob(round(calculate_prob(t, set_of_actions), 2))
        result.append(t)

    return result


def create_transition_reward(set_of_transitions_probs):
    result = []
    print('länge', len(set_of_transitions_probs))
    for t in set_of_transitions_probs:
        if t.get_action() == 'exit':
            if t.get_state() == end_state:
                t.set_reward(1)
            elif t.get_state() == penalty_state:
                t.set_reward(-1)
        print('probs', t.get_state().__dict__, t.get_action(), t.get_succ_state().__dict__, t.get_prob(),
              t.get_reward())
        result.append(t)

    return result


def create_random_initial_state_distribution(set_of_states):
    sample = normal(loc=50, scale=5, size=len(set_of_states))
    sample_mean = mean(sample)
    sample_std = std(sample)
    print('Mean=%.3f, Standard Deviation=%.3f' % (sample_mean, sample_std))
    dist = norm(1, sample_std)
    probabilities = [dist.pdf(value) for value in sample]
    return probabilities


# calculate parameters

# define the distribution

# sample probabilities for a range of outcomes


size = 5
init_set_of_states = create_set_of_states(size)
# initial_distribution_of_states = create_random_initial_state_distribution(init_set_of_states)
initial_state = random.choice(init_set_of_states)
initial_state.set_start(True)
end_state = random.choice([state for state in init_set_of_states if
                           (state != initial_state)])
end_state.set_end(True)
penalty_state = random.choice([state for state in init_set_of_states if
                               (state != initial_state and state != end_state)])

penalty_state.set_penalty(True)
# end_state.set_value(1)
print(initial_state)
init_set_of_actions = ['up', 'down', 'left', 'right']
init_set_of_transitions = create_set_of_transitions(init_set_of_states, init_set_of_actions)
init_set_of_transitions.append(Transition(end_state, 'exit', State(9, 9)))
init_set_of_transitions.append(Transition(penalty_state, 'exit', State(9, 9)))
init_set_of_transitions_probabilities = create_transition_probability(init_set_of_transitions, init_set_of_actions)
init_set_of_transitions_probabilities_and_rewards = create_transition_reward(init_set_of_transitions_probabilities)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# initialStateDistribution = [0.1, 0.05, 0.05, 0.2, 0.4, 0.2]
# initialStateId = np.random.choice(init_set_of_states).id
def draw_square(c, x, y, w, h, color):
    c.create_line(x, y, x + w, y, fill=color, width=3)
    c.create_line(x + w, y, x + w, y + h, fill=color, width=3)
    c.create_line(x + w, y + h, x, y + h, fill=color, width=3)
    c.create_line(x, y + h, x, y, fill=color, width=3)


def draw_graph(c, x, y, scale):
    temp_init_state = {}
    temp_end_state = {}
    for s in init_set_of_states:
        if s.get_start():
            temp_init_state = s
        elif s.get_end():
            temp_end_state = s
        else:
            draw_square(c, x + s.x * scale, y + s.y * scale, scale, scale, 'black')
            c.create_text(x + s.x * scale + scale / 2, y + s.y * scale + scale / 2, text=s.get_value(), anchor='nw',
                          font='TkMenuFont', fill='black')

    draw_square(c, x + temp_init_state.x * scale, y + temp_init_state.y * scale, scale, scale, 'blue')
    c.create_text(x + temp_init_state.x * scale, y + temp_init_state.y * scale, text='Start', anchor='nw',
                  font='TkMenuFont', fill='blue')
    draw_square(c, x + penalty_state.x * scale, y + penalty_state.y * scale, scale, scale, 'red')
    draw_square(c, x + temp_end_state.x * scale, y + temp_end_state.y * scale, scale, scale, 'green')
    c.create_text(x + temp_end_state.x * scale, y + temp_end_state.y * scale, text='End ', anchor='nw',
                  font='TkMenuFont', fill='green')
    c.create_text(x + temp_end_state.x * scale + scale / 2, y + temp_end_state.y * scale + scale / 2,
                  text=temp_end_state.get_value(), anchor='nw',
                  font='TkMenuFont', fill='black')


def run_iteration(set_transitions_probs, set_of_states, gamma, c):
    print('iteration wird ausgeführt')
    result = []
    for state in [s for s in set_of_states]:
        arr = []
        for tr in [t for t in set_transitions_probs if
                   (t.get_state() == state)]:
            # arr.append(tr.get_prob() * ( gamma*tr.get_succ_state().get_value()))
            if tr.get_succ_state() == penalty_state:
                print('penalty state gefunden', tr.get_state().get_x(), tr.get_state().get_y(), tr.get_action(),
                      tr.get_prob(), tr.get_reward(),
                      tr.get_prob() * (tr.get_reward() + gamma * tr.get_succ_state().get_value()))

            arr.append(tr.get_prob() * (tr.get_reward() + gamma * tr.get_succ_state().get_value()))
        result.append(max(arr))

    for x in range(len(set_of_states)):
        set_of_states[x].set_value(result[x])

    c.delete('all')
    draw_graph(c, 100, 100, 100)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    top = Tk()
    top.geometry("1024x960")
    # creating a simple canvas
    c = Canvas(top, bg="white", height="960", width="1024")
    b1 = Button(top, text="Increment Iteration",
                command=lambda: run_iteration(init_set_of_transitions_probabilities_and_rewards, init_set_of_states,
                                              0.9, c),
                activeforeground="red", activebackground="pink", pady=10)

    b1.pack(side=TOP)

    draw_graph(c, 100, 100, 100)
    c.pack()
    top.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
