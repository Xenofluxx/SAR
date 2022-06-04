#!/usr/bin/env python
# ! -*- encoding: utf8 -*-
# 3.- Mono Evolved

import pickle
import random
import sys
from SAR_p3_monkey_lib import Monkey

if __name__ == "__main__":

    if len(sys.argv) not in (2, 3) and (len(sys.argv) == 4 and sys.argv[3] != 'tri'):
        print("python %s indexfile [n] [tri]" % sys.argv[0])
        sys.exit(-1)

    index_filename = sys.argv[1]

    # casteas a int, si no puede n será 10
    try:
        n = int(sys.argv[2])
    except:
        n = 10
    m = Monkey()
    m.load_index(index_filename)
    if len(sys.argv) == 4 and sys.argv[3] == 'tri':
        m.generate_sentences(n, True)
    else:
        m.generate_sentences(n)
