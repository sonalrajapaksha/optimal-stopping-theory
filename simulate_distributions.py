import random

def simulate_distribution(N,k,dist,t):
    '''
    simulate the optimal stopping problem using monte carlo trials for a given distribution of candidates 'N' and estimate success rate

    Args:
        - N (int) : total amount of candidates 
        - k (int) : amount of candidates to automatically reject and observe
        - dist (str): Distribution to sample candidate scores from. One of:
                      - "normal"    : Standard normal (mean=0, std=1)
                      - "uniform"   : Uniform over [0, 1]
                      - "pareto"    : Pareto with shape parameter 1.5
                      - "lognormal" : Log-normal (mean=0, std=1 in log-space)
        - t (int) : number of trials to run
    
    Returns:
        float: Estimated probability of hiring the best candidate,
               computed as (number of successes) / t.
    '''
    def sample():
        #draw the distribution given input
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

        #generates scores for all N candidates
        candidates = [sample() for i in range(N)]
        best_dist = max(candidates[:k]) #record best

        hired = None

        for candidate in candidates[k:]:
            if candidate > best_dist:
                hired = candidate
                break
        
        #success only if global best
        if hired is not None and hired == max(candidates):
            success += 1

    return success / t