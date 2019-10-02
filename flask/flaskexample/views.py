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

#username = 'postgres'
#password = 'yanggnay'     # change this
#host     = 'localhost'
#port     = '5432'            # default port that postgres listens on
#db_name = 'frankl_pm10_db'

username = 'aetyang'
password = 'yanggnay'
host = 'paris-metro-air.ck2ykifurmwj.us-east-2.rds.amazonaws.com'
port = '5432'
db_name  = 'frankl_pm10_db'

db = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, db_name) )
con = None
con = psycopg2.connect(database = db_name, user = username, password = password, port = port, host = host)

query_last = "SELECT MAX(ds) FROM frankl_pm10_table"
query_results_last=pd.read_sql_query(query_last,con)
lastdate = query_results_last.iloc[-1]
lastdate = lastdate['max'] - timedelta(days=1)
lastdate = str(lastdate)
lastdate = lastdate[0:10]
    
@app.route('/')
def cesareans_input():    
    return render_template("input.html",lastdate=lastdate)

@app.route('/output')
def cesareans_output():
    #pull 'birth_month' from input field and store it
    patient = request.args.get('birth_month')
    travelhour = request.args.get('hour_input')
    time0 = datetime.strptime(patient+' '+travelhour,'%Y-%m-%d %H') # date + hour    
    time01 = time0 + timedelta(hours=1)
    
    time1 = datetime.strptime(patient,'%Y-%m-%d') # first hour of the day
    time2 = time1 + timedelta(days=1) # last hour of the day
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
    textCArr = ["#6feb1c","yellow","#800000"]
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
    query_next = "SELECT * FROM frankl_pm10_table WHERE ds >= '%s' AND ds <='%s'" % (time01,time01)
    query_results_next=pd.read_sql_query(query_next,con)
    air_qual_next = query_results_next.iloc[0].yhat    
    air_qual_next="{:10.2f}".format(air_qual_next)
    binary_next = air_qual_next < air_qual
    improve = 'WORSE'
    improve_disc = 'leave now'
    
    if binary_next:
        improve = 'BETTER'
        improve_disc = 'leave later if you can'
    return render_template("output.html", births = births, the_result = the_result, 
                           travelhour = travelhour,patient=patient,date_only = temp,
                          air_qual=air_qual,hourlabel=hourlabel,hourlabelind=hourlabelind,
                          airqualdiscribe=airqualdiscribe,textc=textc,
                          year=year,month=month,day=day,hour=hour,binary=binary,improve=improve,improve_disc=improve_disc,
                          lastdate=lastdate) ### here are the output variables