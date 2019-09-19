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
db_name = 'auber_pm10_db'

db = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, db_name) )
con = None
con = psycopg2.connect(database = db_name, user = 'postgres', password = 'yanggnay', port = '5432', host = 'localhost')

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                             
                SELECT * FROM auber_pm10_table WHERE ds>'2019-12-30 00:00:00';                                                                              
                """
    query_results = pd.read_sql_query(sql_query,con)
    births = ""
    print(query_results[:10])
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births

@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT * FROM auber_pm10_table WHERE ds>'2019-12-30 00:00:00';                                                   
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['ds'], birth_month=str(query_results.iloc[i]['trend'])))
    return render_template('cesareans.html',births=births)









#@app.route('/input')
#def cesareans_input():
#    return render_template("input.html")

#@app.route('/output')
#def cesareans_output():
#    return render_template("output.html")