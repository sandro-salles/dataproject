# list files in dir tree by recursion

import sys
import os


def mylister(currdir):

    if os.path.basename(currdir) == 'migrations':
        for file in os.listdir(currdir):
            if not file == '__init__.py':
                print '%s/%s -- deleting...' % (currdir, file)
                os.remove('%s/%s' % (currdir, file))

    for file in os.listdir(currdir):              # list files here
        path = os.path.join(currdir, file)        # add dir path back
        if os.path.isdir(path):
            mylister(path)

if __name__ == '__main__':
    mylister(sys.argv[1])
