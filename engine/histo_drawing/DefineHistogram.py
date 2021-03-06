from ROOT import *
import os

if not os.path.exists("app/static/plots"):
    os.system("mkdir app/static/plots")

def GetAPlot(hist,histname, username="anonimous", opt_stats_mode = "emr"):
    """ Looks for a png files. If it is not there,
    it produces it by saving a ROOT histogram  as .png """
    #if not os.path.isfile("app/static/plots/"+histname+".png"):
    gStyle.SetOptStat(opt_stats_mode)
    gStyle.SetPadTopMargin(0.06) 
    c = TCanvas("c","c", 900, 900)
    #hist.GetYaxis().SetRangeUser(hist.GetBinContent(hist.GetMinimumBin())-0.2*diff, hist.GetBinContent(hist.GetMaximumBin())+0.2*diff);
    hist.SetTitle(histname.split("_")[-1])
    hist.Draw()
    #print histname + " nEntries: " + str(hist.GetEntries())
    c.SaveAs("app/static/plots/"+histname+".png")
    dic = {"plot":"plots/"+histname+".png", "owner":username,  "init_properties":{}, "properties":{'mean':hist_mean(hist)
                                                            , 'sigma':hist_sigma(hist)
                                                            , 'Y_mean':Y_mean(hist)
                                                            , 'slope':slope(hist)
                                                            , 'smoothness':chi2_lin(hist)
                                                            , 'max_variation':max_variation(hist)
                                                            , 'max_y':max_y(hist)
                                                            , 'min_y':min_y(hist)
                                                            }}
    for p in dic['properties']:
        dic['init_properties'][p]=dic['properties'][p]

    return dic

def hist_mean(hist):
    return hist.GetMean()

def hist_sigma(hist):
    return hist.GetRMS()

def Y_mean(hist):
    #return 0
    hist.Fit("pol0","QW") #q - to make fit silent, w - ignore empty bins
    f = hist.GetFunction("pol0")
    try:
        return f.GetParameter(0)
    except:
        return 0

def slope(hist):
    #return 0
    hist.Fit("pol1","QW") #q - to make fit silent, w - ignore empty bins 
    f = hist.GetFunction("pol1")
    try:
        return f.GetParameter(1)
    except:
        return 0

def chi2_lin(hist):
    return 0
    hist.Fit("pol1","QW") #q - to make fit silent, w - ignore empty bins
    f = hist.GetFunction("pol1")
    try:
        return f.GetChisquare()
    except:
        return 0

def max_variation(hist):
    #return 0
    mean = Y_mean(hist)
    var = 0
    for i in range(1, hist.GetXaxis().GetNbins()+1):
        if hist.GetBinError(i)>0:
            if (hist.GetBinContent(i)-mean)/hist.GetBinError(i)>var:
                var = (hist.GetBinContent(i)-mean)/hist.GetBinError(i)
    return var


def min_y(hist):
    #return 0
    return hist.GetBinContent(hist.GetMinimumBin())

def max_y(hist):
    return hist.GetBinContent(hist.GetMaximumBin()) 
    try:
        return hist.GetBinContent(133)
    except:
        return hist.GetBinContent(hist.GetMaximumBin()) 
    