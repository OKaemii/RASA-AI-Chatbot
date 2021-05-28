print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from ..scripts.python import BestFile2UseAlg

bf = BestFile2UseAlg()

test = "the monkey big"
test = bf.clearStopwords(test)

print(test)