#
# some predefined problems
#
# the conventions here are
# - board:  0 is for a place that must be covered by a piece
#           1 is for obstacles - should not be filled
# - pieces: 1 means there is some material at this location
#           0 where there is just air

import numpy as np
import exact_cover as ec
import matplotlib.pyplot as plt

DTYPE = ec.io.DTYPE_FOR_ARRAY

RAW_SHAPES = {
    "F": [[1, 1, 0], [0, 1, 1], [0, 1, 0]],
    "I": [[1, 1, 1, 1, 1]],
    "L": [[1, 0, 0, 0], [1, 1, 1, 1]],
    "N": [[1, 1, 0, 0], [0, 1, 1, 1]],
    "P": [[1, 1, 1], [1, 1, 0]],
    "T": [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
    "U": [[1, 1, 1], [1, 0, 1]],
    "V": [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
    "W": [[1, 0, 0], [1, 1, 0], [0, 1, 1]],
    "X": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    "Y": [[0, 1, 0, 0], [1, 1, 1, 1]],
    "Z": [[1, 1, 0], [0, 1, 0], [0, 1, 1]],
}

PENTOMINOS = [np.array(shape, dtype=DTYPE) for shape in RAW_SHAPES.values()]


# 0 means the spot is free; 1 means its not in the shape to fill

# rectangles
BOARD_3_20 = np.zeros((3, 20), dtype=DTYPE)
BOARD_4_15 = np.zeros((4, 15), dtype=DTYPE)
BOARD_5_12 = np.zeros((5, 12), dtype=DTYPE)
BOARD_6_10 = np.zeros((6, 10), dtype=DTYPE)

# 8x8 with a 2x2 hole in the middle
BOARD_8_8 = np.zeros((8, 8), dtype=DTYPE)
BOARD_8_8[3:5, 3:5] = 1

# 2 separate 3x10 rectangles
BOARD_2_3_10 = np.zeros((3, 21), dtype=DTYPE)
BOARD_2_3_10[:, 10] = 1

# 2 separate 5x6 rectangles
BOARD_2_5_6 = np.zeros((5, 13), dtype=DTYPE)
BOARD_2_5_6[:, 6] = 1

# 3 separate 4x5 rectangles
BOARD_3_4_5 = np.zeros((3, 23), dtype=DTYPE)
BOARD_3_4_5[:, 5:6] = 1

BOARD_8_9 = np.zeros((8, 9), dtype=DTYPE)
BOARD_8_9[::7, ::8] = 1
BOARD_8_9[1::5, ::8] = 1
BOARD_8_9[::7, 1::6] = 1



# a smaller problem for developping / debugging
# the board is
# +--+--+--+
# |xx|  |xx|
# +--+--+--+
# |  |  |  |
# +--+--+--+
# |xx|  |  |
# +--+--+--+
# and we have 2 identical pieces that look like this
#    +--+
#    |  |
# +--+--+
# |  |  |
# +--+--+

SMALL_BOARD = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=DTYPE)
SMALL_PIECE = np.array([[0, 1], [1, 1]], dtype=DTYPE)

# +

import copy
def getplaces(letter, size):
    L=[]
    s=np.shape(letter)
    n=size[0]
    m=size[1]
    Z=np.zeros(size, dtype=bool)
    for i in range(n-s[0]+1):
        for j in range(m-s[1]+1):
            P=copy.deepcopy(Z)
            for l in range(s[0]):
                for k in range(s[1]):
                    P[i+l,j+k]=letter[l,k]
            Pbien=[]
            for i in P:
                Pbien=Pbien+i
            L.append(np.array(Pbien))
    return L

"""for i in truc:
    plt.imshow(i)
    plt.show()"""



# +



"""partie 1: lilian"""

def positions_possibles(shape):
    """argument : shape , liste de liste ou array numpy
    return : positions , liste d'arrays numpy comportant les positions uniques possibles pour chaque pièce"""
    
    def rotation90h(shape):
        L1,L2=np.shape(shape)
        rotshape=np.zeros((L2,L1))
        for i in range(L1):
            for j in range(L2):
                rotshape[j][L1-i-1]=shape[i][j]
        return rotshape 

    def symmetrie(shape):
        L1,L2=np.shape(shape)
        symshape=np.zeros((L1,L2))
        for i in range(L1):
            for j in range(L2):
                symshape[i][j]=shape[i][L2-j-1]
        return symshape

    
    shape=np.array(shape)
    symshape=symmetrie(shape)
    positions=[shape,symshape]
    for i in range(3):
        shape=rotation90h(shape)
        symshape=rotation90h(symshape)
        positions.append(shape)
        positions.append(symshape)

    print(positions)
    uniquepositions=[positions[0]]

    
    for el in positions:
        add=1
        for ref in uniquepositions:
            if np.shape(el)==np.shape(ref):
                if (ref==el).all():     #l'évènement (toutes les cases d'el et ref correspondent) 
                    add=0            #el est déja dans uniquepositions, on ne l'ajoute donc pas.
        if add==1:
             uniquepositions.append(el)

    
    return uniquepositions

print(list(RAW_SHAPES.keys()))
D={}
for letter in list(RAW_SHAPES.keys()):
    D[letter]=positions_possibles(RAW_SHAPES[letter])
print(len(D))


# +

"""Partie 3: get exact cover par mathieu"""
def prep_finale_lettre(letter,size):
    letters_turn=positions_possibles(RAW_SHAPES[letter])
    #print(letters_turn)
    T=[]
    for lettre_tournee in letters_turn:
        #print(lettre_tournee)
        T=T+getplaces(np.array(lettre_tournee),size)
    
    keys=list(RAW_SHAPES.keys())
    i=keys.index(letter)
    Z=np.zeros((size[0],12),dtype=bool)
    Z[0,i]=1
    
    L=[]
    for t in T:
        #print(t)
        #print(Z)
        L.append(np.concatenate((Z,t),axis=0)) 
    #print(L)
    return L


def final(size):
    FINAL=[]
    for lettre in list(RAW_SHAPES.keys()):
        FINAL=FINAL+prep_finale_lettre(letter,size)
    return FINAL

L=np.array([final((5,12))])
print(L)
S=ec.get_exact_cover(L)

# -

"""partie 4: afficher"""
plt.imshow([S], cmap='rainbow')




