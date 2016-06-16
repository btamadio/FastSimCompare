#!/usr/bin/env python
import ROOT,sys
from pprint import pprint
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
fullSimFile = ROOT.TFile.Open(sys.argv[1])
fastSimFile = ROOT.TFile.Open(sys.argv[2])
d = sys.argv[3]
histNames = ['h_fatjet_pt',
             'h_fatjet_eta',
             'h_fatjet_phi',
             'h_fatjet_m_0',
             'h_fatjet_m_1',
             'h_fatjet_split12',
             'h_fatjet_tau32',
             'h_fatjet_tau21',
             'h_fatjet_C2',
             'h_fatjet_D2',
             'h_fatjet_NTrimSubjets',
             'h_fatjet_m_nsub1',
             'h_fatjet_m_nsub2',
             'h_fatjet_m_nsub3',
             'h_fatjet_m1_nsub1',
             'h_fatjet_m1_nsub2',
             'h_fatjet_m1_nsub3',
             'h_fatjet_pt_nsub1',
             'h_fatjet_pt_nsub2',
             'h_fatjet_pt_nsub3',
             'h_fatjet_split12_nsub1',
             'h_fatjet_split12_nsub2',
             'h_fatjet_split12_nsub3',
             'h_fatjet_tau32_nsub1',
             'h_fatjet_tau32_nsub2',
             'h_fatjet_tau32_nsub3',
             'h_fatjet_tau21_nsub1',
             'h_fatjet_tau21_nsub2',
             'h_fatjet_tau21_nsub3',
             'h_fatjet_C2_nsub1',
             'h_fatjet_C2_nsub2',
             'h_fatjet_C2_nsub3',
             'h_fatjet_D2_nsub1',
             'h_fatjet_D2_nsub2',
             'h_fatjet_D2_nsub3']


             
c = [ ROOT.TCanvas('c'+str(i),'c'+str(i),800,800) for i in range(len(histNames))]
pad1 = []
pad2 = []
axis=[]
leg = ROOT.TLegend(0.7,0.8,0.85,0.9)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)

