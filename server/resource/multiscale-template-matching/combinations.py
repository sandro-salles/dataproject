from random import shuffle
from itertools import product, permutations
import sys
import timeit


def find_occurrence():

    count = 0

    chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')
    shuffle(chars)

    for x in permutations(chars, 6):
        # sys.stdout.write('\r%s: ' % count)
        # sys.stdout.flush()

        if 'NSOED6' == ''.join(x):
            print 'found'
            break

        count += 1

    return True

print timeit.timeit(find_occurrence, number=1)
