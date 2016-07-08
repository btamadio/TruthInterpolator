#!/usr/bin/env python
import ROOT,array,subprocess
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

f=ROOT.TFile.Open('output.root')
srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']
fileNames=['m4_b1','m4_b9','m5_b1','m5_b9']
can=[]
counter=0
ROOT.gStyle.SetPaintTextFormat('1.2f')
for i in range(len(srList)):
    for j in range(len(mjList)):
        if i==i and j==j:
            can.append(ROOT.TCanvas('c_'+str(counter),'c_'+str(counter),800,600))

            h1=f.Get('h_recoEff_'+srList[i]+'_'+mjList[j]).Clone('h_reco_'+srList[i]+'_'+mjList[j])
            h2=f.Get('h_truthEff_'+srList[i]+'_'+mjList[j]).Clone('h_truth_'+srList[i]+'_'+mjList[j])
            for xBin in range(1,h1.GetNbinsX()+1):
                for yBin in range(1,h1.GetNbinsY()+1):
                    val = 0
                    if h2.GetBinContent(xBin,yBin)!=0:
                        val = h1.GetBinContent(xBin,yBin)/h2.GetBinContent(xBin,yBin)
                    else:
                        val = 0
                    h1.SetBinContent(xBin,yBin,val)
            xBin=0
            for yBin in range(1,h1.GetNbinsY()+1):            
                h1.SetBinContent(xBin,yBin,0.0)
            can[-1].cd()
            h1.SetMarkerSize(1.75)
            h1.Draw('text')
            h1.GetXaxis().SetRangeUser(550,1950)
            h1.GetXaxis().SetTickLength(0)
            h1.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
            h1.GetXaxis().SetTitleOffset(1.6)
            h1.GetXaxis().SetLabelOffset(999)

            
            h1.GetYaxis().SetRangeUser(-50,1750)
            h1.GetYaxis().SetTickLength(0)
            h1.GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
            h1.GetYaxis().SetTitleOffset(1.6)
            h1.GetYaxis().SetLabelOffset(999)

            counter+=1
            line = ROOT.TLine()
            line.SetLineStyle(2)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kGray)
            for xi in range(750,2050,100):
                line.DrawLine(xi,0,xi,1750)
            for yi in range(150,1850,200):
                line.DrawLine(675,yi,1975,yi)
            ROOT.ATLASLabel(0.2,0.875,'Simulation Internal')
            lat = ROOT.TLatex()
            lat.DrawLatex(750,1350,'#int L dt = 5.8 fb^{-1}')
            lat.DrawLatex(750,1150,'#bf{'+srList[i]+' M_{J}^{#Sigma} > '+mjList[j]+'}')
            lat.DrawLatex(750,950,'#varepsilon_{reco}/#varepsilon_{truth}')

            t=ROOT.TText()
            t.SetTextAngle(0)
            t.SetTextSize(0.05)
            t.SetTextAlign(33)
            
            for x in range(800,2000,100):
                t.DrawText(x+37.5,-50,str(x/1000.))
            for y in range(50,1850,200):
                t.DrawText(667.5,y+37.5,str(y))
            can[-1].RedrawAxis()
            fileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/DetectorEfficiency/07_07/detector_efficiency_RPV10_'
            fileName+=fileNames[i]+'_MJ_'+mjList[j]+'_13000'
            can[-1].Print(fileName+'.pdf')
            can[-1].Print(fileName+'.png')
            can[-1].Print(fileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/DetectorEfficiency/07_07/*',shell=True)

