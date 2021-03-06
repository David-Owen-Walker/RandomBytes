'''
   Simple AI #1
   cblouin@dal.ca
'''
# Imports the base class for AI player
from ZDengine import ZDPlayer
def increment(indices, max_value):
    '''
    Increases the indices array to the next value, rolling over increases
    in a given index to the previous index if it exceeds the highest allowed
    index, resulting in a "counting" effect
    '''
    # print str(indices)
    incrementing = len(indices)-1
    while incrementing!=-1:
        indices[incrementing]+=1
        if indices[incrementing] == max_value:
            indices[incrementing] = 0
            incrementing -= 1
        else:
            break
    if incrementing==-1:
        return True
    else:
        return False
def unique_increment(indices, max_value):
    '''
    Like increment, but will keep incrementing until no two indices
    are identical. Note - if dice_required is greater than len(cup)
    this will loop forever (or just generally not work)
    '''
    if increment(indices, max_value):
        return True
        while len(set(indices))<len(indices):
            if increment(indices, max_value):
                return True


'''
    Access and manipulation of n_win and rank is strictly forbidden. You may create as many methods
    as needed. However, the only method that will be called by the tournament is Play().

    Name both your file with the pattern: zd_yourname_ainame.py (file name), zd_yourname_ainame (Class name)
'''
dice = {'G':list('BBBFFS'), 'Y':list('BBFFSS'),'R':list('BFFSSS')}
class zd_davidwalker_walker(ZDPlayer):
    # must begin with zd_
    name = 'zd_walker'
    # Specify a division (Use the most specific)
    # Division 1 : less than 20 unergraduate courses in computer science/informatics
    # DIvision 2 : All undergraduate students
    # Division 3 : General category (Graduates, Graduate students, etc.)
    division = 1

    ## Division to be entered in (select the most specific)
    #  Division 1: less than 20 completed courses in CSCI/INFX
    #  Division 2: All Undergraduate students (Includes Div 1)
    #  Division 3: All human beings (include Div 2, Graduates, graduate students, faculty and staff)
    division = 1

    def __init__(self):
        ZDPlayer.__init__(self)

    def Play(self, player_id, tallies, hand, cup, n_brain, n_shotgun):
        '''
        The method called by the game to query a decision from the AI.
        INPUT:
        player_id (int) - the index in tallies of the AI player.
        tallies (list of list of int) - List of scores from rounds for all players.
        hand - (List of string) - List of dice in hand, coded by color (R,G,Y)
        cup - (list of string) - Similar to hand, but for what is left in the cup
        n_brain - (int) Current number of brains on the table
        n_shotgun - (int) Current number of shotgun on the table.
        OUTPUT:
        True - (bool) Proceed with another round of dice rolling
        False - (bool) Cash in the brains and end the turn

        STRATEGY:
        ...
        '''
        # Always cash in, regardless of game state.
        # print "I have "+ str(hand) + " in my hand"
        # print "the cup is "+str(cup)
        try:
            possibilities=hands(hand, cup)
            scores = outcomes(possibilities,n_shotgun)
            expected_value = evaluate_scores(scores, n_brain)
            print "I have "+str(n_brain)+" brains and "+str(n_shotgun)+" blasts"
            if expected_value>0:
                print "I choose to roll"
                return True
            else:
                print "I choose to not roll and cash in my " + str(n_brain) + " points"
                return False
        except Exception as e:
            print str(e)
            input()
            return False

def evaluate_scores(scores, n_brains):
    for index in range(len(scores)-1):
        scores[index]*=index
    scores[len(scores)-1]*=(-n_brains)
    return sum(scores)
def score_roll(hand,indices, n_shotgun):
    roll = ""
    for index in range(len(indices)):
        roll = roll + dice[hand[index]][indices[index]]
    brains = 0
    shotguns = 0
    for die_face in roll:
        if die_face == 'B':
            brains += 1
        elif die_face == 'S':
            shotguns += 1
            if shotguns + n_shotgun>=3:
                return -1
    return brains
def outcomes(possibile_hands, n_shotgun):
    '''
    Lists the possible outcomes of rolling, by bin
    '''
    scores = [0]*(2+len(possibile_hands[0])) # a roll could score from 0 to len(hand) (usually 3), or bust
                                             # scores are stored in their indices. Bust is the highest index.
    for hand in possibile_hands: # For each possible hand
        finished = False
        indices = [0]*len(hand)
        while not finished: # cycle through all possible rolls
            result = score_roll(hand, indices,n_shotgun)
            if result == -1:
                scores[len(scores)-1]+=1
            else:
                scores[result]+=1
            finished = increment(indices, 6)
    return scores


def hands(hand, cup):
    '''
    Returns a list of hands which might occur after drawing from the cup
    Each hand is equally likely
    '''

    if len(hand)>=3:
        return [hand]
    diceRequired = 3 - len(hand)
    if len(cup)<diceRequired:
        diceRequired=len(cup)
    indices = [n for n in range(diceRequired)]
    possible_hands = []
    finished = False
    count = 0;
    while not finished:
        drawn_dice = []
        for index in indices:
            drawn_dice+=cup[index]
        possible_hands.append(drawn_dice +hand)
        finished = unique_increment(indices, len(cup))
    return possible_hands
