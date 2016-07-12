#!/usr/bin/env python

from pointDict import pointDict
from pointDictTruth import pointDictTruth

sr = '4jSRb1'
mj = '600'

pb = 1.0E-3

import ROOT,array,subprocess
f=ROOT.TFile.Open('../HistMaker/hists/RPV6/nominal.root')

#alternate CR
#4jSRb1 MJ > 800
#lumi = 8.9
#expLimit=[10.8,16.0,23.0,33.2,46.0]
#obsLimit = 13.6

#4jSRb1 MJ > 600
#lumi = 8.9
#expLimit=[37.0,52.5,72,100,132]
#obsLimit = 60.5

#5jSRb1
#expLimit=[4.6,6.1,8.7,12.2,18.6]
#obsLimit=15.1


#baseline
#4jSRb1 limits
#lumi = 8.9
#expLimit=[9.4,14.0,20.0,29.1,41.2]
#obsLimit = 12.6

#5jSRb1, MJ > 600 limits:
#lumi = 8.9
#expLimit = [5.5,6.9,9.4,14.3,20.5]
#obsLimit = 13.1

#4jSRb1 MJ > 600
lumi = 8.9
expLimit=[40.5,53.5,74,101,134]
obsLimit = 72

#lumi = 5.8
#expLimit = [4.3,5.8,8.2,11.9,18.5]
#obsLimit = 10.2


ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

srList=['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']

srBin = 5*srList.index(sr) + mjList.index(mj) + 1
print 'srBin = ',srBin
xVals = range(900,1850,50)

yVals = {'median':[],
         '1up':[],
         '1down':[],
         '2up':[],
         '2down':[],
         'observed':[],
         'xsec_1up':[],
         'xsec_1down':[]}
effDict = {}

for runNumber in range(403605,403615):
    mG = pointDict[runNumber][0]
    h_SRyield=f.Get('h_SRyield_'+str(runNumber))
    h_cutflow=f.Get('h_cutflow_'+str(runNumber))
    effDict[mG] = h_SRyield.GetBinContent(srBin) / h_cutflow.GetBinContent(2)

def interpolate(m1,m2,m3,e1,e3):
    return e1+(e3-e1)*(m2-m1)/(m3-m1)

def getXsec(mass):
    for key in pointDictTruth:
        if pointDictTruth[key][0] == mass:
            xSec = pointDictTruth[key][2]*1E6
            uncert = pointDictTruth[key][3]
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
    yVals['xsec_1up'].append( getXsec(xVal)[0]*pb )
    yVals['xsec_1down'].append( getXsec(xVal)[1]*pb )
    
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
    elif key == 'xsec_1up':
        xValsXsec = xVals[1:-1]+list(reversed(xVals[1:-1]))
        yValsXsec = yVals[key][1:-1]+list(reversed(yVals['xsec_1down']))
        graphs['xsec'] = ROOT.TGraph(len(xValsXsec),array.array('d',xValsXsec),array.array('d',yValsXsec))
        
graphs['2up'].SetFillColor(5)
graphs['1up'].SetFillColor(3)
graphs['1down'].SetFillColor(5)
graphs['2down'].SetFillColor(10)
graphs['median'].SetLineWidth(2)
graphs['median'].SetLineStyle(2)
graphs['median'].SetLineColor(1)
graphs['observed'].SetLineColor(1)
graphs['observed'].SetLineWidth(2)
graphs['xsec'].SetFillColor(12)

graphs['2up'].Draw('AF')
graphs['2up'].GetXaxis().SetLimits(800,1900)
graphs['2up'].GetYaxis().SetRangeUser(1E-3,10)
graphs['2up'].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
graphs['2up'].GetYaxis().SetTitle('#sigma(pp#rightarrow#tilde{g}#tilde{g}#rightarrow6q) [pb]')
graphs['1up'].Draw('FSAME')
graphs['1down'].Draw('FSAME')
graphs['2down'].Draw('FSAME')
graphs['xsec'].Draw('FSAME')
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
leg.AddEntry(graphs['xsec'],'#tilde{g}#tilde{g} Cross-section (NLO+NLL)','f')
leg.Draw()

lat = ROOT.TLatex()
ROOT.ATLASLabel(0.2,0.25,'Internal')
lat.DrawLatexNDC(0.2,0.35,'#sqrt{s} = 13 TeV, '+str(lumi)+' fb^{-1}')

lumiStr=str(lumi).split('.')[0]+'p'+str(lumi).split('.')[1]+'fb'

c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'/limit_RPV6_m4_b1_MJ_'+mj+'_13000.pdf')
c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'/limit_RPV6_m4_b1_MJ_'+mj+'_13000.png')
c1.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'/limit_RPV6_m4_b1_MJ_'+mj+'_13000.C')

p=subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'/*',shell=True)
