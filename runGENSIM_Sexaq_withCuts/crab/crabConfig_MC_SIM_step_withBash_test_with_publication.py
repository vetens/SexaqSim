from WMCore.Configuration import Configuration

#DDMMYYYY format
day = "07102022"
version = "v3"
#trial = "4_MultiSQEV_NoEtaCut"
#trial = "4"
trial = "5_MultiSQEV"
mass = "1p8GeV"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'SIMSexaq_trial'+trial+'_'+mass+'_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'BPH-RunIIFall18GenSim-00369_Sexaq_cfg.py' 
config.JobType.priority = 120
#config.JobType.maxMemoryMB = 3000

config.section_('Data') 
config.Data.unitsPerJob = 1 
config.Data.totalUnits = 10000
config.Data.publication = True 
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/GENSIM' 
config.Data.userInputFiles = open('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/runGENSIM_Sexaq_withCuts/crab/inputFiles_trial'+trial+'_'+mass+'.txt').readlines() 
config.Data.outputPrimaryDataset = "CRAB_SimSexaq_trial"+trial
config.Data.ignoreLocality = True


config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =["T2_US_*"] 
config.Site.storageSite = 'T2_US_Wisconsin'
