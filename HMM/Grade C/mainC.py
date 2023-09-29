######### Utils #########

import math
import time
import numpy as np

def multiply(A, B):
    return [[sum(a*b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]


def get_output(A):
    out = ""
    out += str(len(A)) + " " + str(len(A[0])) + " "
    for row in A:
        out += " ".join(map(str, row)) + " "
    return out


def print_list(L):
    for l in L:
        print(l, end=" ")


def read_line(line_char):
    line = line_char.split()
    n = int(line.pop(0))
    k = int(line.pop(0))

    return [[float(line.pop(0)) for _ in range(k)] for _ in range(n)]


def read_obs(line_char):
    line = line_char.split()
    return [int(i) for i in line[1:]]


def read_input():
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break
    return read_obs(lines[0])

######### Exercise #########


def emissions_probability(A, B, pi):
    return multiply(multiply(pi, A), B)


def forward_algorithm(A, B, pi, obs):
    alpha = []
    alpha.append([pi[0][i] * B[i][obs[0]] for i in range(len(pi[0]))])
    for t in range(1, len(obs)):
        alpha.append([sum([alpha[t-1][j] * A[j][i]
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
            delta[t][j] = max([delta[t-1][i] * A[i][j]
                               for i in range(n)]) * B[j][obs[t]]
            delta_idx[t][j] = max(
                range(n), key=lambda i: delta[t-1][i] * A[i][j])

    X = [0 for _ in range(T)]
    X[-1] = max(range(n), key=lambda i: delta[T-1][i])
    for t in range(T-2, -1, -1):
        X[t] = delta_idx[t+1][X[t+1]]
    return X


def alpha_pass(A, B, pi, obs):
    alpha = []
    scalers = []  # introduced it to avoid underflow

    alpha.append([pi[0][i] * B[i][obs[0]] for i in range(len(pi[0]))])
    scalers.append(1/sum(alpha[0]))

    alpha[0] = [alpha_0_i * scalers[0] for alpha_0_i in alpha[0]]

    for t in range(1, len(obs)):
        alpha.append([sum([alpha[t-1][j] * A[j][i]
                     for j in range(len(A))]) * B[i][obs[t]] for i in range(len(A))])
        scalers.append(1/sum(alpha[t]))
        alpha[t] = [alpha_t_i * scalers[t] for alpha_t_i in alpha[t]]

    return alpha, scalers


def beta_pass(A, B, obs, scalers):
    beta = []
    beta.append([scalers[-1] for _ in range(len(A))])
    for t in range(len(obs)-2, -1, -1):
        beta.insert(0, [sum([beta[0][j] * A[i][j] * B[j][obs[t+1]]
                             for j in range(len(A))]) for i in range(len(A))])
        beta[0] = [beta_0_i * scalers[t] for beta_0_i in beta[0]]
    return beta


def get_gammas(A, B, alpha, beta, obs):
    gamma = []
    di_gamma = []

    for t in range(len(obs)-1):
        di_gamma.append([[alpha[t][i] * A[i][j] * B[j][obs[t+1]]
                          * beta[t+1][j] for j in range(len(A))] for i in range(len(A))])
        gamma.append([sum(di_gamma[t][i]) for i in range(len(A))])
    gamma.append(alpha[-1])
    return gamma, di_gamma


def re_estimate(A, B, pi, obs):
    alpha, scalers = alpha_pass(A, B, pi, obs)
    beta = beta_pass(A, B, obs, scalers)
    gamma, di_gamma = get_gammas(A, B, alpha, beta, obs)

    new_pi = [[gamma[0][i] for i in range(len(A))]]
    new_A = [[sum([di_gamma[t][i][j] for t in range(len(obs)-1)])
              / sum([gamma[t][i] for t in range(len(obs)-1)]) for j in range(len(A))] for i in range(len(A))]
    new_B = [[sum([gamma[t][j] for t in range(len(obs)) if obs[t] == k])
              / sum([gamma[t][j] for t in range(len(obs))]) for k in range(len(B[0]))] for j in range(len(A))]

    return new_A, new_B, new_pi, scalers


def compute_log_likelihood(scalers):
    return -sum([math.log(s) for s in scalers])


def baum_welch(A, B, pi, obs, max_time=0.8):
    new_A, new_B, new_pi, scalers = re_estimate(A, B, pi, obs)
    previous_log_likelihood = float("-inf")

    start_time = time.time()
    iterations = 0
    while True:
        A, B, pi = new_A, new_B, new_pi
        current_log_likelihood = compute_log_likelihood(scalers)
        if previous_log_likelihood > current_log_likelihood or time.time() - start_time > max_time:
            print(time.time() - start_time > max_time)
            break

        previous_log_likelihood = current_log_likelihood
        new_A, new_B, new_pi, scalers = re_estimate(A, B, pi, obs)

    return new_A, new_B, new_pi

######### Main #########


def main():
    # Read data
    A = [[0.54, 0.26, 0.20], [0.19, 0.53, 0.28], [0.22, 0.18, 0.6]]
    B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27], [0.19, 0.21, 0.15, 0.45]]
    pi = [[0.3, 0.2, 0.5]]

    obs = read_input()

    A_ini = np.random.rand(3, 3)
    A_ini /= A_ini.sum(axis=1)
    B_ini = np.random.rand(3, 4)
    B_ini[0] /= B_ini.sum(axis=1)[0]
    B_ini[1] /= B_ini.sum(axis=1)[1]
    B_ini[2] /= B_ini.sum(axis=1)[2]
    pi_ini = np.random.rand(1, 3)
    pi_ini /= pi_ini.sum(axis=1)


    #for i in range(100,1000,100):
    #    obs_red = obs[:i]
    #    new_A, new_B, new_pi = baum_welch(A, B, pi, obs_red)
    #    print(get_output(new_A))
    #    print(get_output(new_B))
    #    print("number of observations: ", i,"\n")

    new_A, new_B, new_pi = baum_welch(A_ini, B_ini, pi_ini, obs)

    print(get_output(new_A))
    print(get_output(new_B))
    print(get_output(new_pi))
    

if __name__ == "__main__":
    main()
