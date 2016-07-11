#!/usr/bin/env python
import ROOT,sys,subprocess
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

fileNameList = ['../HistMaker/hists/AFII_FullSim_Study/AFII_NoCalib.root',
                '../HistMaker/hists/AFII_FullSim_Study/FullSim_NoCalib.root',
                '../HistMaker/hists/AFII_FullSim_Study/AFII_Calib.root',
                '../HistMaker/hists/AFII_FullSim_Study/FullSim_Calib.root']
colorList = [ROOT.kBlue,ROOT.kRed,ROOT.kBlue,ROOT.kRed]
legLabelList = ['AFII Pre-calibration','FullSim Pre-calibration','AFII Calibrated','FullSim Calibrated']
styleList = [2,2,1,1]
fileList = [ROOT.TFile.Open(f) for f in fileNameList]
dsidList = [403558,403560,403563,403610]

dsidLabels = ['#splitline{#splitline{RPV10}{m_{#tilde{g}}=1.2 TeV}}{m_{#tilde{#chi}_{1}^{0}}= 50 GeV}',
              '#splitline{#splitline{RPV10}{m_{#tilde{g}}=1.2 TeV}}{m_{#tilde{#chi}_{1}^{0}}= 450 GeV}',
              '#splitline{#splitline{RPV10}{m_{#tilde{g}}=1.2 TeV}}{m_{#tilde{#chi}_{1}^{0}}= 1050 GeV}',
              '#splitline{RPV6}{m_{#tilde{g}}=1.4 TeV}']

histList = [('h_fatjet_pt','fat jet p_{T} [GeV]','fraction of jets',1),
            ('h_MJ_4jSR','M_{J}^{#Sigma} [GeV]','fraction of events',5)]
#            ('h_fatjet_eta','fat jet #eta','fraction of jets',1)]
                # 'h_fatjet_phi',
                # 'h_fatjet_m',
                # 'h_nFatJet_presel',
                # 'h_MJ_presel',

                # 'h_MJ_5jSR',
                # 'h_fatjet_nTrimSubjets',
                # 'h_fatjet_Split12',
                # 'h_fatjet_Split23',
                # 'h_fatjet_Split34',
                # 'h_fatjet_tau32_wta',
                # 'h_fatjet_tau21_wta',
                # 'h_fatjet_tauD2_wta',
                # 'h_fatjet_tauC2_wta',
                # 'h_fatjet_m_nTrim_1',
                # 'h_fatjet_Split12_nTrim_1',
                # 'h_fatjet_Split23_nTrim_1',
                # 'h_fatjet_Split34_nTrim_1',
                # 'h_fatjet_tau32_wta_nTrim_1',
                # 'h_fatjet_tau21_wta_nTrim_1',
                # 'h_fatjet_tauD2_nTrim_1',
                # 'h_fatjet_tauC2_nTrim_1',
                # 'h_fatjet_m_nTrim_2',
                # 'h_fatjet_Split12_nTrim_2',
                # 'h_fatjet_Split23_nTrim_2',
                # 'h_fatjet_Split34_nTrim_2',
                # 'h_fatjet_tau32_wta_nTrim_2',
                # 'h_fatjet_tau21_wta_nTrim_2',
                # 'h_fatjet_tauD2_nTrim_2',
                # 'h_fatjet_tauC2_nTrim_2',
                # 'h_fatjet_m_nTrim_3',
                # 'h_fatjet_Split12_nTrim_3',
                # 'h_fatjet_Split23_nTrim_3',
                # 'h_fatjet_Split34_nTrim_3',
                # 'h_fatjet_tau32_wta_nTrim_3',
                # 'h_fatjet_tau21_wta_nTrim_3',
                # 'h_fatjet_tauD2_nTrim_3',
                # 'h_fatjet_tauC2_nTrim_3']

