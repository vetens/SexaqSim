from WMCore.Configuration import Configuration

day = "21112022"
version = "v4"
#main Multi-Sbar sample
#trial = "5_MultiSQEV"
#For comparison to older version of the analysis
#trial = "4_MultiSQEV_NoEtaCut"
#Single Sbar for reweighting
trial = "4"
mass = "1p8GeV"


config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'Step1_Step2_Skimming_FlatTree_trial'+trial+'_'+mass+'_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py' 
config.JobType.maxMemoryMB = 5000

config.section_('Data') 
config.Data.unitsPerJob = 1 
config.Data.totalUnits = 10000
config.Data.publication = True 
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/Skimmed' 
#config.Data.userInputFiles = open('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/runDIGIRECOSKIM_Sexaq_withCuts/crab/inputFiles_trial'+trial+'_'+mass+'_GENSIM.txt').readlines()
#main Multi-Sbar sample
#config.Data.inputDataset = '/CRAB_SimSexaq_trial5_MultiSQEV/wvetens-crab_SIMSexaq_trial5_MultiSQEV_1p8GeV_07102022_v3-e0f2328d9e3cb9f82d34f8d7ff9293dd/USER'
#For comparison to older version of the analysis
#config.Data.inputDataset = '/CRAB_SimSexaq_trial4_MultiSQEV_NoEtaCut/wvetens-crab_SIMSexaq_trial4_MultiSQEV_NoEtaCut_1p8GeV_07102022_v3-e0f2328d9e3cb9f82d34f8d7ff9293dd/USER'
#Single Sbar for reweighting
config.Data.inputDataset = '/CRAB_SimSexaq_trial4/wvetens-crab_SIMSexaq_trial4_1p8GeV_07102022_v3-e0f2328d9e3cb9f82d34f8d7ff9293dd/USER'
config.Data.inputDBS = 'phys03'
#config.Data.outputPrimaryDataset = "crab_Step2SexaqWithPU2018BParking_trial"+trial
config.Data.ignoreLocality = True


config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =['T2_*'] 
config.Site.storageSite = 'T2_US_Wisconsin'
