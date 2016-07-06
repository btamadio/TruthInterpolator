#!/usr/bin/env python
from pointDictTruth import pointDictTruth
import ROOT
class TruthInterpolator:
    def __init__(self,truthFileName='/project/projectdirs/atlas/btamadio/RPV_SUSY/HistMaker/hists/RPV10Truth/nominal.root',recoFileName='/project/projectdirs/atlas/btamadio/RPV_SUSY/HistMaker/hists/RPV10/nominal.root'):
        self.truthFile=ROOT.TFile.Open(truthFileName)
        self.recoFile=ROOT.TFile.Open(recoFileName)
        self.pointDictTruth=pointDictTruth
        self.srList = ['4jSRb1','4jSR','5jSRb1','5jSR']
        self.mjList = ['600','650','700','750','800']
        self.truthEffHist = []
        self.truthEffXsec=[]
        self.truthEffXsec_1up = []
        self.truthEffXsec_1down = []
        self.outFile=ROOT.TFile('output.root','RECREATE')
        for i in range(len(self.srList)):
            for j in range(len(self.mjList)):
                self.truthEffHist.append(ROOT.TH2D('h_truthEff_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency',24,725,1925,37,25,1875))
                self.truthEffXsec.append(ROOT.TH2D('h_truthEff_xsec_nom_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.truthEffXsec_1up.append(ROOT.TH2D('h_truthEff_xsec_1up_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.truthEffXsec_1down.append(ROOT.TH2D('h_truthEff_xsec_1down_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))

    def makeTruthEffHists(self):
        for key in self.truthFile.GetListOfKeys():
            if 'h_SRyield' in key.GetName():
                h = self.truthFile.Get(key.GetName())
                dsid = key.GetName().split('_')[2]
                mG = pointDictTruth[int(dsid)][0]
                mX = pointDictTruth[int(dsid)][1]
                xsec = pointDictTruth[int(dsid)][2]
                xsec_uncert = pointDictTruth[int(dsid)][3]/100.
                xsec_1up = xsec*(1+xsec_uncert)
                xsec_1down = xsec*(1-xsec_uncert)
                lumi = 5.8E6
                for i in range(h.GetNbinsX()):
                    self.truthEffHist[i].Fill(mG,mX,h.GetBinContent(i+1)/(xsec*lumi))
                    self.truthEffXsec[i].Fill(mG,mX,h.GetBinContent(i+1)/(lumi))
                    self.truthEffXsec_1up[i].Fill(mG,mX,h.GetBinContent(i+1)*xsec_1up/(xsec*lumi))
                    self.truthEffXsec_1down[i].Fill(mG,mX,h.GetBinContent(i+1)*xsec_1down/(xsec*lumi))
    def writeFile(self):
        self.outFile.Write()
p = TruthInterpolator()
p.makeTruthEffHists()
p.writeFile()
