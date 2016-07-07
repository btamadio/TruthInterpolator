#!/usr/bin/env python
import ROOT,array,subprocess
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()


limits = [48.8,39.0,30.1,24.2,19.7,
          98.9,69.9,51.5,38.1,29.1,
          12.7,11.2,9.7,8.8,7.5,
          17.5,14.8,12.8,11.2,9.9]

srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']
f=ROOT.TFile.Open('output.root')
can=[]
limitCounter=0
lat = ROOT.TLatex()
ROOT.gStyle.SetPaintTextFormat('1.1f')
contList=[]
grs=[]
colors=[ROOT.kRed,ROOT.kGreen,ROOT.kBlue,ROOT.kYellow,ROOT.kViolet]
legs = []
for i in range(len(srList)):
    contList.append([])
    can.append(ROOT.TCanvas('c_'+str(i),'c_'+str(i),800,600))
    can[i].cd()
    firstDrawn=False
    for mj in mjList:
        h=f.Get('h_recoYield_nom_interp_'+srList[i]+'_'+mj)
        print h
        h.SetContour(1,array.array('d',[limits[limitCounter]]))
        h.Draw('cont z list')
        can[i].Update()
        contourTList = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
        for cont in contourTList:
            for c in cont:
                contList[i].append(c.Clone('yieldGraph_'+'_'+srList[i]+'_'+mj))
        for j in range(len(contList[i])):
            cont = contList[i][j]
            cont.SetLineColor(colors[j])
            cont.SetLineWidth(2)
            if j==0:
                cont.Draw('AL')
                cont.GetXaxis().SetLimits(700,2000)
                cont.GetYaxis().SetRangeUser(50,2000)
            else:
                cont.Draw('lsame')
        limitCounter+=1
    xVec = [700,1000,1000,700]
    yVec = [0,0,2200,2200]
    grs.append(ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec)))
    grs[-1].SetFillColor(10)
    grs[-1].Draw('FSAME')
    can[i].RedrawAxis()
    ROOT.ATLASLabel(0.2,0.875,'Simulation Internal')
    lat.DrawLatex(800,1500,'#int L dt = 5.8 fb^{-1}')
    lat.DrawLatex(800,1200,srList[i])
    legs.append(ROOT.TLegend(0.7,0.5,0.95,0.9))

    for j in range(len(contList[i])):
        legs[i].AddEntry(contList[i][j],'M_{J}^{#Sigma} > '+mjList[j],'l')
    legs[i].SetBorderSize(0)
    legs[i].SetFillStyle(0)
    legs[i].SetTextSize(0.04)
    legs[i].Draw()
            
