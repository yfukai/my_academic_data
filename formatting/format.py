#!/usr/bin/env python3
import yaml
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def main():
    parser=argparse.ArgumentParser(description="format yaml data in templates")
    parser.add_argument("template",type=str)
    parser.add_argument("--fy",type=int,help="faculty year")
    args=parser.parse_args()
    with open("presentation.yaml","r") as f:
        data=yaml.safe_load(f)
    for d in data:
        if "conference" in d:
            d["conference"]["date"]["begin"]=datetime.strptime(d["conference"]["date"]["begin"],"%Y/%m/%d")
            d["conference"]["date"]["end"]=datetime.strptime(d["conference"]["date"]["end"],"%Y/%m/%d")
        d["presentation_date"]=datetime.strptime(d["presentation_date"],"%Y/%m/%d")
    if not args.fy is None: 
        data=filter(lambda d : 
                ( d["presentation_date"] >= datetime(args.fy,4,1) ) and 
                ( d["presentation_date"] <= datetime(args.fy+1,3,31) ),
                data)
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template(args.template)
    formatted=tpl.render({"data":data})
    print(formatted)
    
if __name__ == '__main__':
    main()
