# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################
#Code by Dylan Sholtes and Bhuvaneshwar Mohan
# Set the given parameters to obtain the specified policies through
# value iteration.
#follows the bridge when there is no noise
def question2():
    answerDiscount = .9
    answerNoise = 0.0
    return answerDiscount, answerNoise
#prefer close exit, risk cliff
def question3a():
    #low discount and negative living reward makes close exit preferable
    answerDiscount = 0.1
    answerNoise = 0
    answerLivingReward = -4.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#prefer close exit avoid cliff
#small noise avoids cliff due to uncertainty
def question3b():
    #low discount, small living reward with  small noise makes close exit avoid cliff preferable
    answerDiscount = .1
    answerNoise = .1
    answerLivingReward = .1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'
#Prefer distant exit risk cliff
def question3c():
    #small negative living reward with discount of 1 prefers distant exit while risking cliff
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#prefer distant exit, avoid cliff
#small noise avoids cliff due to uncertainty
def question3d():
    #small noise with positive living reward avoids cliff and prefers distant exit
    answerDiscount = .7
    answerNoise = .1
    answerLivingReward = 2
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'
#Avoid both exits and cliff
def question3e():
    #discount of 1 and a positive living reward never terminates
    #with a discount of one, there is no benefit in terminating
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    #with exploration, more than 50 iterations are needed for the Q-Learner to find the optimal policy
    answerEpsilon = 0
    answerLearningRate = .1
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
