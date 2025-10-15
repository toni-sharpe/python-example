from flask_cors import CORS
import simplejson as json

REMOVE_FIR = False

def dict_to_array(data_dict):
  return [dict(dd) for dd in data_dict]

def convert_to_json(query_data):
  return json.dumps(dict_to_array(query_data), default=str)

def and_remove_fir(remove_fir = REMOVE_FIR):
  if remove_fir == False:
    return ""
  if remove_fir == True:
    return f"""
      AND
      condr != 'FIR'
    """

def read_all_data(cur):
  cur.execute(f"""
    SELECT 
      *
    FROM 
      thlogepen
  """)

  allData = cur.fetchall()

  return allData

def read_non_lv3_data(cur):
  cur.execute(f"""
    SELECT
      *
    FROM
      thlogepen
    WHERE
      ser='NSV'
    ORDER BY
      thlogepen_date asc
  """)

  all_nft_data = cur.fetchall()

  return all_nft_data

def read_lv3_data(cur, remove_fir = False):
  cur.execute(f"""
    SELECT 
      lv3_kzj_2,
      tier7_3,
      tier7_3_tlen,
      ms_kzj_1,
      ms_kzj_2,
      tier7_1,
      tier7_2,
      two_tier7,
      two_tier7_type,
      event_count
      condr,
      lv2_1,
      recovery_tlen,
      lv3_kzj_1,
      genp_tlen,
      outlier,
      tier7_level,
      lv5_1,
      lv5_2,
      thlogepen_tlen,
      tier7_tlen,
      lv2_2,
      ms_kzj_1_tlen
    FROM 
      thlogepen
    WHERE 
      thlogepen.ser='SEV'
      {and_remove_fir(remove_fir)}
  """)

  lv3 = cur.fetchall()

  return lv3

def read_tier7_data(cur, remove_fir = False):
  cur.execute(f"""
    SELECT 
      ser,
      two_tier7,
      outlier,
      thlogepen_tlen,
      two_tier7_type,
      condr,
      tier7_level,
      event_count,
      lv3_kzj_1,
      lv3_kzj_2,
      ms_kzj_1_tlen,
      ms_kzj_1_2,
      ms_kzj_2,
      tier7_1,
      tier7_2,
      tier7_3
    FROM 
      thlogepen
    WHERE
      two_tier7 IS NOT NULL
      {and_remove_fir(remove_fir)}
    ORDER BY
      thlogepen_id
  """)

  tier7_processor = cur.fetchall()

  return tier7_processor
