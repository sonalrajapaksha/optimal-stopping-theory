import math


def probability_success(N, k):
    '''
    calculates the probability of selecting the best candidate using the reasoning described in the README

    Args:
        - N (int) : total amount of candidates
        - k (int) : number of candidates to observe and reject in phase one

    Return:
        - (float) : probability of selecting the best candidate
    '''

    total = sum(1 / (i-1) for i in range(k+1, N+1))
    return (k / N) * total


def optimal_k(N):
    return (math.floor(N / math.e))

def main():
    '''
    Computes the optimal k for a given N

    prints optimal k and the probability of selecting the best candidate
    '''
    N = 10000  # number of candidates

    k = optimal_k(N)
    prob = probability_success(N, k)

    print("Number of candidates:", N)
    print("Optimal stopping point k:", k)
    print("Analytic probability of success:", prob)

if __name__ == "__main__":
    main()

