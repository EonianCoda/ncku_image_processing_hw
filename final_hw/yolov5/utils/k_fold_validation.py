import random
from collections import namedtuple


Kfold_setting = namedtuple('Kfold_setting', ['K', 'cur_fold', 'is_val', 'seed'])
