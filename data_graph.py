import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import json
import requests
import pprint
import plotly
from plotly.utils import PlotlyJSONEncoder

from flask import Flask, render_template
app = Flask(__name__)


dkb1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv', engine='python', encoding='utf-8')
confirmed = dkb1.iloc[0,1]
recovered = dkb1.iloc[0,2]
deaths = dkb1.iloc[0,3]
active = dkb1.iloc[0,4]


dkb1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv', engine='python', encoding='utf-8')
states1 = dkb1.iloc[1:,0].values

states1 = np.array(dkb1.iloc[1:,0].values)
confirmed1 = np.array(dkb1.iloc[1:,1].values)
recovered1 = np.array(dkb1.iloc[1:,2].values)
deaths1 = np.array(dkb1.iloc[1:,3].values)
active1 = np.array(dkb1.iloc[1:,4].values)





posts = [
    {
        'confirmed':confirmed,
        'recovered':recovered,
        'deaths':deaths,
        'active':active,
        'states1':states1,
        'confirmed1':confirmed1,
        'recovered1':recovered1,
        'deaths1':deaths1,
        'active1':active1,
    }
]




@app.route('/')
def mainpage():
  
    return render_template('index.html')



@app.route('/about')
def aboutus():
  
    return render_template('about.html')




@app.route('/contact')
def contactus():
  
    return render_template('contact.html')





@app.route('/data')

def data():
    lineplot1 = country_lineplot()
    lineplot2 = country_lineplot_rate()
    pie_india = pie_india_vs_world()
    statewise_bar = statewise_barplot()
    statewise_pie = statewise_piechart()

    return render_template('data2.html', posts=posts, plot1=lineplot1, plot2=lineplot2, plot3=pie_india, plot4=statewise_pie, plot5=statewise_bar)







c_data1 = requests.get('https://api.covid19india.org/data.json')
c_data2 = c_data1.json()


def country_lineplot():

    
    time_series1=[]
    for i in range(len(c_data2['cases_time_series'])):
        time_series1.append(c_data2['cases_time_series'][i]['totalconfirmed'])
    time_series1 = np.array(time_series1)

    time_series_date1=[]
    for i in range(len(c_data2['cases_time_series'])):
        time_series_date1.append(c_data2['cases_time_series'][i]['date'])

    time_series_date1 = np.array(time_series_date1)

    time_series_date2=[]
    for i in time_series_date1:
        time_series_date2.append(i + "2020")

    time_series_date3 = pd.to_datetime(time_series_date2, infer_datetime_format=True)
    time_series_date3 = np.array(time_series_date3)

    dq1 = pd.DataFrame(data={'confirmed_cases':time_series1, 'dates':time_series_date3})

    # Confirmed111 = np.array(dq1.iloc[:, 0])
    # dates111 = np.array(dq1.iloc[:, -1])

    # trace1 = go.Scatter(x=dates111, y=Confirmed111)

    # data = [trace1]
    # fig = go.Figure(data=data)

    trace1 = go.Scatter(x=dq1['dates'], y=dq1['confirmed_cases'])
    data=[trace1]
    fig = go.Figure(data=data)
    fig.update_layout(template="plotly_dark", title_text='Spread of corona virus in India')
    #Timeseries showing the spread of corona virus in India

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON




def country_lineplot_rate():
    
    time_series1=[]
    for i in range(len(c_data2['cases_time_series'])):
        time_series1.append(c_data2['cases_time_series'][i]['totalconfirmed'])
    time_series1 = np.array(time_series1)

    time_series_date1=[]
    for i in range(len(c_data2['cases_time_series'])):
        time_series_date1.append(c_data2['cases_time_series'][i]['date'])

    time_series_date1 = np.array(time_series_date1)

    time_series_date2=[]
    for i in time_series_date1:
        time_series_date2.append(i + "2020")

    time_series_date3 = pd.to_datetime(time_series_date2, infer_datetime_format=True)
    time_series_date3 = np.array(time_series_date3)

    time_series4 = []
    for i in range(len(time_series1)):
        if i>0:
            var11 = int(time_series1[i]) - int(time_series1[i-1])
            time_series4.append(var11)
        else:
            pass
    time_series4 = np.array(time_series4)
    time_series_date4 = time_series_date3[1:]

    dq2 = pd.DataFrame(data={'confirmed_cases':time_series4, 'dates':time_series_date4})


    trace2 = go.Scatter(x=dq2['dates'], y=dq2['confirmed_cases'])
    data=[trace2]
    fig2 = go.Figure(data=data)
    fig2.update_layout(template="plotly_dark", title_text='Rate of change of Spread of corona virus',font=dict(size=11))
    #Timeseries showing the Rate of change of Spread of corona virus in India

    # Add range slider
    fig2.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # fig.show()
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON2







dd2 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv', engine='python', encoding='utf-8')

def pie_india_vs_world():
    globalst = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    world_data1 = globalst.json()
    dd1 = pd.DataFrame(data=world_data1, index=[0])
    world_total_confirmed = dd1.iloc[0,0]
    india_total_confirmed = dd2.iloc[0,1]
    other_than_india = world_total_confirmed - india_total_confirmed



    values = [india_total_confirmed, other_than_india]
    labels = ['India', 'Other Countries combined']

    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.2, 0])])

    fig3.update_layout(template="plotly_dark", title_text='Cases in india compared to other countries', font=dict(size=11))
    #Piechart showing the Distribution of cases in india compared to other countries

    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON3




def statewise_piechart():
    df1 = dd2
    state_name = df1.iloc[1:,0]
    state_name[31]='D&NH + D&D'
    state_name[35]='Andaman & Nicobar'


    confirmed_state_cases = df1.iloc[1:,1]

    df2 = pd.DataFrame(data={'state':state_name.values, 'confirmed':confirmed_state_cases.values})

    fig4 = px.pie(df2, values='confirmed', names='state', title='Distribution of the Spread across states', template='plotly_dark')
    fig4.update_layout(showlegend=False, font=dict(size=11))
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON4




def statewise_barplot():
    df1 = dd2
    state_name = df1.iloc[1:,0]
    state_name[31]='D&NH + D&D'
    state_name[35]='Andaman & Nicobar'
    confirmed_state_cases = df1.iloc[1:,1]

    fig5 = go.Figure(data=[go.Bar(
                x=state_name, y=confirmed_state_cases,
            )])
    fig5.update_layout(template="plotly_dark", title_text='Number of cases of coronavirus in each state', font=dict(size=10))

    graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON5













# @app.route('/loopdata')
# def loopdata():



#     postgi = [{
#         'states1':states1,
#         'confirmed1':confirmed1,
#         'recovered1':recovered1,
#         'deaths1':deaths1,
#         'active1':active1,
#     }]

#     return render_template('loopdata.html', posts=postgi)




if __name__ == '__main__':
    app.run(debug=True)