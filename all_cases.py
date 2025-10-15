import copy
from flask_cors import CORS
import numpy as np

from read_data import convert_to_json, dict_to_array

def process_all_ves(all_ves):
  return convert_to_json(all_ves)
  