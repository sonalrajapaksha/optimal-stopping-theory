import random

def simulate_distribution(N,k,dist,t):

    def sample():
        if dist == "normal":
            return random.gauss(0, 1)
        elif dist == "uniform":
            return random.uniform(0, 1)
        elif dist == "pareto":
            return random.paretovariate(1.5)
        elif dist == "lognormal":
            return random.lognormvariate(0, 1)
        
    success = 0

    for i in range(t):
        candidates = [sample() for i in range(N)]
        best_dist = max(candidates[:k])

        hired = None

        for candidate in candidates[k:]:
            if candidate > best_dist:
                hired = candidate
                break
        
        if hired is not None and hired == max(candidates):
            success += 1

    return success / t