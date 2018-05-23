from math import log


def viterbi(obs_states, hidden_states, init_prob, trans_prob, emis_prob):
    d_viterbi = []
    # Initialisation
    log_probabilities = [log(init_prob[k]) + log(emis_prob[k][obs_states[0]]) for k in hidden_states]
    previous_state = None
    d_viterbi.append({"log_prob": log_probabilities, "prev_s" : previous_state})
    # Do Viterbi
    for i in range(1, len(obs_states)):
        log_probabilities = []
        previous_state = []
        for l in hidden_states:
            trans_prob_to_l = [d_viterbi[i-1]["log_prob"][k] +\
                                log(trans_prob[k][l]) for k in hidden_states]
            max_log_prob = max(trans_prob_to_l)
            log_probabilities.append(max_log_prob + log(emis_prob[l][obs_states[i]]))
            previous_state.append(trans_prob_to_l.index(max_log_prob))
        d_viterbi.append({"log_prob": log_probabilities, "prev_s": previous_state})
    # Last state
    last_prob = max(d_viterbi[-1]["log_prob"])
    last_state = d_viterbi[-1]["log_prob"].index(last_prob)
    # Tracing back
    h_states = [0 for i in range(len(obs_states))]
    h_states[-1] = last_state
    for i in range(1, len(obs_states)):
        prev_state = d_viterbi[-i]["prev_s"][h_states[-i]]
        h_states[-i-1] = prev_state
    return (h_states, last_prob)

    