import math


def probability_success(N, k):
    total = sum(1 / (i-1) for i in range(k+1, N+1))
    return (k / N) * total


def optimal_k(N):
    return (math.floor(N / math.e))

def main():

    N = 10000  # number of candidates

    k = optimal_k(N)
    prob = probability_success(N, k)

    print("Number of candidates:", N)
    print("Optimal stopping point k:", k)
    print("Analytic probability of success:", prob)

if __name__ == "__main__":
    main()

