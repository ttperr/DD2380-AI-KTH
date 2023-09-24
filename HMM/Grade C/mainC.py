######### Utils #########

def multiply(A, B):
    if hasattr(A[0], "__len__") or hasattr(B[0], "__len__"):
        return [[sum(a*b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
    else:
        return [sum(a*b for a, b in zip(A, B_col)) for B_col in zip(*B)]


def multiply_scalar(A, scalar):
    return [[a*scalar for a in A_row] for A_row in A]


def add(A, B):
    return [[a+b for a, b in zip(A_row, B_row)] for A_row, B_row in zip(A, B)]


def subtract(A, B):
    return [[a-b for a, b in zip(A_row, B_row)] for A_row, B_row in zip(A, B)]


def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def print_matrix(A):
    for row in A:
        print(row)
    print()


def print_list(A):
    for a in A:
        print(a, end=" ")


def get_output(A):
    out = ""
    if hasattr(A[0], "__len__"):
        out += str(len(A)) + " " + str(len(A[0])) + " "
        for row in A:
            out += " ".join(map(str, row)) + " "
    else:
        out += str(len(A)) + " " + " ".join(map(str, A)) + " "
    return out


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
    return [read_line(line) for line in lines[:3]] + [read_obs(lines[3])]


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


######### Main #########


def main():
    # Read data
    A, B, pi, obs = read_input()

    # Compute for Grade E
    print_list(viterbi(A, B, pi, obs))


if __name__ == "__main__":
    main()
