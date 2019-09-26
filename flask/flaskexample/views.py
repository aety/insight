from a_Model import ModelIt

from datetime import datetime
from datetime import timedelta  
from flask import request
from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

username = 'postgres'
password = 'yanggnay'     # change this
host     = 'localhost'
port     = '5432'            # default port that postgres listens on
db_name = 'frankl_pm10_db'

db = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, db_name) )
con = None
con = psycopg2.connect(database = db_name, user = 'postgres', password = 'yanggnay', port = '5432', host = 'localhost')

@app.route('/input')
def cesareans_input():
    return render_template("input.html")

@app.route('/output')
def cesareans_output():
    #pull 'birth_month' from input field and store it
    patient = request.args.get('birth_month')
    travelhour = request.args.get('hour_input')
    time1 = datetime.strptime(patient,'%Y-%m-%d')
    time2 = time1 + timedelta(days=1)
    temp = patient[0:10]
    year = int(patient[0:4])-2012
    month = int(patient[5:7])-1
    hour = int(travelhour)
    day=time1.weekday()
    
    query = "SELECT * FROM frankl_pm10_table WHERE ds >= '%s' AND ds < '%s'" % (time1, time2)
    query_results=pd.read_sql_query(query,con)
    air_qual=query_results.iloc[int(travelhour)].yhat
    air_qual="{:10.2f}".format(air_qual)
    labelArr = ['good','moderate','unhealthy']
    hourlabelind = query_results.iloc[int(travelhour)].label
    hourlabel = labelArr[hourlabelind]
    binary = "BETTER"
    if query_results.iloc[int(travelhour)].yhat > query_results.iloc[int(travelhour)].yhat_st:
        binary = "WORSE"        
    airqualdiscribe = ['Satisfactory. Air pollution poses little or no risk.',
                      'Acceptable. There may be a moderate health concern for a very small number of people.',
                      'People with heart and lung diseases, older adults and children are at a greater risk.']
    airqualdiscribe = airqualdiscribe[hourlabelind]
    textCArr = ["#008000","#FF8000","#800000"]
    textc = textCArr[hourlabelind]    
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['ds'],
                           birth_month=query_results.iloc[i]['yhat'],
                           birth_month1=query_results.iloc[i]['yhat_upper'],birth_month2=query_results.iloc[i]['yhat_lower'],
                           st_air=query_results.iloc[i]['yhat_st'],st_air1=query_results.iloc[i]['yhat_upper_st'],
                           st_air2=query_results.iloc[i]['yhat_lower_st'])
                     )
    the_result = ModelIt(patient,births)    
    return render_template("output.html", births = births, the_result = the_result, 
                           travelhour = travelhour,patient=patient,date_only = temp,
                          air_qual=air_qual,hourlabel=hourlabel,hourlabelind=hourlabelind,
                          airqualdiscribe=airqualdiscribe,textc=textc,
                          year=year,month=month,day=day,hour=hour,binary=binary) ### here are the output variables