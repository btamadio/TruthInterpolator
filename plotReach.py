#!/usr/bin/env python
import ROOT,array,subprocess
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

lumi = 8.9

#limits = [48.8,39.0,30.1,24.2,19.7,
#          98.9,69.9,51.5,38.1,29.1,
#          12.7,11.2,9.7,8.8,7.5,
#          17.5,14.8,12.8,11.2,9.9]
limits = [81.0, 57.8, 44.4, 33.8, 28.7, 
          189.0, 119.6, 82.5, 57.8, 43.3, 
          13.2, 11.4, 9.7, 8.9, 8.1, 23.2, 
          19.5, 15.9, 13.0, 11.5]

srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']
fileNames=['m4_b1','m4_b9','m5_b1','m5_b9']
f=ROOT.TFile.Open('output.root')
can=[]
limitCounter=0
lat = ROOT.TLatex()
ROOT.gStyle.SetPaintTextFormat('1.1f')
contList=[]
grs=[]
colors=[ROOT.kRed,ROOT.kGreen,ROOT.kBlue,ROOT.kYellow,ROOT.kViolet]
legs = []
gr3=[]
for i in range(len(srList)):
    contList.append([])
    can.append(ROOT.TCanvas('c_'+str(i),'c_'+str(i),800,600))
    can[i].cd()
    firstDrawn=False
    for mj in mjList:
        h=f.Get('h_recoYield_nom_interp_'+srList[i]+'_'+mj)
        h.SetContour(1,array.array('d',[limits[limitCounter]]))
        h.Draw('cont z list')
        can[i].Update()
        contourTList = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
        for cont in contourTList:
            for c in cont:
                if c.GetRMS(1) > 25:
                    contList[i].append(c.Clone('yieldGraph_'+'_'+srList[i]+'_'+mj))
        for j in range(len(contList[i])):
            cont = contList[i][j]
            cont.SetLineColor(colors[j])
            cont.SetLineWidth(2)
            if j==0:
                cont.Draw('AL')
                cont.GetXaxis().SetLimits(700,2000)
                cont.GetYaxis().SetRangeUser(50,2000)
                cont.GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
                cont.GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')

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
    lat.DrawLatex(800,1500,'#int L dt = '+str(lumi)+' fb^{-1}')
    lat.DrawLatex(800,1200,'#bf{'+srList[i]+'}')
    legs.append(ROOT.TLegend(0.7,0.5,0.95,0.9))

    for j in range(len(contList[i])):
        legs[i].AddEntry(contList[i][j],'M_{J}^{#Sigma} > '+mjList[j],'l')
    legs[i].SetBorderSize(0)
    legs[i].SetFillStyle(0)
    legs[i].SetTextSize(0.04)
    #Run 1 limit
    run1Pairs=[(889,65.62),(893.4,96.88),(897.9,128.1),(899.4,159.4),( 901,190.6),( 902.5,221.9),( 908.1,253.1),( 912.5,257.6),(930.6,284.4),(937.5,294),(953,315.6),(962.5,328.7),(975.9,346.9),(987.5,362.5),(996.1,378.1),(1012,407.7),(1013,409.4),(1035,440.6),(1038,454.1),(1041,471.9),(1038,488.1),(1034,503.1),(1028,534.4),(1022,565.6),(1027,596.9),(1012,618.7),(993,628.1),(987.5,629.7),(962.5,640.1),(937.5,652),(922.1,659.4),(912.5,664),(887.5,676.1),(862.5,688.1),(859,690.6),(837.5,708.9),(822.7,721.9),(812.5,731.3)]
    xVec=[p[0] for p in run1Pairs]
    yVec=[p[1] for p in run1Pairs]
    gr3.append(ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec)))
    gr3[-1].SetLineWidth(2)
    gr3[-1].SetLineColor(13)
    gr3[-1].SetLineStyle(2)
    gr3[-1].Draw('LSAME')
    legs[i].AddEntry(gr3[-1],'Run 1 limit','l')
    legs[i].Draw()
    lumiStr = str(lumi).split('.')[0]+'p'+str(lumi).split('.')[1]+'fb'
    fileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ReachPlots/07_12_'+lumiStr+'_alternateCR/reach_RPV10_'
    fileName+=fileNames[i]+'_95CL'
    can[i].Print(fileName+'.pdf')
    can[i].Print(fileName+'.png')
    can[i].Print(fileName+'.C')
subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ReachPlots/07_12_'+lumiStr+'_alternateCR/*',shell=True)
