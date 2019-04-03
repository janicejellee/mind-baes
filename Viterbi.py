def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st]*emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t-1][states[0]]["prob"]*trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t-1][prev_st]["prob"]*trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st
                    
            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
                    
    for line in dptable(V):
        print(line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        #print(data["prob"])
        print(max_prob)
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print ('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


states = ('A', 'B', 'C')
obs = ('Pass', 'Pass', 'Pass', 'Mark', 'Collect', 'Pass', 'Mark', 'Pass')
start_p = {'A': 0.1, 'B': 0.3, 'C': 0.6}
trans_p = {
    'A' : {'A': 0.3, 'B': 0.3, 'C': 0.4},
    'B' : {'A': 0.2, 'B': 0.5, 'C': 0.3},
    'C' : {'A': 0.1, 'B': 0.2, 'C': 0.7},
    }
 
emit_p = {
    'A' : {'Collect': 0.1, 'Mark':0.1, 'Pass': 0.8},
    'B' : {'Collect': 0.2, 'Mark':0.4, 'Pass': 0.4},
    'C' : {'Collect': 0.5, 'Mark':0.3, 'Pass': 0.2},
    }


viterbi(obs, states, start_p, trans_p, emit_p)
