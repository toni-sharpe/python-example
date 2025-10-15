from flask import Flask
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import simplejson as json

from read_data import convert_to_json, read_all_data, read_lv3_data, read_tier7_data, read_non_lv3_data

from check_tool_kit import process_check
from tier7_processor import tier7_processor
from all_ves import process_all_ves

conn = psycopg2.connect(
    host="localhost",
    database="insta",
    user="postgres",
    password="admin")

cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

all_ves = read_all_data(cur)
lv3_ves = read_lv3_data(cur)
non_lv3_ves = read_non_lv3_data(cur)
tier7_ves = read_tier7_data(cur)
anticheck_lv3_ves = read_lv3_data(cur, remove_fir = True)
anticheck_tier7_ves = read_tier7_data(cur, remove_fir = True)
checked_test_ves = read_tier7_data(cur)

conn.commit()
conn.close()

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
  return "Hello world!"

@app.route("/Scatter")
def scatter():
  return process_all_ves(all_ves)

@app.route("/Tier7List")
def tier7_processor():
  return tier7_processor(tier7_ves)

@app.route("/CheckToolKit")
def check():
  return process_check(anticheck_tier7_ves, lv3_ves)

@app.route("/Gantt")
def statistics():
  return process_all_ves(all_ves)

@app.route("/TimeLine")
def timeLine():
  return process_all_ves(all_ves)

@app.route("/HistogramMaker")
def histogramMaker():
  return process_all_ves(all_ves)

@app.route("/SVG")
def svg():
  return process_all_ves(all_ves)

@app.route("/WorldMap")
def world_map():
  return process_all_ves(all_ves)

