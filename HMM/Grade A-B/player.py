#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import math
import time
import sys

epsilon = sys.float_info.epsilon  # avoid division by zero


### Utils ###


def generate_row_stochastic_matrix(n, m):
    """
    Generates a n x m matrix with random values in the range [0, 1]
    and normalizes each row to sum up to 1.
    :param n: number of rows
    :param m: number of columns
    :return: a n x m matrix
    """
    matrix = [[1 / m + random.random() / 1000 for _ in range(m)]
              for _ in range(n)]
    for row in matrix:
        row_sum = sum(row)
        for i in range(len(row)):
            row[i] /= row_sum
    return matrix


def multiply(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]


def print_list(L):
    for l in L:
        print("{:.3f}".format(l), end=" ")
        # print(l, end=" ")


def print_matrix(M):
    for row in M:
        print_list(row)
        print()
    print()


### Functions ###


def emissions_probability(A, B, pi):
    return multiply(multiply(pi, A), B)


def forward_algorithm(A, B, pi, obs):
    alpha = [[pi[0][i] * B[i][obs[0]] for i in range(len(pi[0]))]]
    for t in range(1, len(obs)):
        alpha.append([sum([alpha[t - 1][j] * A[j][i]
                           for j in range(len(A))]) * B[i][obs[t]] for i in range(len(A))])
    return sum(alpha[-1])


def viterbi(A, B, pi, obs):
    n = len(A)
    k = len(B[0])
    T = len(obs)

    delta = [[0 for _ in range(k)] for _ in range(T)]
    delta_idx = [[0 for _ in range(k)] for _ in range(T)]
    for i in range(n):
        delta[0][i] = pi[0][i] * B[i][obs[0]]

    for t in range(1, T):
        for j in range(n):
            delta[t][j] = max([delta[t - 1][i] * A[i][j]
                               for i in range(n)]) * B[j][obs[t]]
            delta_idx[t][j] = max(
                range(n), key=lambda i: delta[t - 1][i] * A[i][j])

    X = [0 for _ in range(T)]
    X[-1] = max(range(n), key=lambda i: delta[T - 1][i])
    for t in range(T - 2, -1, -1):
        X[t] = delta_idx[t + 1][X[t + 1]]
    return X


def alpha_pass(A, B, pi, obs):
    alpha = []
    scalers = []  # introduced it to avoid underflow

    alpha.append([pi[0][i] * B[i][obs[0]] for i in range(len(pi[0]))])
    scalers.append(1 / (sum(alpha[0]) + epsilon))

    alpha[0] = [alpha_0_i * scalers[0] for alpha_0_i in alpha[0]]

    for t in range(1, len(obs)):
        alpha.append([sum([alpha[t - 1][j] * A[j][i]
                           for j in range(len(A))]) * B[i][obs[t]] for i in range(len(A))])
        scalers.append(1 / (sum(alpha[t]) + epsilon))
        alpha[t] = [alpha_t_i * scalers[t] for alpha_t_i in alpha[t]]

    return alpha, scalers


def beta_pass(A, B, obs, scalers):
    beta = [[scalers[-1] for _ in range(len(A))]]
    for t in range(len(obs) - 2, -1, -1):
        beta.insert(0, [sum([beta[0][j] * A[i][j] * B[j][obs[t + 1]]
                             for j in range(len(A))]) for i in range(len(A))])
        beta[0] = [beta_0_i * scalers[t] for beta_0_i in beta[0]]
    return beta


def get_gammas(A, B, alpha, beta, obs):
    gamma = []
    di_gamma = []

    for t in range(len(obs) - 1):
        di_gamma.append([[alpha[t][i] * A[i][j] * B[j][obs[t + 1]]
                          * beta[t + 1][j] for j in range(len(A))] for i in range(len(A))])
        gamma.append([sum(di_gamma[t][i]) for i in range(len(A))])
    gamma.append(alpha[-1])
    return gamma, di_gamma


