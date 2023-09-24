######### Utils #########

def multiply(A, B):
    return [[sum(a*b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]


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


def read_input():
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break
    return [read_line(line) for line in lines]


######### Exercise #########

def emissions_probability(A, B, pi):
    return multiply(multiply(pi, A), B)

######### Main #########


def main():
    # Read data
    [A, B, pi] = read_input()

    # Compute for Grade E
    print(get_output(emissions_probability(A, B, pi)))


if __name__ == "__main__":
    main()
