#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src ; eval `scram runtime -sh`>/dev/null
export X509_USER_PROXY=/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/userproxy
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/runDIGIRECOSKIM_Sexaq_withCuts/crab/
cmsRun BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py inputFiles=file:test7.root outputFile=file:output7.root > outputTest5.txt 2>&1
#DEBUG
#python -i runDIGIRECOSKIM_Sexaq_withCuts/BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py inputFiles=file:GenSimTest3.root outputFile=file:FullSkimTest3.root > SkimTest3Out.txt 2>&1