def re_estimate(A, B, pi, obs):
    alpha, scalers = alpha_pass(A, B, pi, obs)
    beta = beta_pass(A, B, obs, scalers)
    gamma, di_gamma = get_gammas(A, B, alpha, beta, obs)

    new_pi = [[gamma[0][i] for i in range(len(A))]]
    new_A = [[sum([di_gamma[t][i][j] for t in range(len(obs) - 1)])
              / (sum([gamma[t][i] for t in range(len(obs) - 1)]) + epsilon) for j in range(len(A))] for i in
             range(len(A))]
    new_B = [[sum([gamma[t][j] for t in range(len(obs)) if obs[t] == k])
              / (sum([gamma[t][j] for t in range(len(obs))]) + epsilon) for k in range(len(B[0]))] for j in
             range(len(A))]

    return new_A, new_B, new_pi, scalers


def compute_log_likelihood(scalers):
    return -sum([math.log(s) for s in scalers])


def baum_welch(A, B, pi, obs, max_iter=5):
    new_A, new_B, new_pi, scalers = re_estimate(A, B, pi, obs)
    previous_log_likelihood = float("-inf")

    iterations = 0
    while True:
        A, B, pi = new_A, new_B, new_pi
        current_log_likelihood = compute_log_likelihood(scalers)
        if previous_log_likelihood > current_log_likelihood or iterations >= max_iter:
            break
        iterations += 1
        previous_log_likelihood = current_log_likelihood
        new_A, new_B, new_pi, scalers = re_estimate(A, B, pi, obs)

    return new_A, new_B, new_pi


### Model ###


class HiddenMarkovModel:
    def __init__(self, n_states, n_emissions):
        """
        Creates a new Hidden Markov Model with n_states states and n_observations possible observations.
        :param n_states: number of states
        :param n_observations: number of possible observations
        """
        self.n_states = n_states
        self.n_observations = n_emissions
        self.PI = generate_row_stochastic_matrix(1, n_states)
        self.A = generate_row_stochastic_matrix(n_states, n_states)
        self.B = generate_row_stochastic_matrix(n_states, n_emissions)

    def __str__(self):
        return "PI: {}\nA: {}\nB: {}".format(self.PI, self.A, self.B)

    def set_A(self, A):
        self.A = A

    def set_B(self, B):
        self.B = B

    def set_PI(self, PI):
        self.PI = PI

    def update_model(self, observations):
        """
        Updates the model's parameters using the Baum-Welch algorithm.
        :param observations: a list of observations
        """
        start_time = time.time()
        self.A, self.B, self.PI = baum_welch(
            self.A, self.B, self.PI, observations, max_iter=10)
        # print("     Time to update model: {:.3f}s".format(time.time() - start_time))

    def get_most_probable_sequence(self, observations):
        """
        Returns the most probable sequence of states given a list of observations.
        :param observations: a list of observations
        :return: a list of states
        """
        return viterbi(self.A, self.B, self.PI, observations)

    def get_probability(self, observations):
        """
        Returns the probability of a sequence of observations.
        :param observations: a list of observations
        :return: a float
        """
        return forward_algorithm(self.A, self.B, self.PI, observations)

    def find_most_probable_state(self, observations):
        """
        Returns the most probable state given a list of observations.
        :param observations: a list of observations
        :return: a list of states
        """
        alpha, _ = alpha_pass(self.A, self.B, self.PI, observations)
        return max(range(len(alpha[-1])), key=lambda i: alpha[-1][i])


class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.models = [HiddenMarkovModel(
            1, N_EMISSIONS) for _ in range(
            N_SPECIES)]  # done one model by species to update them when we know the species and each one got 1 state that describe if the fish is of this species or not
        self.fishes_obs = [[] for _ in range(N_FISH)]
        self.fished_tested = [False for _ in range(N_FISH)]

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        for i in range(N_FISH):
            if not self.fished_tested[i]:
                self.fishes_obs[i].append(observations[i])

        if step < 110:  # 180 steps - 70 guesses
            return None
        else:
            best_prob = 0
            fish_type = -1

            fish_id = random.choice(
                [i for i in range(N_FISH) if not self.fished_tested[i]])

            for i, model in enumerate(self.models):
                prob = model.get_probability(
                    self.fishes_obs[fish_id])
                if prob > best_prob:
                    best_prob = prob
                    fish_type = i

            # print("     Guessing fish {} is of type {}".format(fish_id, fish_type))

            return fish_id, fish_type

    def reveal(self, correct, fish_id, true_type):
        """
        This method gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        self.fished_tested[fish_id] = True
        if not correct:
            # print("     Fish {} was of type {}".format(fish_id, true_type))
            self.models[true_type].update_model(self.fishes_obs[fish_id])
