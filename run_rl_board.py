
from flask import Flask, Markup, render_template
import time
import random
import pandas

app = Flask(__name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

'''
values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]
'''

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

ACC_values_history = [80, 80 ,80, 75, 50, 0.5, 0.5, 0.5, 50, 75, 80, 80, 80]
ACC_labels_history = []
for i in range(len(ACC_values_history)):
    ACC_labels_history.append(i)
global count
count = 0   

global ACC_value_array, ACC_label_array
ACC_value_array = [0]
ACC_label_array = [0]

global N1, N2
N_new = 0
N_old = 0
global reward, reward_accum, acc_state, quant_state, episode_num, layer_num, layers_bits_list
reward = []
reward_accum = []
acc_state = []
quant_state = []
episode_num = []
layer_num = []

@app.route('/bar')
def bar():
    global ACC_value, ACC_label
    global ACC_value_array, ACC_label_array
    global count
    count+=1
    ACC_value_array.append(random.randint(0,100))
    ACC_label_array.append(count)
    return render_template('bar_chart.html', title=' UCSD_ACT_rlboard --- RL Agent ACCURCY', max=100, labels=ACC_label_array, values=ACC_value_array)

@app.route('/rlboard')
def line():
    global N_old, N_new
    global reward, reward_accum, acc_state, quant_state, episode_num, layer_num, layers_bits_list, layers_labels
    layers_labels = ['conv1','conv2','conv3','conv4','conv5','fc6', 'fc7','fc8' ]
    #io = pandas.read_csv('../rl_board_history.csv',sep=",",usecols=(1,2,4)) # To read 1st,2nd and 4th columns
    df = pandas.read_csv('../rl_board_history.csv',sep=",")
    N_new = len(df.index)
    diff = N_new-N_old
    #for i in range(diff):
    for i in range(diff):
        reward.append(df.loc[(N_old+i),'reward'])
        reward_accum.append(sum(df.loc[:(N_old+i), 'reward'].tolist()))
        acc_state.append(df.loc[(N_old+i),'acc_state'])
        quant_state.append(df.loc[(N_old+i),'quant_state'])
        episode_num.append(df.loc[(N_old+i),'episode_num'])

    lst = df.values[N_old+diff-1].tolist()
    layers_bits_list = lst[-8:]

    N_old = N_new
    line_labels=episode_num
    line_values=acc_state
    #return render_template('line_chart.html', title='UCSD_ACT_rl-board', max=1, labels=line_labels, values1 = acc_state, values2 = quant_state)
    return render_template('line_chart.html', title='UCSD_ACT_rlboard', max=1, labels=line_labels, values=[acc_state, quant_state, reward, reward_accum, layers_bits_list, layers_labels])

"""
@app.route('/bar')
def bar():
    global ACC_value, ACC_label
    global ACC_value_array, ACC_label_array
    global count
    if count == len(ACC_values_history): 
        count = 0
    else: count+=1
    
    ACC_value = ACC_values_history[count]
    ACC_label = count
    print(ACC_label, ACC_value)
    ACC_value_array.append(ACC_value)
    ACC_label_array.append(ACC_label)
    return render_template('bar_chart.html', title='RL Agent ACCURCY', max=17000, labels=ACC_label_array, values=ACC_value_array)
    #return render_template('bar_chart.html', title='RL Agent ACCURCY', max=17000, labels=str(ACC_label), values=str(ACC_value))
    #return render_template('bar_chart.html', title='RL Agent ACCURCY', max=17000, labels=ACC_labels_history, values=ACC_values_history)

"""
"""
@app.route('/bar')
def bar():
    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)
"""

@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors))

if __name__ == '__main__':

    global ACC_value, ACC_label

    ACC_values_history = [80, 80 ,80, 75, 50, 0.5, 0.5, 0.5, 50, 75, 80, 80, 80]
    ACC_labels_history = []
    for i in range(len(ACC_values_history)):
        ACC_labels_history.append(i)

    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=6000, debug=True)

    '''
    while True:
        for i in range(len(ACC_values_history)):
            time.sleep(2)
            ACC_value = ACC_values_history[i]
            ACC_label = i
            print('---------------')
            app.run(host='0.0.0.0', port=5000, debug=True)
    '''
