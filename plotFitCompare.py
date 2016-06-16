#!/usr/bin/env python
import ROOT,sys,math
from pprint import pprint
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
fullSimFile = ROOT.TFile.Open(sys.argv[1])
fastSimFile = ROOT.TFile.Open(sys.argv[2])
d = sys.argv[3]
histNames = ['h_m_responseM_fit','h_m_responsePt_fit']
xLabels = ['m_{truth} [GeV]','truth p_{T} [GeV]']

c = [ ROOT.TCanvas('c'+str(i),'c'+str(i),800,600) for i in range(len(histNames))]

leg = ROOT.TLegend(0.65,0.8,0.85,0.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)

fullSimHists=[]
fastSimHists=[]

for i in range(len(histNames)):
    fullSimHists.append(fullSimFile.Get(histNames[i]))
    fastSimHists.append(fastSimFile.Get(histNames[i]))
    if i == 0:
        leg.AddEntry(fullSimHists[i],'full sim','pl')
        leg.AddEntry(fastSimHists[i],'fast sim','pl')
    c[i].cd()
    fullSimHists[i].SetLineColor(ROOT.kRed)
    fullSimHists[i].SetMarkerColor(ROOT.kRed)
    fullSimHists[i].SetMarkerStyle(20)
    fullSimHists[i].GetXaxis().SetTitle(xLabels[i])
    fullSimHists[i].GetYaxis().SetTitle('m_{reco}/m_{truth}')
    fullSimHists[i].GetYaxis().SetTitleOffset(1.4)
    fastSimHists[i].SetLineColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerStyle(20)
    fastSimHists[i].SetLineStyle(2)
    fullSimHists[i].Draw()
    fastSimHists[i].Draw('same')
    leg.Draw()
    c[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/'+str(16+i)+'_'+histNames[i]+'.pdf')
