import pandas as pd
import json 
import numpy

# fname = 'chatelet'
# fcode = 'cha4'
#fname = 'auber'
#fcode = 'auba'
fname = 'franklin-d-roosevelt'
fcode = 'fra1'

dateTimeArr = []
nameArr = ['c2'+fcode,'t'+fcode,'hy'+fcode,'10'+fcode,'n2'+fcode,'no'+fcode,'dateheure'] # auber
dispArr = ['CO2','temp','humidity','PM10','NO2','NO','dateTime']
bigDataArr = []



with open('qualite-de-lair-mesuree-dans-la-station-' + fname + '.json') as json_data:
    jsonData = json.load(json_data)
    
    for i in jsonData:        
        
        fields = i['fields']        
        tempArr = []
        
        for j in range(len(nameArr)-1):            
            ent = numpy.nan
            if nameArr[j] in fields:
                ent = fields[nameArr[j]]
            tempArr.append(ent)
            
        j = len(nameArr)-1 # special processing for dateTime
        ent = numpy.nan
        if nameArr[j] in fields:
                ent = fields[nameArr[j]]
                ent = ent[0:19]
                ent = ent.replace("T"," ")
                #print(ent)
        tempArr.append(ent)
            
        bigDataArr.append(tempArr)
        
# transpose
bigDataArr = [[bigDataArr[j][i] for j in range(len(bigDataArr))] for i in range(len(bigDataArr[0]))] 
        
# c2cha4 = CO2
# tcha4 = TEMP
# hych4 = humidity
# 10cha4 = PM10
# n2cha4 = NO2
# nocha4 = NO
# dateheure = dateTime








dArr = list(range(0,6))

for dInd in dArr:
    
    d = None
    df = None
    m = None
    forecast = None
    
    print(dInd)
    dnumber = dInd

    d = {'ds': bigDataArr[6],'y': bigDataArr[dnumber]}
    dname = dispArr[dnumber]
    df = pd.DataFrame(data=d)

    # start playing around with PROPHET
    from fbprophet import Prophet

    df.ds = pd.to_datetime(df.ds) # convert into datetime

    # fitting
    print("fitting " + dname)
    m = Prophet()
    m.fit(df) # Fitting should take 1-5 seconds

    # predict
    print("predicting " + dname)
    future = m.make_future_dataframe(periods=365)
    #future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    # save model and prediction
    import pickle
    pkl_path = fname + '/' + dname + "_prophet.pkl"
    with open(pkl_path, "wb") as f:
        # Pickle the 'Prophet' model using the highest protocol available.
        pickle.dump(m, f)

    # save the dataframe
    forecast.to_pickle(fname + '/' + dname + "_forecast.pkl")
    print("*** " + dname + " Data Saved ***")

    # plot using prophet 
    pd.plotting.register_matplotlib_converters() # this resolves some issues with data type
    components_fig = m.plot(forecast)
    axes = components_fig.get_axes()
    axes[0].set_ylabel(dname)
    components_fig.savefig(fname + '/' + dname + '_1.jpg')
    
    # plot using prophet 
    pd.plotting.register_matplotlib_converters() # this resolves some issues with data type
    components_fig = m.plot_components(forecast)
    axes = components_fig.get_axes()
    axes[0].set_ylabel(dname)
    components_fig.savefig(fname + '/' + dname + '_2.jpg')
    