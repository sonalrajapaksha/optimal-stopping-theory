import random


def sim_with_cost(N, k, cost, t=10000):
    """
    Simulate a secretary problem variant where each candidate interviewed
    incurs a time cost, and estimate the average net reward.

    Candidate scores are drawn from Uniform(0, 1). The first k candidates
    are observed to establish a benchmark (exploration phase). The first
    subsequent candidate exceeding that benchmark is hired. If no such
    candidate is found, the last candidate is hired by default.

    Net reward per trial = hired_value - cost * stopping_time
    where stopping_time is the 1-based index at which we hire.

    Args:
        N    (int):   Total number of candidates.
        k    (int):   Number of candidates to observe before selecting.
        cost (float): Cost incurred per candidate interviewed (time penalty).
        t    (int):   Number of Monte Carlo trials (default: 10000).

    Returns:
        float: Mean net reward across all trials.
    """
    total_reward = 0  # Fixed: was referenced before assignment in original

    for _ in range(t):
        # Generate scores for all N candidates
        candidates = [random.uniform(0, 1) for _ in range(N)]  # Fixed: range(N) not range(i)

        # Exploration phase: find the best score among the first k candidates
        best_observed = max(candidates[:k])

        # Default: if no candidate beats the benchmark, hire the last one
        hired_value = candidates[-1]
        stopping_time = N  

        # Selection phase: hire the first candidate who exceeds the benchmark
        for j in range(k, N):
            candidate = candidates[j]
            if candidate > best_observed:
                hired_value = candidate
                stopping_time = j + 1  # Fixed: should index into candidates, not trials
                break

        # Subtract the time cost proportional to how long we searched
        net_reward = hired_value - cost * stopping_time
        total_reward += net_reward  # Fixed: was reward += instead of total_reward +=

    return total_reward / t

def optimal_k_with_cost(N, cost, t=10000):
    """
    Brute-force search for the exploration threshold k that maximises
    average net reward in the secretary problem with interview costs.

    Evaluates every candidate value of k from 1 to N-1 via simulation,
    and returns the k that yields the highest mean net reward.

    Args:
        N    (int):   Total number of candidates.
        cost (float): Per-interview time cost passed to sim_with_cost.
        t    (int):   Monte Carlo trials per k evaluation (default: 10000).

    Returns:
        tuple[int, float]: (optimal_k, best_reward)
            - optimal_k   : The k value that maximises net reward.
            - best_reward : The corresponding mean net reward.
    """
    best_k = 1
    best_reward = float("-inf")

    # Evaluate every possible stopping threshold
    for k in range(1, N):
        reward = sim_with_cost(N, k, cost, t)
        if reward > best_reward:
            best_reward = reward
            best_k = k

    return best_k, best_reward