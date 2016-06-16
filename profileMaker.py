#!/usr/bin/env python
import ROOT
from array import array
class profileMaker:
    def __init__(self,hist2d,name,mStart=1.0,sigStart=0.2,mult=1.5):
        self.hist2d=hist2d
        self.name = name
        self.projHists = [hist2d.ProjectionY('p_'+str(i),i,i) for i in range(1,hist2d.GetNbinsX()+1)]
        self.profile_width = hist2d.ProjectionX(name+'_width')
        self.profile_err = hist2d.ProjectionX(name+'_err')
        self.xMinStart = mStart-mult*sigStart
        self.xMaxStart = mStart+mult*sigStart
        self.mult = mult
    def getResponseFits(self):
        self.canvas = ROOT.TCanvas('c_'+self.name,'c_'+self.name,1000,1000)
        self.results0 = []
        self.results = []
        nPlots = self.hist2d.GetNbinsX()
        if nPlots < 10:
            self.canvas.Divide(3,3)
        elif nPlots < 17:
            self.canvas.Divide(4,4)
        elif nPlots < 26:
            self.canvas.Divide(5,5)
        elif nPlots < 37:
            self.canvas.Divide(6,6)

        for i in range(0,self.hist2d.GetNbinsX()):
            self.xMin = self.xMinStart
            self.xMax = self.xMaxStart
            self.canvas.cd(i+1)
            finalFit = False
            if self.projHists[i].Integral() < 100:
                print 'Not enough statistics. Merging histograms after bin',i
                finalFit = True
                for j in range(i+1,self.hist2d.GetNbinsX()):
                    self.projHists[i].Add(self.projHists[j])
            self.projHists[i].Rebin(10)
            self.results0.append(self.projHists[i].Fit('gaus','QSN','',self.xMin,self.xMax))
            self.xMin = self.results0[i].Parameters().at(1)-self.mult*self.results0[i].Parameters().at(2)
            self.xMax = self.results0[i].Parameters().at(1)+self.mult*self.results0[i].Parameters().at(2)
            self.results.append(self.projHists[i].Fit('gaus','QS','',self.xMin,self.xMax))
            self.profile_err.SetBinContent(i+1,self.results[i].Parameters().at(1))
            self.profile_err.SetBinError(i+1,self.results[i].Errors().at(1))
            self.profile_width.SetBinContent(i+1,self.results[i].Parameters().at(1))
            self.profile_width.SetBinError(i+1,self.results[i].Parameters().at(2))
            if finalFit:
                self.profile_err = self.dropBins(self.profile_err,i)
                self.profile_width = self.dropBins(self.profile_width,i)
                break
        return(self.profile_err,self.profile_width,self.canvas)
    def dropBins(self,hist,bin):
        xBins = []
        for i in range(0,hist.GetNbinsX()):
            if i <= bin:
                xBins.append(hist.GetBinLowEdge(i+1))
        xBins.append(hist.GetBinLowEdge(hist.GetNbinsX()))
        tmp = hist.GetName()
        hist.SetName('tmp')
        newHist = ROOT.TH1F(tmp,hist.GetTitle(),len(xBins)-1,array('d',xBins))
        for i in range(0,hist.GetNbinsX()):
            if i <= bin:
                newHist.SetBinContent(i+1,hist.GetBinContent(i+1))
                newHist.SetBinError(i+1,hist.GetBinError(i+1))
        return newHist
