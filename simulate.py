import random

# function to simulate N candidates over t trials. uses k as the tested optimal value
def simulate(N, k, t = 10000):

    #init successful picks
    success = 0

    #randomise a list of N numbers
    for i in range(t):
        candidates = list(range(1,N+1))
        random.shuffle(candidates)
        #use values before k to compare to
        best = max(candidates[:k])

        hired = None
    
        #compare if the values after k is bigger than the largest in set [1,k]
        for candidate in candidates[k:]:
            if candidate > best:
                hired = candidate
                break
            
        #if N is not found before k values, then a success is recorded
        if hired == N:
            success += 1

    return success/t



j = 10000
k = 4000

print(simulate(j, k, 10000))