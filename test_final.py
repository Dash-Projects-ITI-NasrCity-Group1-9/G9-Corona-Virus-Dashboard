from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

# https://covid19.who.int/info/
df = pd.read_csv("WHO-COVID-19-global-data(1).csv")

# Define the root route
@app.route('/')
def index():
    countries = df['Country'].drop_duplicates().to_list()
    dates = df['Date_reported'].drop_duplicates().to_list()
    # return render_template('test_final.html', dates=dates, countries=countries)
    return render_template('refrence.html', dates=dates, countries=countries)


@app.route('/callback1/<endpoint>')
def cb1(endpoint):
    if endpoint == "getTest":
        return km(request.args.get('country'), request.args.get('date'))
    elif endpoint == "getTest1":
        return km1(request.args.get('country'), request.args.get('date'))
    elif endpoint == "getNumbers1":
        return getNumbers1(request.args.get('country'), request.args.get('date'))


@app.route('/callback/<endpoint>')
def cb(endpoint):
    if endpoint == "getStock":
        return gm(request.args.get('country'), request.args.get('date'))
    elif endpoint == "getGraph2":
        return gm1(request.args.get('country'), request.args.get('date'))
    # elif endpoint == "getTest":
    #     return gm1(request.args.get('country'), request.args.get('date'))
    elif endpoint == "getNumbers":
        return getNumbers(request.args.get('country'), request.args.get('date'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = df.describe()["Followers(millions)"].to_json()
        return json.dumps(st)
    else:
        return "Bad endpoint", 400


# Return the JSON data for the Plotly graph
# def gm(country, date):
#     fig = px.bar(df[df['Country'] == country], x="Date_reported", y="New_cases")
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
def gm(country, date):
    fig = px.bar(df[df['Country'] == country], x="Date_reported", y="New_cases")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def gm1(country, date):
    fig1 = px.bar(df[df['Country'] == country], x="Date_reported", y="New_deaths")
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON1

def km(country, date):
    fig = px.bar(df[df['Country_code'] == country], x="Date_reported", y="New_cases")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def km1(country, date):
    fig = px.bar(df[df['Country_code'] == country], x="Date_reported", y="New_deaths")
    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON1


def getNumbers(country,date):
    cond = (df['Date_reported'] == str(date)) & (df['Country'] == str(country))
    print("********************" + str(country))
    print("********************" + str(date))
    a = df[cond]["New_deaths"].values[0]
    b = df[cond]["New_cases"].values[0]
    c = df[cond]["Cumulative_cases"].values[0]
    d = df[cond]["Cumulative_deaths"].values[0]
    print(str(a),str(b))
    return {"a":str(a),"b":str(b),"c":str(c),"d":str(d)}

def getNumbers1(country,date):
    cond = (df['Date_reported'] == str(date)) & (df['Country_code'] == str(country))
    print(str(country))
    print("********************" + str(country))
    print("********************" + str(date))
    a = df[cond]["New_deaths"].values[0]
    b = df[cond]["New_cases"].values[0]
    c = df[cond]["Cumulative_cases"].values[0]
    d = df[cond]["Cumulative_deaths"].values[0]
    print(str(a),str(b))
    return {"a":str(a),"b":str(b),"c":str(c),"d":str(d)}

if __name__ == "__main__":
    app.run(debug=True)