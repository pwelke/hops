# Some utilities for graph sampling scripts

import math
import networkx as nx
import approaches.globals_sampling


# def read_number_observations_exhaustive_approach_split_N_intervals(path_to_file,N_intervals):
#    '''
#    :param path_to_file: path to file consisting the number of observations of the exhaustive approach. The line should start with:


def make_command_string(arguments):
    string = ""
    for arg in arguments:
        string += arg + " "
    return string



def kld(p, q):
    """
    Function that computes Kullback-Leibler divergence of two discrete probability distributions.
    The probability distributions 'p' and 'q' must be python lists.
    Log2 is used in this implementation, so the outcome is in bits.
    """
    sum = 0
    # print p
    # print q
    for i in range(len(p)):
        if p[i] == 0:
            sum += 0
        else:
            sum += p[i] * (math.log(p[i], 2) - math.log(q[i], 2))
    return sum


def kld_dict_old(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list = []
    for k in p.keys():
        p_list.append(p[k])
        q_list.append(q[k])
    return kld(p_list, q_list)


def kld_dict(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list = []
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
        # else:
        # q_list.append(0.00000000001)
        # print p_list,q_list
    return kld(p_list, q_list)


def hellinger(p, q):
    """
    Calculates the Hellinger distance (using Bhattacharyya coefficient) among discrete probability distributions 'p' and 'q', given as python lists.
    It is bounded to [0, 1], unlike the Bhattacharyya, which is unbounded.
    Often the Hellinger distance is wrongly reffered to as Bhattacharyya distance.
    """
    coef = 0
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    argu = 1 - coef
    if argu <= 0:  # can happen to be 0, because of Python's rounding
        argu = 0.000000000000001
    return math.sqrt(argu)


def hellinger_dict(p, q):
    """The same as 'hellinger()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list = []
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
    ##        else:
    ##            q_list.append(0.00000000001)
    return hellinger(p_list, q_list)


def bhatta(p, q):
    """
    Calculates the Bhattacharyya distance among discrete probability distributions 'p' and 'q', given as python lists
    """
    coef = 0.000000000000001
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    return -1 * math.log(coef)


def bhatta_dict(p, q):
    """The same as 'bhatta()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list = []
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
    ##        else:
    ##            q_list.append(0.00000000001)
    return bhatta(p_list, q_list)


def abs_d_diff(p, q):
    """
    Returns the absolute difference among discrete probability distributions 'p' and 'q', which are given as python dictionaries.
    A sum of absolute differences at each value.
    """
    diff = 0
    for k in p.keys():
        diff = diff + abs(p[k] - q[k])
    return diff


def cum_abs_d_diff(p_table, q_table):
    """
    Returns a cumulative absolute difference among two discrete probability distribution tables - so, collections of distributions.
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    Absolute differences of all distributions are summed together and returned
    """
    err = 0
    for k in p_table.keys():
        ierr = abs_d_diff(p_table[k], q_table[k])
        err = err + ierr
    return err


def avg_kld(p_table, q_table):
    """
    Returns an average Kullback-Leibler divergence of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_kld = 0
    for k in p_table.keys():
        if k in q_table.keys():
            kld_i = kld_dict(p_table[k], q_table[k])
        elif approaches.globals_sampling.default_key in q_table.keys():
            kld_i = kld_dict(p_table[k], q_table[approaches.globals_sampling.default_key])
        elif 'empty' in q_table.keys():
            kld_i = kld_dict(p_table[k], q_table['empty'])
        else:
            kld_i = 0
            print('BIG ERROR in computation of KLD. NOt yet FIXED')
        cum_kld = cum_kld + kld_i
    if approaches.globals_sampling.report == "furer":
        return float(cum_kld) / (len(p_table.keys()))
    else:
        return float(cum_kld) / (len(p_table.keys()))


def avg_hellinger(p_table, q_table):
    """
    Returns an average Hellinger distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_hd = 0
    for k in p_table.keys():
        if k in q_table.keys():
            hd_i = hellinger_dict(p_table[k], q_table[k])
        elif approaches.globals_sampling.default_key in q_table.keys():
            hd_i = hellinger_dict(p_table[k], q_table[approaches.globals_sampling.default_key])
        elif 'empty' in q_table.keys():
            hd_i = hellinger_dict(p_table[k], q_table['empty'])
        else:
            hd_i = 0
            print('BIG ERROR in computation of KLD. NOt yet FIXED')
        cum_hd = cum_hd + hd_i
    return float(cum_hd) / len(p_table.keys())





def avg_bhatta(p_table, q_table):
    """
    Returns an average Bhattacharyya distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_bd = 0
    for k in p_table.keys():
        if k in q_table.keys():
            bd_i = bhatta_dict(p_table[k], q_table[k])
        elif approaches.globals_sampling.default_key in q_table.keys():
            bd_i = bhatta_dict(p_table[k], q_table[approaches.globals_sampling.default_key])
        elif 'empty' in q_table.keys():
            bd_i = bhatta_dict(p_table[k], q_table['empty'])
        else:
            bd_i = 0
            print('BIG ERROR in computation of KLD. NOt yet FIXED')
        cum_bd = cum_bd + bd_i
    return float(cum_bd) / len(p_table.keys())
