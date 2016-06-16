#!/usr/bin/env python
import ROOT,sys,math
from pprint import pprint
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
fullSimFile = ROOT.TFile.Open(sys.argv[1])
fastSimFile = ROOT.TFile.Open(sys.argv[2])
d = sys.argv[3]
histNames = ['h_m_response','h_m_responsePt','h_m_responseEta']
xLabels = ['m_{truth} [GeV]','truth p_{T} [GeV]','truth #eta']

c = [ ROOT.TCanvas('c'+str(i),'c'+str(i),800,800) for i in range(len(histNames))]
pad1 = []
pad2 = []
axis=[]
leg = ROOT.TLegend(0.65,0.6,0.85,0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)

fullSimHists=[]
fastSimHists=[]
fullSimProfs=[]
fastSimProfs=[]
ratioHists = []
ratioProfs = []
for i in range(len(histNames)):
    fullSimHists.append(fullSimFile.Get(histNames[i]))
    fastSimHists.append(fastSimFile.Get(histNames[i]))
    fullSimProfs.append(fullSimHists[i].ProfileX(histNames[i]+'_fullPfx',1,-1,'S'))
    fastSimProfs.append(fastSimHists[i].ProfileX(histNames[i]+'_fastPfx',1,-1,'S'))
    if i == 0:
        leg.AddEntry(fullSimProfs[i],'full sim','pl')
        leg.AddEntry(fastSimProfs[i],'fast sim','pl')
    c[i].cd()
    pad1.append(ROOT.TPad('pad1_'+str(i),'pad1_'+str(i),0,0.2,1,1.0))
    pad1[i].Draw()
    pad1[i].cd()
    fullSimProfs[i].SetLineColor(ROOT.kRed)
    fullSimProfs[i].SetMarkerColor(ROOT.kRed)
    fullSimProfs[i].SetMarkerStyle(20)
    fastSimProfs[i].GetXaxis().SetTitle(xLabels[i])
    fullSimProfs[i].GetYaxis().SetTitle('m_{reco}/m_{truth}')
    fullSimProfs[i].GetYaxis().SetTitleOffset(1.4)
    fastSimProfs[i].SetLineColor(ROOT.kBlue)
    fastSimProfs[i].SetMarkerColor(ROOT.kBlue)
    fastSimProfs[i].SetMarkerStyle(20)
    fullSimProfs[i].GetXaxis().SetLabelSize(0)
    fullSimProfs[i].Draw()
    fastSimProfs[i].Draw('same')
    leg.Draw()
    c[i].cd()
    pad2.append(ROOT.TPad('pad2_'+str(i),'pad2_'+str(i),0,0.05,1,0.3))
    pad2[i].SetTopMargin(0)
    pad2[i].SetBottomMargin(0.2)
    pad2[i].SetGridy()
    pad2[i].Draw()
    pad2[i].cd() 
    ratioHists.append(fastSimProfs[i].ProjectionX().Clone('ratio_'+str(i)))
    ratioHists[i].Divide(fullSimProfs[i].ProjectionX())
    ratioHists[i].SetLineColor(ROOT.kBlack)
    ratioHists[i].SetMarkerColor(ROOT.kBlack)
    if i == 2:
        ratioHists[i].SetMinimum(0.8)
        ratioHists[i].SetMaximum(1.22)
    else:
        ratioHists[i].SetMinimum(0.93)
        ratioHists[i].SetMaximum(1.025)
    ratioHists[i].GetXaxis().SetTitle(xLabels[i])
    ratioHists[i].SetMarkerStyle(21)
    ratioHists[i].Draw("ep")
    ratioHists[i].GetYaxis().SetTitle('AFII/FullSim')
    ratioHists[i].GetYaxis().SetNdivisions(505)
    ratioHists[i].GetYaxis().SetTitleSize(20)
    ratioHists[i].GetYaxis().SetTitleFont(43)
    ratioHists[i].GetYaxis().SetTitleOffset(1.55)
    ratioHists[i].GetYaxis().SetLabelFont(43)
    ratioHists[i].GetYaxis().SetLabelSize(15)
    ratioHists[i].GetXaxis().SetTitleSize(20)
    ratioHists[i].GetXaxis().SetTitleFont(43)
    ratioHists[i].GetXaxis().SetTitleOffset(3.5)
    ratioHists[i].GetXaxis().SetLabelFont(43)
    ratioHists[i].GetXaxis().SetLabelSize(15)
    c[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/'+str(13+i)+'_'+histNames[i]+'.pdf')
