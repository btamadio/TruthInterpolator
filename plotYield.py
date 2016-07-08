#!/usr/bin/env python
import ROOT,array,subprocess
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

lumi = 5.8

f=ROOT.TFile.Open('output.root')
srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjList = ['600','650','700','750','800']
fileNames=['m4_b1','m4_b9','m5_b1','m5_b9']
srLabs = ['#splitline{b-tag        |#eta| < 1.4}{N_{fatjet} #geq 4}',
          '#splitline{b-inclusive  |#eta| < 1.4}{N_{fatjet} #geq 4}',
          '#splitline{b-tag        |#eta| < 1.4}{N_{fatjet} #geq 5}',
          '#splitline{b-inclusive  |#eta| < 1.4}{N_{fatjet} #geq 5}']
can=[]
counter=0
gr3=[]

ROOT.gStyle.SetPaintTextFormat('1.1f')
for i in range(len(srList)):
    for j in range(len(mjList)):
        h0=f.Get('h_recoYield_nom_'+srList[i]+'_'+mjList[j]).Clone('h_reco_'+srList[i]+'_'+mjList[j])
        hInterp=f.Get('h_recoYield_nom_interp_'+srList[i]+'_'+mjList[j]).Clone('h_reco_'+srList[i]+'_'+mjList[j])
        hists=[h0,hInterp]
        for k in range(len(hists)):
            h1=hists[k]
            can.append(ROOT.TCanvas('c_'+str(counter),'c_'+str(counter),800,600))
            can[-1].cd()
            if k == 0:
                h1.SetMarkerSize(1.75)
            else:
                h1.SetMarkerSize(0.85)
            h1.Scale(lumi/5.8)
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

            ROOT.ATLASLabel(0.2,0.875,'Simulation Internal')
            lat = ROOT.TLatex()
            lat.DrawLatex(750,1375,'#int L dt = '+str(lumi)+' fb^{-1}')
            lat.DrawLatex(750,1125,srLabs[i])
            lat.DrawLatex(750,925,'M_{J}^{#Sigma} > '+mjList[j])

            t=ROOT.TText()
            t.SetTextAngle(0)
            t.SetTextSize(0.05)
            t.SetTextAlign(33)

            #Run 1 limit
            run1Pairs=[(889,65.62),(893.4,96.88),(897.9,128.1),(899.4,159.4),( 901,190.6),( 902.5,221.9),( 908.1,253.1),( 912.5,257.6),(930.6,284.4),(937.5,294),(953,315.6),(962.5,328.7),(975.9,346.9),(987.5,362.5),(996.1,378.1),(1012,407.7),(1013,409.4),(1035,440.6),(1038,454.1),(1041,471.9),(1038,488.1),(1034,503.1),(1028,534.4),(1022,565.6),(1027,596.9),(1012,618.7),(993,628.1),(987.5,629.7),(962.5,640.1),(937.5,652),(922.1,659.4),(912.5,664),(887.5,676.1),(862.5,688.1),(859,690.6),(837.5,708.9),(822.7,721.9),(812.5,731.3)]
            xVec=[p[0] for p in run1Pairs]
            yVec=[p[1] for p in run1Pairs]
            gr3.append(ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec)))
            gr3[-1].SetLineWidth(2)
            gr3[-1].SetLineColor(ROOT.kRed)
            gr3[-1].SetLineStyle(2)
            gr3[-1].Draw('LSAME')
            
            for x in range(800,2000,100):
                t.DrawText(x+37.5,-50,str(x/1000.))
            for y in range(50,1850,200):
                t.DrawText(667.5,y+37.5,str(y))
            can[-1].RedrawAxis()
            lumiStr = str(lumi).split('.')[0]+'p'+str(lumi).split('.')[1]+'fb'
            fileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/07_08_'+lumiStr+'/SignalYield_RPV10_'
            if k==1:
                fileName+='interp_'
            fileName+=fileNames[i]+'_MJ_'+mjList[j]+'_13000'
            can[-1].Print(fileName+'.pdf')
            can[-1].Print(fileName+'.png')
            can[-1].Print(fileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/07_08_'+lumiStr+'/*',shell=True)

