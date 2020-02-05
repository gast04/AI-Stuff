import pickle

def generateInputSequences(length):

    sequences = []

    # alternating 1010101010....        
    seq = []
    for i in range(length+1):
        if (i%2)==1:
            seq.append(1)
        else:
            seq.append(0)
    sequences.append(seq.copy())

    # alternating 110011001100...
    seq = []
    for i in range(int(length/2)+1):
        if (i%2)==1:
            seq.append(1)
            seq.append(1)
        else:
            seq.append(0)
            seq.append(0)
    sequences.append(seq.copy())

    # mod 3 100100100100
    seq = []
    for i in range((length)+1):
        if (i%3)==0:
            seq.append(1)
        else:
            seq.append(0)
    sequences.append(seq.copy())

    # mod 4 1000100010001000
    seq = []
    for i in range((length)+1):
        if (i%4)==0:
            seq.append(1)
        else:
            seq.append(0)
    sequences.append(seq.copy())


    sequences.append([0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1])

    return sequences


def getGameSequences():
    with open('sequences.pickle', 'rb') as handle:
        seqs = pickle.load(handle)
    return seqs


def getGameValidationSeqs():
    with open('validation_sequences.pickle', 'rb') as handle:
        seqs = pickle.load(handle)
    return seqs
