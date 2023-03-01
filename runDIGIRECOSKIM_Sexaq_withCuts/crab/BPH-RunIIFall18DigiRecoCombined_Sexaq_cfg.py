import sys
import FWCore.ParameterSet.Config as cms
from RecoVertex.V0Producer.generalV0Candidates_cff import *
from SexaQAnalysis.Skimming.MassFilter_cfi import massFilter

from Configuration.StandardSequences.Eras import eras
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process('HLT',eras.Run2_2018,eras.bParking)
options = VarParsing ('analysis')
options.parseArguments()

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

####################################
# import of standard configurations#
####################################

#### FIRST STEP: DIGI
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_Flat_0_50_25ns_cfi')
#process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_2018v32_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.RecoSim_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#Debug: uncomment the following command and run this file with ``python -i``
#print process.dumpPython()

runningOnData = False

process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(1000)
    input = cms.untracked.int32(-1)
)

input_collections = cms.untracked.vstring(
        'keep *', 
        'drop *_genParticles_*_*', 
        'keep *_genParticles_*_HLT', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'
 )
collections_to_keep = cms.untracked.vstring(
        'drop *',
        'keep *_InitialProducer_*_*',
        'keep recoVertexs_offlinePrimaryVertices_*_*',
        'keep recoBeamSpot_offlineBeamSpot_*_*',
        'keep *_genParticles_*_HLT',
        'keep *_genParticlesPlusGEANT_*_*',
        'keep recoVertexCompositeCandidates_generalV0Candidates_*_*',
        'keep recoTracks_lambdaKshortVertexFilter_sParticlesTracks_*',
        'keep recoVertexCompositePtrCandidates_rMassFilter_sVertexCompositePtrCandidate_*',
        'keep recoVertexCompositePtrCandidates_sMassFilter_sVertexCompositePtrCandidate_*',
        'keep *_*_*_SEXAQ',
        'keep *_lambdaKshortVertexFilter_sParticles_*',
        'keep *_offlinePrimaryVertices_*_*',
        "keep *_genParticlesPlusGEANT_*_*",
#        "keep *_g4SimHits_*_*",
        "keep *_simSiPixelDigis_*_*",
#        "keep *_simMuonRPCDigis_*_*",
        "keep *_simSiStripDigis_*_*",
        "keep *_mix_MergedTrackTruth_*",
#        "keep *_siPixelDigis_*_*",
#        "keep *_siStripDigis_*_*",
#        "keep *_siStripDigis_*_*",
        "keep *_siPixelClusters_*_*",
        "keep *_siStripClusters_*_*",
        "keep *_generalTracks_*_*"
 )
# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    duplicateCheckMode = cms.untracked.string ("noDuplicateCheck"),
    #fileNames = cms.untracked.vstring('file:BPH-RunIIFall18GS-00369.root'),
    fileNames = cms.untracked.vstring(options.inputFiles),
    inputCommands = input_collections,
    secondaryFileNames = cms.untracked.vstring()
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:1000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

### LONG LINE COMING
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')

##### SECOND STEP: RECO

process.load("RecoVertex.V0Producer.generalV0Candidates_cfi")
process.generalV0Candidates.innerHitPosCut = -1
process.generalV0Candidates.cosThetaXYCut = -1
process.generalV0Candidates.kShortMassCut = 0.03
process.generalV0Candidates.lambdaMassCut = 0.015

##### THIRD STEP: Skimming
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

#In the original config but not sure if we want it here:
#process.load('Configuration/StandardSequences/MagneticField_38T_cff')


########################
#####Scheduling#########
########################

#FIRST STEP: DIGI

process.digitisation_step = cms.Path(process.pdigi)

process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)

#SECOND STEP: RECO

process.raw2digi_step = cms.Path(process.RawToDigi)

process.L1Reco_step = cms.Path(process.L1Reco)

process.reconstruction_step = cms.Path(process.reconstruction)

process.recosim_step = cms.Path(process.recosim)

process.eventinterpretaion_step = cms.Path(process.EIsequence)
#process.endjob_step = cms.EndPath(process.endOfProcess)
#process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

