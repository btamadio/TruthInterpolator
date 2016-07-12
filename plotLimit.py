#!/usr/bin/env python
import ROOT,array,subprocess
f=ROOT.TFile.Open('output.root')

lumi=8.9
#baseline
#expLimit = [6.9,9.4,14.3]
#obsLimit = [13.1]

#alternate CR
expLimit = [6.1,8.7,12.2]
obsLimit = [15.1]


#lumi = 5.8
#expLimit = [5.8,8.2,11.9]
#obsLimit = [10.2]
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('~/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()



sr = '5jSRb1'
mj = '600'
c1 = ROOT.TCanvas('c1','c1',800,600)
histNameNom = 'h_recoYield_nom_interp_'+sr+'_'+mj
histNameUp = 'h_recoYield_1up_interp_'+sr+'_'+mj
histNameDown = 'h_recoYield_1down_interp_'+sr+'_'+mj

hNom = f.Get(histNameNom)
hNom.Scale(lumi/5.8)
hNom.SetContour(3,array.array('d',expLimit))
hNom.Draw('cont list')
c1.Update()

contExpList = []
contObsList = []

contourTListExp = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
for cont in contourTListExp:
    for c in cont:
        contExpList.append(c.Clone('yieldGraph_'+str(len(contExpList))))
c2 = ROOT.TCanvas('c2','c2',800,600)
c2.cd()
hUp = f.Get(histNameUp)
hDown = f.Get(histNameDown)

hUp.Scale(lumi/5.8)
hDown.Scale(lumi/5.8)

hNom.SetContour(1,array.array('d',obsLimit))
hUp.SetContour(1,array.array('d',obsLimit))
hDown.SetContour(1,array.array('d',obsLimit))

hNom.Draw('cont list')
c2.Update()
contourTListObs = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
for cont in contourTListObs:
    for c in cont:
        contObsList.append(c.Clone('yieldGraphObs_'+str(len(contObsList))))


hUp.Draw('cont list')
c2.Update()
contourTListObs = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
for cont in contourTListObs:
    for c in cont:
        contObsList.append(c.Clone('yieldGraphObs_'+str(len(contObsList))))

hDown.Draw('cont list same')
c2.Update()
contourTListObs = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
for cont in contourTListObs:
    for c in cont:
        contObsList.append(c.Clone('yieldGraphObs_'+str(len(contObsList))))


contExp=[contExpList[0],contExpList[1],contExpList[2]]
c3 = ROOT.TCanvas('c3','c3',800,600)
c3.cd()
contExp[0].SetFillColor(5)
contExp[0].GetXaxis().SetTitle("m_{#tilde{g}} [GeV]")
contExp[0].GetYaxis().SetTitle("m_{#tilde{#chi}_{1}^{0}} [GeV]")
contExp[0].GetYaxis().SetTitleOffset(1.4)
contExp[0].Draw('AF')
contExp[0].GetXaxis().SetLimits(700,2200)
contExp[0].GetYaxis().SetRangeUser(50,2200)
contExp[2].SetFillColor(10)
contExp[2].Draw('FSAME')
contExp[1].SetLineStyle(2)
contExp[1].SetLineWidth(2)
contExp[1].Draw('LSAME')

contObs=[contObsList[0],contObsList[1],contObsList[2]]
contObs[1].SetLineStyle(2)
contObs[2].SetLineStyle(2)
for c in contObs:
    c.SetLineColor(ROOT.kRed)
    c.SetLineWidth(2)
    c.Draw('LSAME')

#Blocking out the weird low part of the contour
line = ROOT.TLine()
line.SetLineWidth(50)
line.SetLineColor(10)
line.DrawLine(800,50,800,1050)
line.SetLineColor(10)

#forbidden band
line.SetLineStyle(2)
line.SetLineColor(13)
line.SetLineWidth(2)
line.DrawLine(700,700,1750,1750)
line.DrawLine(1900,1900,2200,2200)
xVec=[700,2200,2200,700]
yVec=[600,2100,2200,700]
gr=ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec))
gr.SetFillColor(10)
gr.Draw('FSAME')

