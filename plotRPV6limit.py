#!/usr/bin/env python

from pointDict import pointDict
from pointDictTruth import pointDictTruth
from pointDict8TeV import pointDict8TeV

pb = 1.0E-3

import ROOT,array,subprocess
f=ROOT.TFile.Open('../HistMaker/hists/RPV6/nominal.root')

lumi = 13.277
sr = '5jSRb1'
mj = '600'
expLimit=[7.1,8.6,12.8,18.3,27.7]
obsLimit=26.9

ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

srList=['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']

srBin = 5*srList.index(sr) + mjList.index(mj) + 1
xVals = range(900,1850,50)

yVals = {'median':[],
         '1up':[],
         '1down':[],
         '2up':[],
         '2down':[],
         'observed':[],
         'xsec8_1up':[],
         'xsec8_1down':[],
         'xsec13_1up':[],
         'xsec13_1down':[]}
effDict = {}

for runNumber in range(403605,403615):
    mG = pointDict[runNumber][0]
    h_SRyield=f.Get('h_SRyield_'+str(runNumber))
    h_cutflow=f.Get('h_cutflow_'+str(runNumber))
    effDict[mG] = h_SRyield.GetBinContent(srBin) / h_cutflow.GetBinContent(2)

def interpolate(m1,m2,m3,e1,e3):
    return e1+(e3-e1)*(m2-m1)/(m3-m1)

def getXsec(mass,e):
    if e == 13:
        for key in pointDictTruth:
            if pointDictTruth[key][0] == mass:
                xSec = pointDictTruth[key][2]*1E6
                uncert = pointDictTruth[key][3]
                xSec_1up = xSec*(1+uncert/100.)
                xSec_1down = xSec*(1-uncert/100.)
                return(xSec_1up,xSec_1down)
    elif e == 8:
        for key in pointDict8TeV:
            if pointDict8TeV[key][0] == mass:
                xSec = pointDict8TeV[key][2]*1E6
                uncert = pointDict8TeV[key][3]
                xSec_1up = xSec*(1+uncert/100.)
                xSec_1down = xSec*(1-uncert/100.)
                return(xSec_1up,xSec_1down)

for xVal in xVals:
    if xVal not in effDict:
        effDict[xVal] = interpolate(xVal-50,xVal,xVal+50,effDict[xVal-50],effDict[xVal+50])
    yVals['2down'].append( expLimit[0]*pb / (effDict[xVal]*lumi) )
    yVals['1down'].append( expLimit[1]*pb / (effDict[xVal]*lumi) )
    yVals['median'].append( expLimit[2]*pb / (effDict[xVal]*lumi) )
    yVals['1up'].append( expLimit[3]*pb / (effDict[xVal]*lumi) )
    yVals['2up'].append( expLimit[4]*pb / (effDict[xVal]*lumi) )
    yVals['observed'].append( obsLimit*pb / (effDict[xVal]*lumi) )
    yVals['xsec8_1up'].append( getXsec(xVal,8)[0]*pb )
    yVals['xsec8_1down'].append( getXsec(xVal,8)[1]*pb )
    yVals['xsec13_1up'].append( getXsec(xVal,13)[0]*pb )
    yVals['xsec13_1down'].append( getXsec(xVal,13)[1]*pb )
    
xVals.insert(0,900)
xVals.append(1800)

c1 = ROOT.TCanvas('c1','c1',800,600)
c1.cd()
c1.SetLogy()

denom = 5.0
graphs = {}
for key in yVals:
    yVals[key].insert(0,yVals[key][0]/denom)
    yVals[key].append(yVals[key][-1]/denom)
    if key != 'median' and key != 'observed' and 'xsec' not in key:
        graphs[key] = ROOT.TGraph(len(xVals),array.array('d',xVals),array.array('d',yVals[key]))
    elif 'xsec' not in key:
        graphs[key] = ROOT.TGraph(len(xVals)-2,array.array('d',xVals[1:-1]),array.array('d',yVals[key][1:-1]))
    elif key == 'xsec13_1up':
        xValsXsec = xVals[1:-1]+list(reversed(xVals[1:-1]))
        yValsXsec = yVals[key][1:-1]+list(reversed(yVals['xsec13_1down']))
        graphs['xsec13'] = ROOT.TGraph(len(xValsXsec),array.array('d',xValsXsec),array.array('d',yValsXsec))
    elif key == 'xsec8_1up':
        xValsXsec = xVals[1:-1]+list(reversed(xVals[1:-1]))
        yValsXsec = yVals[key][1:-1]+list(reversed(yVals['xsec8_1down']))
        graphs['xsec8'] = ROOT.TGraph(len(xValsXsec),array.array('d',xValsXsec),array.array('d',yValsXsec))
        
graphs['2up'].SetFillColor(5)
graphs['1up'].SetFillColor(3)
graphs['1down'].SetFillColor(5)
graphs['2down'].SetFillColor(10)
graphs['median'].SetLineWidth(2)
graphs['median'].SetLineStyle(2)
graphs['median'].SetLineColor(1)
graphs['observed'].SetLineColor(ROOT.kRed)
graphs['observed'].SetLineWidth(2)
graphs['xsec8'].SetFillColor(16)
graphs['xsec13'].SetFillColor(12)


graphs['2up'].Draw('AF')
graphs['2up'].GetXaxis().SetLimits(880,1820)
graphs['2up'].GetYaxis().SetRangeUser(1E-3,10)
graphs['2up'].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
#graphs['2up'].GetYaxis().SetTitle('#sigma(pp#rightarrow#tilde{g}#tilde{g}#rightarrow6q) [pb]')
graphs['2up'].GetYaxis().SetTitle('#sigma [pb]')
graphs['1up'].Draw('FSAME')
graphs['1down'].Draw('FSAME')
graphs['2down'].Draw('FSAME')
#graphs['xsec8'].Draw('FSAME')
graphs['xsec13'].Draw('FSAME')
graphs['median'].Draw('LSAME')
graphs['observed'].Draw('LSAME')

leg = ROOT.TLegend(0.2,0.75,0.4,0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.03)

leg.AddEntry(graphs['observed'],'Observed 95% CL Limit','l')
leg.AddEntry(graphs['median'],'Expected Limit','l')
leg.AddEntry(graphs['1up'],'#pm 1 #sigma Exp Limit','f')
leg.AddEntry(graphs['2up'],'#pm 2 #sigma Exp Limit','f')
leg.AddEntry(graphs['xsec13'],'#tilde{g}#tilde{g} Cross-section (NLO+NLL)','f')
#leg.AddEntry(graphs['xsec8'],'8 TeV #tilde{g}#tilde{g} Cross-section (NLO+NLL)','f')
leg.Draw()

lat = ROOT.TLatex()
ROOT.ATLASLabel(0.65,0.88,'Internal')
lat.DrawLatexNDC(0.625,0.8,'#sqrt{s} = 13 TeV, 13.3 fb^{-1}')
lat.DrawLatex(880+55,12.5,'#scale[0.5]{#tilde{g}-#tilde{g} production, #tilde{g}#rightarrow 6q}')

lumiStr='13p3fb'
c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_24_'+lumiStr+'/limit_RPV6_m5_b1_MJ_'+mj+'_13000.pdf')
c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_24_'+lumiStr+'/limit_RPV6_m5_b1_MJ_'+mj+'_13000.png')
c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_24_'+lumiStr+'/limit_RPV6_m5_b1_MJ_'+mj+'_13000.C')
p=subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_24_'+lumiStr+'/*',shell=True)