#INTERMEDIATE FLAT TREE PRODUCERS
## Commented out to reduce computing resources used per CRAB job, to be run separately
#process.load("SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi")
#process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
#process.load("Validation.RecoTrack.cuts_cff")
#process.load("Validation.RecoTrack.MultiTrackValidator_cff")
#process.load("DQMServices.Components.EDMtoMEConverter_cff")
#process.load("Validation.Configuration.postValidation_cff")
#process.quickTrackAssociatorByHits.SimToRecoDenominator = 'reco'
#process.quickTrackAssociatorByHits.useClusterTPAssociation = True
#process.load("SimTracker.TrackerHitAssociation.tpClusterProducer_cfi")
#process.validation = cms.Sequence(
#    process.tpClusterProducer *
#    process.quickTrackAssociatorByHits
#)
#process.load("SexaQAnalysis.AnalyzerAllSteps.FlatTreeProducerTracking_cfi")
#process.FlatTreeProducerTracking.innerHitPosCut = -1
#process.FlatTreeProducerTracking.cosThetaXYCut = -1
#process.FlatTreeProducerTracking.kShortMassCut = 0.03
#process.FlatTreeProducerTracking.lambdaMassCut = 0.015
#process.ValidationAndFlatTreeProducerTrackingPath = cms.Path(process.validation * process.FlatTreeProducerTracking)


#THIRD STEP: SKIMMING
process.nEvTotal        = cms.EDProducer("EventCountProducer")
process.nEvLambdaKshort = cms.EDProducer("EventCountProducer")
process.nEvLambdaKshortVertex = cms.EDProducer("EventCountProducer")
process.nEvSMass        = cms.EDProducer("EventCountProducer")

#process.genParticlePlusGEANT = cms.EDProducer("GenPlusSimParticleProducer",
#  src           = cms.InputTag("g4SimHits"),
#  setStatus     = cms.int32(8),                # set status = 8 for GEANT GPs
#  particleTypes = cms.vstring("Xi-","Xibar+","Lambda0","Lambdabar0","K_S0","K0"),      # also picks pi- (optional)
#  filter        = cms.vstring("pt >= 0.0"),     # just for testing
#  genParticles  = cms.InputTag("genParticles") # original genParticle list
#
#)
process.generalV0Candidates.innerHitPosCut = -1
process.generalV0Candidates.cosThetaXYCut = -1
process.generalV0Candidates.kShortMassCut = 0.03
process.generalV0Candidates.lambdaMassCut = 0.015
#generalV0Candidates_step = cms.Path(process.generalV0Candidates)


process.load("SexaQAnalysis.Skimming.LambdaKshortFilter_cfi")
process.lambdaKshortFilter.genCollection = cms.InputTag("genParticlesPlusGEANT")
process.lambdaKshortFilter.isData = True
process.lambdaKshortFilter.minPtLambda = 0. 
process.lambdaKshortFilter.minPtKshort = 0. 
process.lambdaKshortFilter.checkLambdaDaughters = True
process.lambdaKshortFilter.prescaleFalse = 0

process.load("SexaQAnalysis.Skimming.LambdaKshortVertexFilter_cfi")
process.lambdaKshortVertexFilter.lambdaCollection = cms.InputTag("lambdaKshortFilter","lambda")
process.lambdaKshortVertexFilter.kshortCollection = cms.InputTag("lambdaKshortFilter","kshort")
process.lambdaKshortVertexFilter.maxchi2ndofVertexFit = 10.

massFilter.lambdakshortCollection = cms.InputTag("lambdaKshortVertexFilter","sParticles")
massFilter.minMass = -10000 # effectively no filter
massFilter.maxMass = 10000  # effectively no filter
process.rMassFilter = massFilter.clone()
process.rMassFilter.targetMass = 0
process.sMassFilter = massFilter.clone()
process.sMassFilter.targetMass = 0.939565

process.load("SexaQAnalysis.Skimming.InitialProducer_cfi")

process.load("SexaQAnalysis.TreeProducer.Treeproducer_AOD_cfi")

# FINAL STEP: Output FlatTree Production

process.load("SexaQAnalysis.AnalyzerAllSteps.FlatTreeProducerBDT_cfi")
process.FlatTreeProducerBDT.runningOnData = runningOnData
#process.flattreeproducerBDT = cms.Path(process.FlatTreeProducerBDT)

#Keep edm output file --> used in the analyzer
process.out_step = cms.OutputModule("PoolOutputModule",
  compressionAlgorithm = cms.untracked.string('LZMA'),
  compressionLevel = cms.untracked.int32(4),
  dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('AODSIM-SKIM'),
    filterName = cms.untracked.string('')
  ),
  eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
  outputCommands = collections_to_keep,
  fileName = cms.untracked.string("EDM_"+options.outputFile[:-5]+"_events_skimmed.root"),
  SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('*')
  ),
)

