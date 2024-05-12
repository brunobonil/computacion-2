
import re
a = '1021'

if len(a) != 4 or any(i not in ['1','0'] for i in a):
    print('permiso mal indicado')
else: print('permiso correcto')
