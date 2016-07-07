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

        self.recoYieldHist = []
        self.recoYieldHist_1up = []
        self.recoYieldHist_1down = []
        
        self.recoEffHist = []
        self.recoEffXsec = []
        self.recoEffXsec_1up = []
        self.recoEffXsec_1down = []


        self.outFile=ROOT.TFile('output.root','RECREATE')
        for i in range(len(self.srList)):
            for j in range(len(self.mjList)):
                self.truthEffHist.append(ROOT.TH2D('h_truthEff_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency',24,725,1925,37,25,1875))
                self.truthEffXsec.append(ROOT.TH2D('h_truthEff_xsec_nom_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.truthEffXsec_1up.append(ROOT.TH2D('h_truthEff_xsec_1up_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.truthEffXsec_1down.append(ROOT.TH2D('h_truthEff_xsec_1down_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))

                self.recoYieldHist.append(ROOT.TH2D('h_recoYield_nom_'+self.srList[i]+'_'+self.mjList[j],'nominal reco yield',24,725,1925,37,25,1875))
                self.recoYieldHist_1up.append(ROOT.TH2D('h_recoYield_1up_'+self.srList[i]+'_'+self.mjList[j],'+1 #sigma reco yield',24,725,1925,37,25,1875))
                self.recoYieldHist_1down.append(ROOT.TH2D('h_recoYield_1down_'+self.srList[i]+'_'+self.mjList[j],'-1 #sigma reco yield',24,725,1925,37,25,1875))

                self.recoEffHist.append(ROOT.TH2D('h_recoEff_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency',24,725,1925,37,25,1875))
                self.recoEffXsec.append(ROOT.TH2D('h_recoEff_xsec_nom_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.recoEffXsec_1up.append(ROOT.TH2D('h_recoEff_xsec_1up_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                self.recoEffXsec_1down.append(ROOT.TH2D('h_recoEff_xsec_1down_'+self.srList[i]+'_'+self.mjList[j],'selection efficiency * xsec',24,725,1925,37,25,1875))
                
    def makeTruthHists(self):
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
    def makeRecoEffHists(self):
        for key in self.recoFile.GetListOfKeys():
            if 'h_SRyield_4' in key.GetName():
                h = self.recoFile.Get(key.GetName())
                dsid = key.GetName().split('_')[2]
                mG = pointDict[int(dsid)][0]
                mX = pointDict[int(dsid)][1]
                xsec = pointDict[int(dsid)][2]
                xsec_uncert = pointDict[int(dsid)][3]/100.
                xsec_1up = xsec*(1+xsec_uncert)
                xsec_1down = xsec*(1-xsec_uncert)
                lumi = 5.8E6
                for i in range(h.GetNbinsX()):
                    self.recoEffHist[i].Fill(mG,mX,h.GetBinContent(i+1)/(xsec*lumi))
                    self.recoEffXsec[i].Fill(mG,mX,h.GetBinContent(i+1)/(lumi))
                    self.recoEffXsec_1up[i].Fill(mG,mX,h.GetBinContent(i+1)*xsec_1up/(xsec*lumi))
                    self.recoEffXsec_1down[i].Fill(mG,mX,h.GetBinContent(i+1)*xsec_1down/(xsec*lumi))
                    self.recoYieldHist[i].Fill(mG,mX,h.GetBincontent(i=1))
                    self.recoYieldHist_1up[i].Fill(mG,mX,h.GetBincontent(i=1)*xsec_1up/xsec)
                    self.recoYieldHist_1down[i].Fill(mG,mX,h.GetBincontent(i=1)*xsec_1down/xsec)
    def writeFile(self):
        self.outFile.Write()
p = TruthInterpolator()
p.makeTruthHists()
p.makeRecoHists()
p.writeFile()
