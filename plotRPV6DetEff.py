#!/usr/bin/env python
import argparse,ROOT,sys,pprint,array
from pointDictTruth import pointDictTruth
from pointDict import pointDict
import ROOT,array,subprocess,math
fReco=ROOT.TFile.Open('../HistMaker/hists/RPV6/nominal.root')
fTruth=ROOT.TFile.Open('../HistMaker/hists/RPV6Truth/nominal.root')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

lumi = 5.8

srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']
srFileNames=['m4_b1','m4_b9','m5_b1','m5_b9']

massDict = {}

for key in fTruth.GetListOfKeys():
    if 'SRyield_4' in key.GetName():
        dsid = int(key.GetName().split('_')[2])
        mG = pointDictTruth[dsid][0]
        if mG % 100 == 0:
            massDict[mG]=[]
            massDict[mG].append(dsid)

for key in pointDict:
    if pointDict[key][1]==0:
        mG = pointDict[key][0]
        dsid = key
        massDict[mG].append(dsid)
can = []
srBin = 0
effHists=[]
j=-1
for sr in srList:
    j+=1
    for mj in mjList:
        srBin+=1
        can.append(ROOT.TCanvas('c_'+str(srBin),'c_'+str(srBin),800,600))
        can[-1].cd()
        effHists.append(ROOT.TH1F('h_eff_'+sr+'_'+mj,'h_eff_'+sr+'_'+mj,10,0.850,1.850))
        for key in massDict:
            if len(massDict[key]) > 1:
                hTruth = fTruth.Get('h_SRyield_'+str(massDict[key][0]))
                hReco = fReco.Get('h_SRyield_'+str(massDict[key][1]))

                hTruth_uw = fTruth.Get('h_SRyield_unweighted_'+str(massDict[key][0]))
                hReco_uw = fReco.Get('h_SRyield_unweighted_'+str(massDict[key][1]))
                hInitReco_uw = fReco.Get('h_initEvents_'+str(massDict[key][1]))

                #this ratio will give us the central values
                xSec = pointDict[massDict[key][1]][2]
                effReco = hReco.GetBinContent(srBin) / (1E6*lumi*xSec)
                effTruth = hTruth.GetBinContent(srBin) / (1E6*lumi*xSec)

                #statistical uncertainty
                eReco = hReco_uw.GetBinContent(srBin)/hInitReco_uw.GetBinContent(1)
                eTruth = hTruth_uw.GetBinContent(srBin)/100000.
                uncertReco = math.sqrt(eReco*(1-eReco)/hInitReco_uw.GetBinContent(1))
                uncertTruth = math.sqrt(eTruth*(1-eTruth)/100000.)
                uncertTotal = (uncertReco*uncertReco)/(effReco*effReco)
                uncertTotal += (uncertTruth*uncertTruth)/(effTruth*effTruth)
                uncertTotal *= (effReco*effReco)/(effTruth*effTruth)
                uncertTotal = math.sqrt(uncertTotal)
                mG = key
                effHists[-1].Fill(mG/1000.,effReco/effTruth)
                bin = effHists[-1].FindBin(mG/1000.)
                effHists[-1].SetBinError(bin,uncertTotal)

        effHists[-1].SetLineColor(ROOT.kBlue)
        effHists[-1].SetFillColor(ROOT.kBlue-10)
        effHists[-1].Draw('hist')
        effHists[-1].Draw('e same')
        effHists[-1].GetYaxis().SetTitle('#varepsilon_{reco}/#varepsilon_{truth}')
        effHists[-1].GetYaxis().SetTitleOffset(1.5)
        effHists[-1].GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
        effHists[-1].SetMinimum(0.5)
        effHists[-1].SetMaximum(1.25)
        lat = ROOT.TLatex()
        lat.DrawLatexNDC(0.2,0.775,'#bf{'+sr+' M_{J}^{#Sigma} > '+mj+'}')
        ROOT.ATLASLabel(0.2,0.875,'Simulation Internal')

        fileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/DetectorEfficiency/07_07/detector_efficiency_RPV6_'
        fileName+=srFileNames[j]+'_MJ_'+mj+'_13000'
        print fileName
        can[-1].Print(fileName+'.pdf')
        can[-1].Print(fileName+'.png')
        can[-1].Print(fileName+'.pdf')
        
#        can[-1].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/DetectorEfficiency/07_07/
#        can[-1].Print('/global/project/projectdirs/atlas/www/btamadio/
