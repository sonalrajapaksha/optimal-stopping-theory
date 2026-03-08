import random

def sim_with_cost(N, k, cost, t = 10000):

    reward = 0

    for i in range(t):
        candidates = [random.uniform(0,1) for i in N]
        best_obv = max(candidates[:k])

        #forced to take last
        hired = candidates[-1]

        stop_time = N

        for j in range(k,N):
            candidate = candidates[j]
            if candidate > best_obv:
                hired_value = candidate
                stopping_time = i + 1  
                break

        net_reward = hired_value - cost * stopping_time
        total_reward += net_reward

    return total_reward / t

def optimal_k_with_cost(N, cost, t=10000):
    
    best_k = 1
    best_reward = float("-inf")
    for k in range(1, N):
        reward = sim_with_cost(N, k, cost, t)
        if reward > best_reward:
            best_reward = reward
            best_k = k
    return best_k, best_reward