#Atlas and luminosity labels
ROOT.ATLASLabel(0.6,0.88,'Internal')
legLatex = ROOT.TLatex()

legLatex.DrawLatex(1500,1775,'#sqrt{s} = 13 TeV, '+str(lumi)+' fb^{-1}')

#Custom legend
xVec=[775.0,925.0,925.0,775.0]
yVec=[1950.0,1950.0,2100.0,2100.0]
gr2 = ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec))
gr2.SetFillColor(5)
gr2.Draw('FSAME')
line.SetLineColor(1)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.DrawLine(xVec[0],(yVec[2]+yVec[1])/2,xVec[1],(yVec[2]+yVec[1])/2)
legLatex.DrawLatex(950,2000,'#scale[0.65]{Expected limit (#pm1 #sigma_{exp})}')
line.SetLineColor(ROOT.kRed)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.DrawLine(775,1787.5,925,1787.5)
line.DrawLine(775,1862.5,925,1862.5)
line.SetLineStyle(1)
line.DrawLine(775,1825,925,1825)
legLatex.DrawLatex(950,1800,'#scale[0.65]{Observed limit (#pm1 #sigma^{SUSY}_{theory})}')
line.SetLineColor(13)
line.SetLineStyle(1)
line.DrawLine(775,1625,925,1625)
legLatex.DrawLatex(950,1600,'#scale[0.65]{Run 1 limit}')
legLatex.DrawLatex(800,1400,'#scale[0.65]{All limits at 95% CL}')

legLatex.DrawLatex(775,2250,'#scale[0.5]{#tilde{g}-#tilde{g} production, #tilde{g}#rightarrowqq#tilde{#chi}_{1}^{0}, #tilde{#chi}_{1}^{0}#rightarrow qqq}')

#Run 1 limit
run1Pairs=[(889,65.62),(893.4,96.88),(897.9,128.1),(899.4,159.4),( 901,190.6),( 902.5,221.9),( 908.1,253.1),( 912.5,257.6),(930.6,284.4),(937.5,294),(953,315.6),(962.5,328.7),(975.9,346.9),(987.5,362.5),(996.1,378.1),(1012,407.7),(1013,409.4),(1035,440.6),(1038,454.1),(1041,471.9),(1038,488.1),(1034,503.1),(1028,534.4),(1022,565.6),(1027,596.9),(1012,618.7),(993,628.1),(987.5,629.7),(962.5,640.1),(937.5,652),(922.1,659.4),(912.5,664),(887.5,676.1),(862.5,688.1),(859,690.6),(837.5,708.9),(822.7,721.9),(812.5,731.3)]
xVec=[p[0] for p in run1Pairs]
yVec=[p[1] for p in run1Pairs]
gr3=ROOT.TGraph(len(xVec),array.array('d',xVec),array.array('d',yVec))
#gr3.SetLineStyle(2)
gr3.SetLineWidth(2)
gr3.SetLineColor(13)
gr3.Draw('LSAME')

legLatex.SetTextAngle(26)
legLatex.DrawLatex(850,900,'#color[12]{#scale[0.55]{#tilde{g}#rightarrow qq#tilde{#chi}_{1}^{0} forbidden}}')

c3.RedrawAxis()
lumiStr=str(lumi).split('.')[0]+'p'+str(lumi).split('.')[1]+'fb'
c3.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'_alternateCR/limit_RPV10_m5_b1_MJ_600_13000.pdf')
c3.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'_alternateCR/limit_RPV10_m5_b1_MJ_600_13000.pdf')
c3.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'_alternateCR/limit_RPV10_m5_b1_MJ_600_13000.pdf')

p=subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/LimitPlots/07_08_'+lumiStr+'_alternateCR/*',shell=True)
