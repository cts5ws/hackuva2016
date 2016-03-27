from models import Bigram

def readBigrams():
    f = open('../static/rec/w2_.txt', 'r')
    
    models = []
    for line in f:
        sp = line.split() # sp[0] = freq, sp[1] = first_word, sp[2] = second_word
        
        freq = int(sp[0])
        first = sp[1]
        second = sp[2]
        bigram = Bigram(first_word=first, next_word=second, frequency=freq)
        
        models.append(bigram)
        
    for model in models:
        model.save()
        