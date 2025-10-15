from flask_cors import CORS

from read_data import convert_to_json

def tier7_processor(tier7_ves):
  return convert_to_json(tier7_ves)
