# Run: pip install dash plotly pandas; python SpaceX_Dash_App.py
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
df=pd.read_csv("dataset_part_2.csv")
app=Dash(__name__)
app.layout=html.Div([html.H1("SpaceX Falcon 9 Landing Dashboard"),dcc.Dropdown(id="site",options=[{"label":"All sites","value":"ALL"}]+[{"label":s,"value":s} for s in sorted(df.LaunchSite.unique())],value="ALL"),dcc.RangeSlider(id="mass",min=0,max=int(df.PayloadMass.max())+1000,step=500,value=[0,int(df.PayloadMass.max())+1000]),dcc.Graph(id="pie"),dcc.Graph(id="scatter")])
@app.callback(Output("pie","figure"),Output("scatter","figure"),Input("site","value"),Input("mass","value"))
def update(site,mass):
 d=df if site=="ALL" else df[df.LaunchSite==site]
 d=d[d.PayloadMass.between(*mass)].copy();d["Landing"]=d.Class.map({0:"Unsuccessful",1:"Successful"})
 return px.pie(d,names="Landing",title="Landing outcome share"),px.scatter(d,x="PayloadMass",y="Class",color="LaunchSite",hover_data=["Orbit","FlightNumber"],title="Payload mass versus landing outcome")
if __name__=="__main__":app.run(debug=True)
