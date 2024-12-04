#! /usr/bin/env python
import subprocess
from datetime import datetime
from dateutil import parser
import yaml
import bibtexparser
from jinja2 import Environment, FileSystemLoader
import shutil
import os

PAST_CONF_YEARS = 5
script_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.join(script_path,"..")
data_path = os.path.join(base_path,"data")

# Load data

with open(os.path.join(data_path,"presentations/presentations.yaml"),"r") as f:
    presentations=yaml.safe_load(f)
with open(os.path.join(data_path,"publications/mypublications.bib"),"r") as f:
    mypublications=bibtexparser.load(f)
with open(os.path.join(data_path,"CV/resume.yaml"),"r") as f:
    CV_data = yaml.safe_load(f)
with open(os.path.join(base_path,"config.yaml"),"r") as f:
    config_data = yaml.safe_load(f)
    
env=Environment(loader=FileSystemLoader(script_path,encoding="utf8"), 
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((=",
    comment_end_string="=))",
)
def add_newline_after_comma(s):
    return s.replace(", ", ", \\\\")
env.filters["add_newline_after_comma"] =  add_newline_after_comma
def format_datetime(s):
    try:
        return parser.parse(s).strftime("%b. %Y")
    except ValueError:
        return s
env.filters["format_datetime"] =  format_datetime

CV_tpl=env.get_template("CV.tex.j2")


params={}
params["config"]=config_data
params["resume"]=CV_data

exclude=lambda e: e["ENTRYTYPE"] != "mastersthesis"
params["mypublications"]=filter(exclude,mypublications.entries)
params["conferences"]=[]
params["seminars"]=[]
for p in presentations :
    date = datetime.strptime(p["presentation_date"],"%Y/%m/%d")
    if date.year < datetime.now().year-PAST_CONF_YEARS:
        continue
    
    p["names"][p["presentor_id"]-1]=r"\underline{"+p["names"][p["presentor_id"]-1]+"}"
    if not p["international"]:
        continue
    if len(p["names"]) == 1:
        p["names_connected"]=p["names"][0]
    elif len(p["names"]) == 1:
        p["names_connected"]=p["names"][0]+" and "+p["names"][1]
    else:
        p["names_connected"]=", ".join(p["names"][0:-1])+" and "+p["names"][-1]
    p["presentation_date"]=datetime.strptime(p["presentation_date"],"%Y/%m/%d").strftime("%B, %Y")
    if "conference" in p["type"]:
        p["conference"]["place_str"]=", ".join(p["conference"]["place"][1:3])
        if "oral" in p["type"]:
            p["type_str"] = "Oral Session"
        elif "poster" in p["type"]:
            p["type_str"] = "Poster Session"
        else:
            raise RuntimeError("presentation type incorrect")
        params["conferences"].append(p)
    elif "seminar" in p["type"]:
        p["seminar"]["place_str"]=", ".join([p["seminar"]["place"][0],p["seminar"]["place"][2]])
        params["seminars"].append(p)
    else:
        raise RuntimeError("presentation type incorrect")

CV_str=CV_tpl.render(params)
os.chdir(script_path)
with open("./CV.tex", "w") as f:
    f.write(CV_str)
subprocess.run(["latexmk","-c"])
subprocess.run(["latexmk","./CV.tex"])
shutil.copy("./build/CV.pdf","./CV.pdf")