can = []
leg = []
pad1 = []
pad2 = []
ratioCalib = []
ratioNoCalib = []
for i in range(len(dsidList)):
    for j in range(len(histList)):
        can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,800))
        can[-1].cd()
        pad1.append(ROOT.TPad('pad1_'+str(len(pad1)),'pad1_'+str(len(pad1)),0,0.2,1,1.0))
        pad1[-1].Draw()
        pad1[-1].cd()
        leg.append(ROOT.TLegend(0.65,0.6,0.85,0.775))
        leg[-1].SetBorderSize(0)
        leg[-1].SetFillStyle(0)
        leg[-1].SetTextSize(0.025)
        hName = histList[j][0]+'_'+str(dsidList[i])
        h=[f.Get(hName) for f in fileList]
        for k in range(len(h)):
            if not h[k]:
                print 'Histogram %s not found in file %s.' % (hName,h[k])
                sys.exit(1)
            if h[k].Integral() > 0:
                h[k].Scale(1.0/h[k].Integral())
            h[k].Rebin(histList[j][3])
            h[k].SetLineColor(colorList[k])
            h[k].SetLineStyle(styleList[k])
            h[k].SetLineWidth(2)
            h[k].GetXaxis().SetLabelOffset(999)
            h[k].GetYaxis().SetTitle(histList[j][2])
            h[k].GetYaxis().SetTitleOffset(1.5)
            leg[-1].AddEntry(h[k],legLabelList[k])
            if k == 0:
                h[k].Draw()
                h[k].SetMaximum(1.5*h[k].GetMaximum())
            else:
                h[k].Draw('same')

        ROOT.ATLASLabel(0.45,0.875,'Simulation Internal')
        lat = ROOT.TLatex()
        lat.DrawLatexNDC(0.7,0.8,'#sqrt{s} = 13 TeV')
        if dsidList[i]==403610:
            lat.DrawLatexNDC(0.2,0.85,dsidLabels[i])
        else:
            lat.DrawLatexNDC(0.2,0.8,dsidLabels[i])            
        leg[-1].Draw()


        can[-1].cd()
        pad2.append(ROOT.TPad('pad2_'+str(len(pad2)),'pad2_'+str(len(pad2)),0,0.05,1,0.3))
        pad2[-1].SetTopMargin(0)
        pad2[-1].SetBottomMargin(0.2)
        pad2[-1].SetGridy()
        pad2[-1].Draw()
        pad2[-1].cd() 

        nBins = h[0].GetNbinsX()
        binLow = h[0].GetBinLowEdge(1)
        binUp = h[0].GetBinLowEdge(nBins+1)
        ratioNoCalib.append(ROOT.TH1F('ratioNoCalib_'+str(len(ratioNoCalib)),'ratio no calibration',nBins,binLow,binUp))
        ratioCalib.append(ROOT.TH1F('ratioCalib_'+str(len(ratioCalib)),'ratio calibration',nBins,binLow,binUp))

        endBin = ratioNoCalib[-1].GetNbinsX()+1
        for bin in range(1,endBin):
            if 'jSR' in histList[j][0]:
                integrals=[hist.Integral(bin,endBin) for hist in h]
                if integrals[1] > 0 and integrals[3] > 0:
                    ratioNoCalib[-1].SetBinContent(bin,integrals[0]/integrals[1])
                    ratioCalib[-1].SetBinContent(bin,integrals[2]/integrals[3])
            else:
                if h[1].GetBinContent(bin) > 0 and h[3].GetBinContent(bin) > 0:
                    ratioNoCalib[-1].SetBinContent(bin,h[0].GetBinContent(bin)/h[1].GetBinContent(bin))
                    ratioCalib[-1].SetBinContent(bin,h[2].GetBinContent(bin)/h[3].GetBinContent(bin))

        ratioCalib[-1].SetLineColor(ROOT.kBlack)
        ratioCalib[-1].SetMarkerColor(ROOT.kBlack)
        ratioCalib[-1].SetMarkerStyle(21)
        ratioCalib[-1].SetMaximum(1.1)
        ratioCalib[-1].SetMinimum(0.9)
        ratioCalib[-1].Draw('hist')

        ratioNoCalib[-1].SetLineStyle(2)
        ratioNoCalib[-1].SetLineColor(ROOT.kBlack)
        ratioNoCalib[-1].Draw('hist same')
        ratioCalib[-1].GetYaxis().SetTitle('AFII/FullSim')
        ratioCalib[-1].GetYaxis().SetNdivisions(505)
        ratioCalib[-1].GetYaxis().SetTitleSize(20)
        ratioCalib[-1].GetYaxis().SetTitleFont(43)
        ratioCalib[-1].GetYaxis().SetTitleOffset(1.55)
        ratioCalib[-1].GetYaxis().SetLabelFont(43)
        ratioCalib[-1].GetYaxis().SetLabelSize(15)
        ratioCalib[-1].GetXaxis().SetTitleSize(20)
        ratioCalib[-1].GetXaxis().SetTitleFont(43)
        ratioCalib[-1].GetXaxis().SetTitleOffset(3.5)
        ratioCalib[-1].GetXaxis().SetLabelFont(43)
        ratioCalib[-1].GetXaxis().SetLabelSize(15)
        ratioCalib[-1].GetXaxis().SetTitle(histList[j][1])
        outDir = '/global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/AFII_FullSim_Study/'+str(dsidList[i])+'/'
        subprocess.call('mkdir -p '+outDir,shell=True)
        subprocess.call('chmod a+rx '+outDir,shell=True)
        outFileName = outDir+histList[j][0][2:]+'.pdf'
        can[-1].Print(outFileName)
        subprocess.call('chmod a+r '+outDir+'*',shell=True)        