# Autogenerated output - ignoring for now
#process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
#    compressionAlgorithm = cms.untracked.string('LZMA'),
#    compressionLevel = cms.untracked.int32(4),
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string('AODSIM'),
#        filterName = cms.untracked.string('')
#    ),
#    eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
#    #fileName = cms.untracked.string('file:BPH-RunIIAutumn18DR-00142.root'),
#    fileName = cms.untracked.string(options.outputFile),
#    outputCommands = process.AODSIMEventContent.outputCommands
#)

########################
#FINAL SCHEDULE#########
########################

process.skimming_and_BDTflattreeproducer_step = cms.Path(
    process.generalV0Candidates*
    process.tree*
    process.nEvTotal *
    process.InitialProducer *
    process.lambdaKshortFilter *
    process.nEvLambdaKshort *
    process.lambdaKshortVertexFilter *
    process.nEvLambdaKshortVertex *
    process.rMassFilter *
    process.sMassFilter *
    process.nEvSMass *
    process.FlatTreeProducerBDT
)

# Schedule definition
process.schedule = cms.Schedule(
    process.digitisation_step,
    process.L1simulation_step,
    process.digi2raw_step
)

process.schedule.extend(process.HLTSchedule)

process.output_step_EndPath = cms.EndPath(process.out_step)
#Step2_Skimming_FlatTreeProducer_Schedule = cms.Schedule(process.raw2digi_step, process.reconstruction_step, process.recosim_step, process.eventinterpretaion_step, process.skimming_and_flattreeproducer_step,process.V0FlatTree, process.output_step_EndPath)
#Step2_Skimming_FlatTreeProducer_Schedule = cms.Schedule(process.raw2digi_step, process.reconstruction_step, process.recosim_step, process.eventinterpretaion_step, process.ValidationAndFlatTreeProducerTrackingPath, process.skimming_and_BDTflattreeproducer_step, process.output_step_EndPath)
Step2_Skimming_FlatTreeProducer_Schedule = cms.Schedule(process.raw2digi_step, process.reconstruction_step, process.recosim_step, process.eventinterpretaion_step, process.skimming_and_BDTflattreeproducer_step, process.output_step_EndPath)

process.schedule.extend(Step2_Skimming_FlatTreeProducer_Schedule)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(options.outputFile)
)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99) 
process.mix.input.nbPileupEvents.probValue = cms.vdouble(1.286e-05,4.360e-05,1.258e-04,2.721e-04,4.548e-04,7.077e-04,1.074e-03,1.582e-03,2.286e-03,3.264e-03,4.607e-03,6.389e-03,8.650e-03,1.139e-02,1.456e-02,1.809e-02,2.190e-02,2.589e-02,2.987e-02,3.362e-02,3.686e-02,3.938e-02,4.100e-02,4.173e-02,4.178e-02,4.183e-02,4.189e-02,4.194e-02,4.199e-02,4.205e-02,4.210e-02,4.178e-02,4.098e-02,3.960e-02,3.761e-02,3.504e-02,3.193e-02,2.840e-02,2.458e-02,2.066e-02,1.680e-02,1.320e-02,9.997e-03,7.299e-03,5.139e-03,3.496e-03,2.305e-03,1.479e-03,9.280e-04,5.729e-04,3.498e-04,2.120e-04,1.280e-04,7.702e-05,4.618e-05,2.758e-05,1.641e-05,9.741e-06,5.783e-06,3.446e-06,2.066e-06,1.248e-06,7.594e-07,4.643e-07,2.842e-07,1.734e-07,1.051e-07,6.304e-08,3.733e-08,2.179e-08,1.251e-08,7.064e-09,3.920e-09,2.137e-09,1.144e-09,6.020e-10,3.111e-10,1.579e-10,7.880e-11,3.866e-11,1.866e-11,8.864e-12,4.148e-12,1.914e-12,8.721e-13,3.928e-13,1.753e-13,7.757e-14,3.413e-14,1.496e-14,6.545e-15,2.862e-15,1.253e-15,5.493e-16,2.412e-16,1.060e-16,4.658e-17,2.045e-17,8.949e-18,3.899e-18)

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
#Uncomment below line for troubleshooting
#print process.dumpPython()