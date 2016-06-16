#!/usr/bin/env python
import ROOT,sys,math
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
f = ROOT.TFile.Open(sys.argv[1])
h_pt = f.Get('h_m_responsePt')
hPt = []
func = ROOT.TF1("f1","gaus",-2,2)
c1 = ROOT.TCanvas('c1','c1',1000,1000)
c1.Divide(4,4)
resultsPt0 = []
resultsPt1 = []
resultsPt = []

h_resultsPt = ROOT.TH1F('h_resultsPt','h_resultsPt',h_pt.GetNbinsX()-1,h_pt.GetXaxis().GetBinLowEdge(2),h_pt.GetXaxis().GetBinLowEdge(h_pt.GetNbinsX()+1))
for bin in range(1,h_pt.GetNbinsX()+1):
    hPt.append(h_pt.ProjectionY('p'+str(bin),bin,bin))
    hPt[bin-1].Rebin(10)
    xmin =[]
    xmax =[]
    xmin.append(0.5)
    xmax.append(1.5)
    c1.cd(bin)
    multLow = 2.0
    multUp = 2.0
    if bin == 1:
        multLow = 1.2
        multUp = 0.7
    resultsPt0.append(hPt[bin-1].Fit("gaus","QSN+","",xmin[0],xmax[0]))
    xmin.append(resultsPt0[bin-1].Parameters().at(1)-multLow*resultsPt0[bin-1].Parameters().at(2))
    xmax.append(resultsPt0[bin-1].Parameters().at(1)+multUp*resultsPt0[bin-1].Parameters().at(2))
    resultsPt1.append(hPt[bin-1].Fit("gaus","QSN+","",xmin[1],xmax[1]))
    xmin.append(resultsPt1[bin-1].Parameters().at(1)-multLow*resultsPt0[bin-1].Parameters().at(2))
    xmax.append(resultsPt1[bin-1].Parameters().at(1)+multUp*resultsPt0[bin-1].Parameters().at(2))
    resultsPt.append(hPt[bin-1].Fit("gaus","QS+","",xmin[2],xmax[2]))
    h_resultsPt.SetBinContent(bin,resultsPt[bin-1].Parameters().at(1))
    h_resultsPt.SetBinError(bin,resultsPt[bin-1].Parameters().at(2))
    print xmin,xmax
                            
for result in resultsPt:
    print result.Parameters().at(0),result.Parameters().at(1),result.Parameters().at(2)

c4 = ROOT.TCanvas('c4','c4',800,600)
c4.cd()
h_resultsPt.Draw()

