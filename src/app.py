import scipy
from scipy import special
import base64
import datetime
import io
import os

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'default-value-used-in-development')

app.layout = html.Div([
    html.H3('Betting Algorithm'),
    dcc.Input(id='bet_number', type='number', placeholder="Number of bets"),
    dcc.Input(id="rebate", type="number", placeholder="Rebate amount"),
    dcc.Input(id="win", type="number", placeholder="Player Win Amount"),
    dcc.Input(id="loss", type="number", placeholder="Player Loss Amount"),
    html.Br(),
    html.Button('Submit', id='button', n_clicks=0),
    html.Div(id='container',
             children='Enter all values and press submit')
])


@app.callback(
    dash.dependencies.Output('container', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('bet_number', 'value'), dash.dependencies.State('rebate', 'value'),
    dash.dependencies.State('win', 'value'), dash.dependencies.State('loss', 'value')])

def update_output(n_clicks, bet_value, rebate_value, win_value, loss_value):
    
    expected_value = []
    outcomes = list(range(0,bet_value + 1))
        
    for value in outcomes:
        w = value
        l = bet_value - value
        perm = scipy.special.binom(bet_value,w)
        prob = ((1/2**w)*(1/2**l))*perm
        win_amount = w*win_value
        loss_amount = l*loss_value
        net_winnings = win_amount - loss_amount
        if net_winnings < 0:
            net_winnings = net_winnings * (1-rebate_value)
        expected_value.append(net_winnings * prob)
        
    result = sum(expected_value)
    
    return html.H4("Player's expected value is {}".format(result))

if __name__ == '__main__':
    app.run_server()
