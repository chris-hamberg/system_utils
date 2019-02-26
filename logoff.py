import os

username = 'chris'
try:
    os.system('sudo pkill -u {username}'.format_map(vars()))
except Exception:
    pass
