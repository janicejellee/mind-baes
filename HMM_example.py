from __future__ import division
import numpy as np

def compute_resource_probability(states, obs):
    # takes a list of states and a list of observations as inputs, print out probability distributaion of resources 

    print("Calculating the type of resource HMM")
    liklihood = {'A': {'pass': 0.1, 'mark': 0.1, 'collect': 0.8}, \
                'B': {'pass': 0.2, 'mark': 0.4, 'collect': 0.4}, \
                'C': {'pass': 0.5, 'mark': 0.3, 'collect': 0.2}}
    A_from_A = 0.3
    B_from_A = 0.3
    C_from_A = 0.4

    A_from_B = 0.2
    B_from_B = 0.5
    C_from_B = 0.3

    A_from_C = 0.1
    B_from_C = 0.2
    C_from_C = 0.7

    A_prob = 0.1
    B_prob = 0.3
    C_prob = 0.6

    loc_x = 0
    loc_y = 0
    
    print("With %d measurements: %s, P(s = (%d, %d) at t = %d) is [Resource A: %.4f, Resource B: %.4f, Resource C: %.4f]" % \
    (0, str(obs[:0]), loc_x, loc_y, 0, A_prob, B_prob, C_prob))  
    
    for i in range(1, len(obs)+1):            
        A_num = liklihood['A'][obs[i - 1]]*(A_from_A*A_prob + A_from_B*B_prob + A_from_C*C_prob)
        B_num = liklihood['B'][obs[i - 1]]*(B_from_A*A_prob + B_from_B*B_prob + B_from_C*C_prob)
        C_num = liklihood['C'][obs[i - 1]]*(C_from_A*A_prob + C_from_B*B_prob + C_from_C*C_prob)
        
        den = A_num + B_num + C_num
        A_prob = A_num/den
        B_prob = B_num/den
        C_prob = C_num/den
       
        if states[i-1] == 'U':
            loc_y += 1
        elif states[i-1] == 'D':
            loc_y -= 1
        elif states[i-1] == 'R':
            loc_x += 1
        elif states[i-1] == 'L':
            loc_x -= 1
        
        print("With %d measurements: %s, P(s = (%d, %d) at t = %d) is [Resource A: %.4f, Resource B: %.4f, Resource C: %.4f]" % \
        (i, str(obs[:i]), loc_x, loc_y, i, A_prob, B_prob, C_prob))  
        
    return



states = ['D','R','R','D','L','D','R','U']
obs = ['mark','collect','mark','pass','pass','pass','mark','pass']
compute_resource_probability(states, obs)

# Ideal Output
# Calculating the type of resource HMM
# With 0 measurements: [], P(s = (0, 0) at t = 0) is [Resource A: 0.1000, Resource B: 0.3000, Resource C: 0.6000]
# With 1 measurements: ['mark'], P(s = (0, -1) at t = 1) is [Resource A: 0.0500, Resource B: 0.4000, Resource C: 0.5500]
# With 2 measurements: ['mark', 'collect'], P(s = (1, -1) at t = 2) is [Resource A: 0.3380, Resource B: 0.3662, Resource C: 0.2958]
# With 3 measurements: ['mark', 'collect', 'mark'], P(s = (2, -1) at t = 3) is [Resource A: 0.0696, Resource B: 0.4683, Resource C: 0.4621]
# With 4 measurements: ['mark', 'collect', 'mark', 'pass'], P(s = (2, -2) at t = 4) is [Resource A: 0.0485, Resource B: 0.2097, Resource C: 0.7419]
# With 5 measurements: ['mark', 'collect', 'mark', 'pass', 'pass'], P(s = (1, -2) at t = 5) is [Resource A: 0.0356, Resource B: 0.1457, Resource C: 0.8187]
# With 6 measurements: ['mark', 'collect', 'mark', 'pass', 'pass', 'pass'], P(s = (1, -3) at t = 6) is [Resource A: 0.0323, Resource B: 0.1311, Resource C: 0.8366]
# With 7 measurements: ['mark', 'collect', 'mark', 'pass', 'pass', 'pass', 'mark'], P(s = (2, -3) at t = 7) is [Resource A: 0.0398, Resource B: 0.3231, Resource C: 0.6371]
# With 8 measurements: ['mark', 'collect', 'mark', 'pass', 'pass', 'pass', 'mark', 'pass'], P(s = (2, -2) at t = 8) is [Resource A: 0.0397, Resource B: 0.1702, Resource C: 0.7902]
