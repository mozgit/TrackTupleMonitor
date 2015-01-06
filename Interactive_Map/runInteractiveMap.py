from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for, request, flash
from ROOT import *
from CreateDetectors import *

import pickle
f = open('NameList.pkl')
NameList = pickle.load(f)

gROOT.SetBatch(kTRUE)


tt_d = create_TT()
it_d = create_IT()
f = open('TT_Efficiency_Per_Run.pkl')
TT_hists = pickle.load(f)



hname ='Efficiency_time_dependence'
Add_Histograms(tt_d, TT_hists, hname)

for h in GetHistosFromNT('data/STTrackMonitor-2012.root'):
    if h[0] == 'T':
        f = open(h+".pkl")
        TT_hists = pickle.load(f)
        Add_Histograms(tt_d, TT_hists, h)
    if h[0] == 'I':
        f = open(h+".pkl")
        IT_hists = pickle.load(f)
        Add_Histograms(it_d, IT_hists, h)

app = Flask(__name__)


@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    global Drawing_mode
    if request.method == 'POST':
        #Drawing_mode['TT_hist'] = 'Efficiency_time_dependence'
        #Drawing_mode['form']=request.form['TT_hist']
        for m in ['IT_hist', 'TT_hist']:
            try:
                Drawing_mode[m]=request.form[m]
            except:
                pass
        return render_template('index.html', tt = tt_d, it=it_d, dm = Drawing_mode)
    Drawing_mode = {'TT_hist':'', 'IT_hist':''}
    return render_template('index.html', tt = tt_d, it=it_d, dm = Drawing_mode)
    #return "Hello World!"

@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    """
    if d == "IT":
        if request.method == 'POST':
            return render_template('IT.html', it=it_d)
        return render_template('IT.html', it=it_d)
    if d == "TT":
        if request.method == 'POST':
            return render_template('TT.html', tt=tt_d)
        return render_template('TT.html', tt=tt_d)
    """
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', sec=tt_d[p_name['layer']][p_name['side']][p_name['sector']], histoname = hname)
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', sec=it_d[p_name['station']][p_name['side']][p_name['layer']][p_name['sector']], histoname = hname)
    return redirect(url_for('hello'))
    #return render_template('Sector.html', sec=d)

if __name__ == "__main__":
    Drawing_mode = {'TT_hist':'', 'IT_hist':''}
    app.debug = True
    app.run()