#!/bin/bash
./makeHistosFromNTUP.py ../MAF/Gtt/FullSim/data-tree/dsList.Gtt.Local.FullSim.root Gtt/FullSim.root Gtt_FullSim
./makeHistosFromNTUP.py ../MAF/Gtt/FastSim/data-tree/dsList.Gtt.Local.FastSim.root Gtt/FastSim.root Gtt_FastSim
./makeHistosFromNTUP.py ../MAF/WPrimeAFII/FullSim/data-tree/dsList.WPrime.Local.FullSim.root Wprime/FullSim.root WPrime_FullSim
./makeHistosFromNTUP.py ../MAF/WPrimeAFII/FastSim/data-tree/dsList.WPrime.Local.FastSim.root Wprime/FastSim.root WPrime_FastSim
mv responsePt_fit*_WPrime*.pdf /global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/WPrime_NoCalib/ 
mv responsePt_fit*_Gtt*.pdf /global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/Gtt_NoCalib/ 
./plotCompare.py Wprime/FullSim.root Wprime/FastSim.root WPrime_NoCalib 
./plotCompare.py Gtt/FullSim.root Gtt/FastSim.root Gtt_NoCalib
chmod 775 /global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/Gtt_NoCalib/*
chmod 775 /global/project/projectdirs/atlas/www/btamadio/RPV_SUSY/FastFullCompare/WPrime_NoCalib/*