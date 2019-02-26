import os, sys

if sys.argv[1:]:
    x = sys.argv[1]
else:
    x = 7 
os.system('transset-df 0.{}'.format(x))
