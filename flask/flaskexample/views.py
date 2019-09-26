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
#db_name = 'birth_db'
db_name = 'frankl_pm10_db'

db = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, db_name) )
con = None
con = psycopg2.connect(database = db_name, user = 'postgres', password = 'yanggnay', port = '5432', host = 'localhost')


#@app.route('/')
#@app.route('/index')
#def index():
#    return render_template("index.html",
#       title = 'Home', user = { 'nickname': 'Miguel' },
#       )

#@app.route('/db')
#def birth_page():
#    sql_query = """                                                             
#                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean'\
#;                                                                               
#                """
#    query_results = pd.read_sql_query(sql_query,con)
#    births = ""
#    print(query_results[:10])
#    for i in range(0,10):
#        births += query_results.iloc[i]['birth_month']
#        births += "<br>"
#    return births

#@app.route('/db_fancy')
#def cesareans_page_fancy():
#    sql_query = """
#               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
#                """
#    query_results=pd.read_sql_query(sql_query,con)
#    births = []
#    for i in range(0,query_results.shape[0]):
#        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], #birth_month=query_results.iloc[i]['birth_month']))
#    return render_template('cesareans.html',births=births)






@app.route('/input')
def cesareans_input():
    return render_template("input.html")

#@app.route('/output')
#def cesareans_output():
#    return render_template("output.html")

@app.route('/output')
def cesareans_output():
    #pull 'birth_month' from input field and store it
    patient = request.args.get('birth_month')
    temp = patient[0:10]
    print(temp)
    travelhour = request.args.get('hour_input')
    time1 = datetime.strptime(patient,'%Y-%m-%d')
    time2 = time1 + timedelta(days=1)
    query = "SELECT * FROM frankl_pm10_table WHERE ds >= '%s' AND ds < '%s'" % (time1, time2)
    #print(query)
    query_results=pd.read_sql_query(query,con)
    air_qual=query_results.iloc[int(travelhour)].yhat
    air_qual="{:10.2f}".format(air_qual)
    labelArr = ['good','moderate','unhealthy']
    hourlabelind = query_results.iloc[int(travelhour)].label
    hourlabel = labelArr[hourlabelind]
    
    births = []
    #print(query_results)
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
                          air_qual=air_qual,hourlabel=hourlabel,hourlabelind=hourlabelind) ### here are the output variables