fullSimHists=[]
fastSimHists=[]
ratioHists = []
for i in range(len(histNames)):
    fullSimHists.append(fullSimFile.Get(histNames[i]))
    fastSimHists.append(fastSimFile.Get(histNames[i]))
    if i == 0:
        leg.AddEntry(fullSimHists[i],'FullSim','pl')
        leg.AddEntry(fastSimHists[i],'AFII','pl')
    c[i].cd()
    pad1.append(ROOT.TPad('pad1_'+str(i),'pad1_'+str(i),0,0.2,1,1.0))
    pad1[i].Draw()
    pad1[i].cd()
    fullSimHists[i].SetLineColor(ROOT.kRed)
    fullSimHists[i].SetMarkerColor(ROOT.kRed)
    fullSimHists[i].SetMarkerStyle(20)
    fullSimHists[i].GetYaxis().SetTitle('fraction of jets')
    maxMult=1.2
    if i == 0:
        pad1[i].SetLogy()
        maxMult=10
    fullSimHists[i].GetYaxis().SetTitleOffset(1.4)
    fastSimHists[i].SetLineColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerStyle(20)
    fullSimHists[i].Sumw2()
    fastSimHists[i].Sumw2()
    if fullSimHists[i].Integral() != 0:
        fullSimHists[i].Scale(1./fullSimHists[i].Integral())
    if fastSimHists[i].Integral() != 0:
        fastSimHists[i].Scale(1./fastSimHists[i].Integral())
    fullSimHists[i].GetXaxis().SetLabelSize(0)
    fullSimHists[i].Draw('ehist')
    fastSimHists[i].Draw('ehist same')
    if fastSimHists[i].GetMaximum() > fullSimHists[i].GetMaximum():
        fullSimHists[i].SetMaximum(fastSimHists[i].GetMaximum()*maxMult)
    else:
        fullSimHists[i].SetMaximum(fullSimHists[i].GetMaximum()*maxMult)
    leg.Draw()
    label = ROOT.ATLASLabel(0.2,0.85,'Internal')
    c[i].cd()
    pad2.append(ROOT.TPad('pad2_'+str(i),'pad2_'+str(i),0,0.05,1,0.3))
    pad2[i].SetTopMargin(0)
    pad2[i].SetBottomMargin(0.2)
    pad2[i].SetGridy()
    pad2[i].Draw()
    pad2[i].cd() 
    ratioHists.append(fastSimHists[i].Clone('ratio_'+str(i)))
    ratioHists[i].SetLineColor(ROOT.kBlack)
    ratioHists[i].SetMarkerColor(ROOT.kBlack)
    ratioHists[i].Divide(fullSimHists[i])
    ratioHists[i].SetMarkerStyle(21)
    ratioHists[i].SetMaximum(2)
    ratioHists[i].SetMinimum(0)
    ratioHists[i].Draw()
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
    ratioHists[i].GetXaxis().SetTitle(ratioHists[i].GetTitle())
    if i < 10:
        c[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/0'+str(i)+'_'+histNames[i]+'.pdf')
    else:
        c[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/'+str(i)+'_'+histNames[i]+'.pdf')

responseNames = ['h_m_responsePt_fit0','h_m_responsePt_fit1','h_m_responsePt_fit2','h_m_responsePt_fit3']
xLabel = 'truth p_{T} [GeV]'
cres = [ ROOT.TCanvas('cres_'+str(i),'cres_'+str(i),800,600) for i in range(len(responseNames))]
fullSimErr = []
fullSimWidth = []
fastSimErr = []
fastSimWidth = []
leg2 = ROOT.TLegend(0.25,0.8,0.4,0.9)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
leg2.SetTextSize(0.04)

for i in range(len(responseNames)):
    fullSimErr.append(fullSimFile.Get(responseNames[i]+'_err'))
    fastSimErr.append(fastSimFile.Get(responseNames[i]+'_err'))
    fullSimWidth.append(fullSimFile.Get(responseNames[i]+'_width'))    
    fastSimWidth.append(fastSimFile.Get(responseNames[i]+'_width'))
    if i == 0:
        leg2.AddEntry(fullSimWidth[i],'FullSim','pl')
        leg2.AddEntry(fastSimWidth[i],'AFII','pl')
    cres[i].cd()
    fullSimErr[i].SetLineColor(ROOT.kRed)
    fullSimErr[i].SetFillColor(ROOT.kRed)
    fullSimErr[i].SetFillStyle(3001)
    fullSimWidth[i].SetLineColor(ROOT.kRed)
    fullSimWidth[i].SetMarkerColor(ROOT.kRed)
    fullSimWidth[i].SetMarkerStyle(20)
    fullSimWidth[i].GetXaxis().SetTitle(xLabel)
    fullSimWidth[i].GetYaxis().SetTitle('m_{reco}/m_{truth}')
    fullSimWidth[i].GetYaxis().SetTitleOffset(1.4)

    fastSimErr[i].SetLineColor(ROOT.kBlue)
    fastSimErr[i].SetFillColor(ROOT.kBlue)
    fastSimErr[i].SetFillStyle(3001)
    fastSimWidth[i].SetLineColor(ROOT.kBlue)
    fastSimWidth[i].SetLineStyle(2)
    fastSimWidth[i].SetMarkerColor(ROOT.kBlue)
    fastSimWidth[i].SetMarkerStyle(20)

    fullSimWidth[i].Draw()
    fullSimErr[i].Draw('E2 same')
    fastSimErr[i].Draw('E2 same')
    fullSimWidth[i].Draw('same')
    fastSimWidth[i].Draw('same')
    
    leg2.Draw()
    label = ROOT.ATLASLabel(0.6,0.85,'Internal')
    cres[i].Print('/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/'+d+'/'+str(90+i)+'_'+responseNames[i]+'.pdf')
