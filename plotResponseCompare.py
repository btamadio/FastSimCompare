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

c = [ ROOT.TCanvas('c'+str(i),'c'+str(i),800,600) for i in range(len(histNames))]
xis=[]
leg = ROOT.TLegend(0.65,0.8,0.85,0.9)
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
    fullSimProfs[i].SetLineColor(ROOT.kRed)
    fullSimProfs[i].SetMarkerColor(ROOT.kRed)
    fullSimProfs[i].SetMarkerStyle(20)
    fullSimProfs[i].GetXaxis().SetTitle(xLabels[i])
    fullSimProfs[i].GetYaxis().SetTitle('m_{reco}/m_{truth}')
    fullSimProfs[i].GetYaxis().SetTitleOffset(1.4)
    fastSimProfs[i].SetLineColor(ROOT.kBlue)
    fastSimProfs[i].SetMarkerColor(ROOT.kBlue)
    fastSimProfs[i].SetMarkerStyle(20)
    fastSimProfs[i].SetLineStyle(2)
    fullSimProfs[i].Draw()
    fastSimProfs[i].Draw('same')
    leg.Draw()
    c[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/'+str(13+i)+'_'+histNames[i]+'.pdf')
