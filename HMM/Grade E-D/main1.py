######### Utils #########

def multiply(A, B):
    return [[sum(a*b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]


def get_output(A):
    out = ""
    out += str(len(A)) + " " + str(len(A[0])) + " "
    for row in A:
        out += " ".join(map(str, row)) + " "
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

######### Main #########


def main():
    # Read data
    A, B, pi, obs = read_input()

    print(forward_algorithm(A, B, pi, obs))


if __name__ == "__main__":
    main()
