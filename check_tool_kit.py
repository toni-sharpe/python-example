import copy
import math
import numpy as np
import simplejson as json

from flask_cors import CORS
from read_data import convert_to_json, dict_to_array

DEFAULT_DICT = { 
   '0': [],  '5': [], '10': [], '15': [],
  '20': [], '25': [], '30': [], '35': [],
  '40': [], '45': [], '50': [], '55': [],
  '60': [],
  'lv3Ave': 0,
  'nonLvl2Ave': 0,
  'aveDiff': 0,
  'hue': 0,
}

LIST_REDUCTION_FACTOR = 0.50

MASSIVE = True

def two_tier7_blocks (two_tier7):
  if (two_tier7 > 60):
    return '60'
  if (two_tier7 > 55):
    return '55'
  if (two_tier7 > 50):
    return '50'
  if (two_tier7 > 45):
    return '45'
  if (two_tier7 > 40):
    return '40'
  if (two_tier7 > 35):
    return '35'
  if (two_tier7 > 30):
    return '30'
  if (two_tier7 > 25):
    return '25'
  if (two_tier7 > 20):
    return '20'
  if (two_tier7 > 15):
    return '15'
  if (two_tier7 > 10):
    return '10'
  if (two_tier7 > 5):
    return '5'
  return '0'

def format_ser(r):
  ser = ''
  if r[0] == 'LV2':
    ser = 'lv3'
  if r[0] == 'NFT':
    ser = 'nonLvl2'
  return ser

def serialize_sets(obj):
  if isinstance(obj, set):
      return list(obj)

  return obj


def map_tier7_processor(tier7):
  return [tier7['ser'], tier7['two_tier7']]

def process_check(tier7_ves, lv3_ves):
  # for 50 times
  final_result = []
  if MASSIVE == False:
    final_result = list(range(10000))
  else:
    final_result = list(range(10000))

  x = 0
  final_result_len = len(final_result)

  while(x < final_result_len):
    tier7_processor = np.array(dict_to_array(tier7_ves))
    prsypt_len = tier7_processor.size
    random_augment = 0 - (5.5 * np.random.rand()) + (11 * np.random.rand())
    reduced_size = math.ceil(prsypt_len * LIST_REDUCTION_FACTOR + random_augment)
    np.random.shuffle(tier7_processor)
    reduced_tier7_processor = np.resize(tier7_processor, reduced_size)

    full_array = list(map(map_tier7_processor, reduced_tier7_processor))

    data_dict = dict()
    data_dict = copy.deepcopy(DEFAULT_DICT)

    lv3_array = []
    non_lv3_array = []

    for thlogepen in full_array:
      ser = format_ser(thlogepen)
      two_tier7 = thlogepen[1]

      tier7_block = two_tier7_blocks(two_tier7)
      data_dict[tier7_block].append([ser, two_tier7])

      if ser == 'lv3':
        lv3_array.append(two_tier7)
      if ser == 'nonLvl2':
        non_lv3_array.append(two_tier7)

    data_dict['lv3Ave'] = np.median(lv3_array)
    data_dict['nonLvl2Ave'] = np.median(non_lv3_array)
    data_dict['aveDiff'] = data_dict['nonLvl2Ave'] - data_dict['lv3Ave']
    if data_dict['aveDiff'] < 0:
      data_dict['hue'] = 220 + data_dict['aveDiff'] * 6
    else:
      data_dict['hue'] = 20 + data_dict['aveDiff']

    final_result[x] = data_dict['hue']

    x = x + 1

  result_to_return = dict()
  result_to_return['tier7_ves'] = tier7_ves
  result_to_return['checked_test_ves'] = final_result
  result_to_return['scatter_ves'] = lv3_ves

  return json.dumps(result_to_return, default=serialize_sets)


