import sys
#A program that runs the Ceasers Cipher algorithm on a word. This was the very first program that I made without starter code.


#There are 26 letters in the alphabet
#Exactly like the problem you ran in to on picoCTF
#What is the i letter after x,

""" author: @Jevon_Jackson
>>> 'a'
b
c
d...
>>> 'yessir'
zfttjs
aguukt...
"""

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#We may not need helper counter function, unless it will actually be sued to count other things, which is prolly needed given the fact that we
#may need to knwo th elength of wrod
#What i am thinking right now is making a counter for each index for both the word and the alphabet
#THe alphabets counter would be used for counting the distance needed for the shift of the letters
#THe counter for the passed in word would be sued to know where we are in the word

#Gives the letter as the [0] and the number index as [1]
def counter(value):
    container = [[value[i], i] for i in range(len(value))]
    return container

#Prints the original word w/ the number in the alphabet
def original(word):
    letters = counter(alphabet)
    characters = counter(word)
    for x in characters:
        for y in letters:
            if x[0] is y[0]:
                print(y)
    print('--')

def plus_one(word, alphabet, stopwatch):
    letters = counter(alphabet)
    characters = counter(word)
    if stopwatch == 26:
        return
    else:
        for x in characters:
            for y in letters:
                if x[0] is y[0]:
                    placeholder = y[1] + stopwatch
                    if placeholder > 25:
                        placeholder -= 26
                    for x in letters:
                        if x[1] == placeholder:
                            print(x)
                    break
        print('--')
    plus_one(word,alphabet, stopwatch +1)





original(sys.argv[0])
plus_one(sys.argv[0], alphabet, 1)
