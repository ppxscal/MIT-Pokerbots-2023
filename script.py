import pickle, sys
dic = pickle.load(open('flopLookup.pkl', 'rb'))
print(sys.getsizeof(dic))

