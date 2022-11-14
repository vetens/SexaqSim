# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/BPH-RunIIFall18GS-00369-fragment.py --python_filename BPH-RunIIFall18GS-00369_1_cfg.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:BPH-RunIIFall18GS-00369.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 1000
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process('SIM',eras.Run2_2018)
options = VarParsing ('analysis')
options.outputFile = 'file:BPH-RunIIFall18GS-00369.root'
options.inputFiles = 'root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/crmc/Sexaquark_13TeV_trial_4_1p8GeV/0/crmc_Sexaq_1.root'
options.maxEvents= 4000
options.parseArguments()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
# Vtx Smearing done in hepmc 2 gen step
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
#process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoVertex.BeamSpotProducer.BeamSpot_cfi')

# Lengthy message logs - uncomment to debug
#process.MessageLogger = cms.Service("MessageLogger",
#  destinations = cms.untracked.vstring('cout'),
#  cout = cms.untracked.PSet(
#    threshold = cms.untracked.string('INFO')
#  )
#)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
    #input = cms.untracked.int32(-1)
)

# Input source

#process.source = cms.Source("EmptySource")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(0),
    duplicateCheckMode = cms.untracked.string ("noDuplicateCheck")
)


process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/BPH-RunIIFall18GS-00369-fragment.py nevts:'+str(options.maxEvents)),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.RAWSIMoutput.outputCommands += ("keep *_genParticlesPlusGEANT_*_*",)

# Other statements
process.XMLFromDBSource.label = cms.string("Extended")
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v11', '')

#process.tagfilter = cms.EDFilter("PythiaDauVFilter",
#    ChargeConjugation = cms.untracked.bool(True),
#    DaughterIDs = cms.untracked.vint32(-413, -15, 16),
#    MaxEta = cms.untracked.vdouble(9999999.0, 9999999.0, 9999999.0),
#    MinEta = cms.untracked.vdouble(-9999999.0, -9999999.0, -9999999.0),
#    MinPt = cms.untracked.vdouble(-1.0, -1, -1.0),
#    NumberDaughters = cms.untracked.int32(3),
#    ParticleID = cms.untracked.int32(511)
#)
#
#
#process.tau_mufilter = cms.EDFilter("PythiaDauVFilter",
#    ChargeConjugation = cms.untracked.bool(True),
#    DaughterIDs = cms.untracked.vint32(-16, -13, 14),
#    MaxEta = cms.untracked.vdouble(9999999.0, 1.6, 9999999.0),
#    MinEta = cms.untracked.vdouble(-9999999.0, -1.6, -9999999.0),
#    MinPt = cms.untracked.vdouble(-1.0, 6.7, -1.0),
#    MotherID = cms.untracked.int32(511),
#    NumberDaughters = cms.untracked.int32(3),
#    ParticleID = cms.untracked.int32(-15)
#)
#
#
#process.generator = cms.EDFilter("Pythia8GeneratorFilter",
#    ExternalDecays = cms.PSet(
#        EvtGen130 = cms.untracked.PSet(
#            convertPythiaCodes = cms.untracked.bool(False),
#            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
#            list_forced_decays = cms.vstring(
#                'Myanti-B0', 
#                'MyB0'
#            ),
#            operates_on_particles = cms.vint32(),
#            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
#            user_decay_embedded = cms.vstring('\nAlias      MyTau+      tau+\nAlias      MyTau-      tau-\nAlias      MyD0        D0\nAlias      Myanti-D0   anti-D0\nAlias      MyD*-       D*-\nAlias      MyD*+       D*+\nAlias      MyB0        B0\nAlias      Myanti-B0   anti-B0\nChargeConj MyTau+   MyTau-\nChargeConj MyD0   Myanti-D0\nChargeConj MyB0   Myanti-B0\nChargeConj MyD*-  MyD*+\nDecay MyTau+\n1.000      mu+  nu_mu   anti-nu_tau         TAULNUNU;\nEnddecay\nCDecay MyTau-\nDecay MyD0\n1.000       K-  pi+           PHSP;\nEnddecay\nCDecay Myanti-D0\nDecay MyD*-\n1.000       Myanti-D0 pi-     VSS;\nEnddecay\nCDecay MyD*+\nDecay MyB0\n1.000       MyD*- MyTau+ nu_tau   PHOTOS  ISGW2;\nEnddecay\nCDecay Myanti-B0\nEnd\n')
#        ),
#        parameterSets = cms.vstring('EvtGen130')
#    ),
#    PythiaParameters = cms.PSet(
#        parameterSets = cms.vstring(
#            'pythia8CommonSettings', 
#            'pythia8CP5Settings', 
#            'processParameters'
#        ),
#        processParameters = cms.vstring(
#            'SoftQCD:nonDiffractive = on', 
#            'PTFilter:filter = on', 
#            'PTFilter:quarkToFilter = 5', 
#            'PTFilter:scaleToFilter = 5.0', 
#            '300553:new = 300553 -300553 1 0 0 1.0579400e+01 2.0500001e-02 10.5584 10.6819 0.0000000e+00', 
#            '100313:new = 100313 -100313 1 0 0 1.4140000e+00 2.3199996e-01 0.254 2.574 0.0000000e+00', 
#            '100323:new = 100323 -100323 1 1 0 1.4140000e+00 2.3199996e-01 0.254 2.574 0.0000000e+00', 
#            '30343:new = 30343 -30343 1 0 0 1.6000000e+00 0.0000000e+00 1.6 1.6 0.0000000e+00', 
#            '30353:new = 30353 -30353 1 1 0 1.6000000e+00 0.0000000e+00 1.6 1.6 0.0000000e+00', 
#            '30363:new = 30363 -30363 1 0 0 1.8000000e+00 0.0000000e+00 1.8 1.8 0.0000000e+00', 
#            '9020221:new = 9020221 -9020221 0 0 0 1.4089000e+00 5.1100000e-02 1.1534 1.6644 3.8616000e-12', 
#            '9000443:new = 9000443 -9000443 1 0 0 4.0390000e+00 8.0000005e-02 3.639 4.439 0.0000000e+00', 
#            '9010443:new = 9010443 -9010443 1 0 0 4.1530000e+00 7.8000000e-02 3.763 4.543 0.0000000e+00', 
#            '9020443:new = 9020443 -9020443 1 0 0 4.4210000e+00 6.1999976e-02 4.111 4.731 0.0000000e+00', 
#            '110551:new = 110551 -110551 0 0 0 1.0232500e+01 0.0000000e+00 10.2325 10.2325 0.0000000e+00', 
#            '120553:new = 120553 -120553 1 0 0 1.0255500e+01 0.0000000e+00 10.2555 10.2555 0.0000000e+00', 
#            '100555:new = 100555 -100555 2 0 0 1.0268600e+01 0.0000000e+00 10.2686 10.2686 0.0000000e+00', 
#            '210551:new = 210551 -210551 0 0 0 1.0500700e+01 0.0000000e+00 10.5007 10.5007 0.0000000e+00', 
#            '220553:new = 220553 -220553 1 0 0 1.0516000e+01 0.0000000e+00 10.516 10.516 0.0000000e+00', 
#            '200555:new = 200555 -200555 2 0 0 1.0526400e+01 0.0000000e+00 10.5264 10.5264 0.0000000e+00', 
#            '130553:new = 130553 -130553 1 0 0 1.0434900e+01 0.0000000e+00 10.4349 10.4349 0.0000000e+00', 
#            '30553:new = 30553 -30553 1 0 0 1.0150100e+01 0.0000000e+00 10.1501 10.1501 0.0000000e+00', 
#            '20555:new = 20555 -20555 2 0 0 1.0156200e+01 0.0000000e+00 10.1562 10.1562 0.0000000e+00', 
#            '120555:new = 120555 -120555 2 0 0 1.0440600e+01 0.0000000e+00 10.4406 10.4406 0.0000000e+00', 
#            '557:new = 557 -557 3 0 0 1.0159900e+01 0.0000000e+00 10.1599 10.1599 0.0000000e+00', 
#            '100557:new = 100557 -100557 3 0 0 1.0444300e+01 0.0000000e+00 10.4443 10.4443 0.0000000e+00', 
#            '110553:new = 110553 -110553 1 0 0 1.0255000e+01 0.0000000e+00 10.255 10.255 0.0000000e+00', 
#            '210553:new = 210553 -210553 1 0 0 1.0516000e+01 0.0000000e+00 10.516 10.516 0.0000000e+00', 
#            '110555:new = 110555 -110555 2 0 0 1.0441000e+01 0.0000000e+00 10.441 10.441 0.0000000e+00', 
#            '10555:new = 10555 -10555 2 0 0 1.0157000e+01 0.0000000e+00 10.157 10.157 0.0000000e+00', 
#            '13124:new = 13124 -13124 1.5 0 0 1.6900000e+00 6.0000018e-02 1.39 1.99 0.0000000e+00', 
#            '43122:new = 43122 -43122 0.5 0 0 1.8000000e+00 2.9999996e-01 0.3 3.3 0.0000000e+00', 
#            '53122:new = 53122 -53122 0.5 0 0 1.8100000e+00 1.5000001e-01 1.06 2.56 0.0000000e+00', 
#            '13126:new = 13126 -13126 2.5 0 0 1.8300000e+00 9.5000007e-02 1.355 2.305 0.0000000e+00', 
#            '13212:new = 13212 -13212 0.5 0 0 1.6600000e+00 1.0000000e-01 1.16 2.16 0.0000000e+00', 
#            '3126:new = 3126 -3126 2.5 0 0 1.8200000e+00 7.9999995e-02 1.42 2.22 0.0000000e+00', 
#            '3216:new = 3216 -3216 2.5 0 0 1.7750000e+00 1.1999999e-01 1.175 2.375 0.0000000e+00', 
#            '14124:new = 14124 -14124 2.5 1 0 2.626600 0 2.626600 2.626600 0.0000000e+00'
#        ),
#        pythia8CP5Settings = cms.vstring(
#            'Tune:pp 14', 
#            'Tune:ee 7', 
#            'MultipartonInteractions:ecmPow=0.03344', 
#            'PDF:pSet=20', 
#            'MultipartonInteractions:bProfile=2', 
#            'MultipartonInteractions:pT0Ref=1.41', 
#            'MultipartonInteractions:coreRadius=0.7634', 
#            'MultipartonInteractions:coreFraction=0.63', 
#            'ColourReconnection:range=5.176', 
#            'SigmaTotal:zeroAXB=off', 
#            'SpaceShower:alphaSorder=2', 
#            'SpaceShower:alphaSvalue=0.118', 
#            'SigmaProcess:alphaSvalue=0.118', 
#            'SigmaProcess:alphaSorder=2', 
#            'MultipartonInteractions:alphaSvalue=0.118', 
#            'MultipartonInteractions:alphaSorder=2', 
#            'TimeShower:alphaSorder=2', 
#            'TimeShower:alphaSvalue=0.118'
#        ),
#        pythia8CommonSettings = cms.vstring(
#            'Tune:preferLHAPDF = 2', 
#            'Main:timesAllowErrors = 10000', 
#            'Check:epTolErr = 0.01', 
#            'Beams:setProductionScalesFromLHEF = off', 
#            'SLHA:keepSM = on', 
#            'SLHA:minMassSM = 1000.', 
#            'ParticleDecays:limitTau0 = on', 
#            'ParticleDecays:tau0Max = 10', 
#            'ParticleDecays:allowPhotonRadiation = on'
#        )
#    ),
#    comEnergy = cms.double(13000.0),
#    maxEventsToPrint = cms.untracked.int32(0),
#    pythiaHepMCVerbosity = cms.untracked.bool(False),
#    pythiaPylistVerbosity = cms.untracked.int32(0)
#)

process.genParticlesPlusGEANT = cms.EDProducer("GenPlusSimParticleProducer",
  src           = cms.InputTag("g4SimHits"),
  setStatus     = cms.int32(8),                 # set status = 8 for GEANT GPs
  particleTypes = cms.vstring(),
  filter = cms.vstring(),
  genParticles  = cms.InputTag("genParticles") # original genParticle list
)

process.g4SimHits.Physics.type = cms.string('SimG4Core/Physics/CustomPhysics')
process.g4SimHits.Physics.RHadronDummyFlip = cms.bool(False)
process.g4SimHits.Physics.Verbosity = 1
process.g4SimHits.Physics = cms.PSet(
  process.g4SimHits.Physics, #keep all default value and add others
  particlesDef = cms.FileInPath('SimG4Core/CustomPhysics/data/particles_sexaq_1p8_GeV.txt'),
)
#process.g4SimHits.Generator.ApplyEtaCuts = cms.bool(False)

#process.g4SimHits.HepMCProductLabel = cms.InputTag("source", "generator")
#process.g4SimHits.Generator.HepMCProductLabel = cms.InputTag("source", "generator")
## Vtx Smearing done in hepmc 2 gen step
#process.VtxSmeared.src = cms.InputTag("source", "generator")
#process.genParticles.src = cms.InputTag("source", "generator")
process.g4SimHits.HepMCProductLabel = cms.InputTag("generatorSmeared")
process.g4SimHits.Generator.HepMCProductLabel = cms.InputTag("generatorSmeared")
# Vtx Smearing done in hepmc 2 gen step
process.VtxSmeared.src = cms.InputTag("source", "generator")
process.genParticles.src = cms.InputTag("generatorSmeared")

#process.ProductionFilterSequence = cms.Sequence(process.generator+process.tagfilter+process.tau_mufilter)

#make a cut on the daughters of the antiS: V0s which are created larger than 20cm should be cut (normally you could put the interaction cross section high, so they would all interact)
#Updated cut to 2.45 cm for 2018 BPH - new inner tracker supports go down to 2.5 cm - but we are only interested in interactions from the beampipe and surrounding air molecules
#process.genAntiSGranddaughterFilterKs = cms.EDFilter("CandViewSelector",
#     src = cms.InputTag("genParticlesPlusGEANT"),
#     cut = cms.string("abs(pdgId) == 310 && mother(0).pdgId == -1020000020 && sqrt(vx*vx+vy*vy) < 20")
#     )
process.genAntiSGranddaughterFilterKs = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("abs(pdgId) == 310 && mother(0).pdgId == -1020000020 && sqrt(vx*vx+vy*vy) < 2.45")
     )
process.NumgenAntiSGranddaughterFilterKs = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterKs"),
    minNumber = cms.uint32(1),
  )

#process.genAntiSGranddaughterFilterAntiLambda = cms.EDFilter("CandViewSelector",
#     src = cms.InputTag("genParticlesPlusGEANT"),
#     cut = cms.string("pdgId == -3122 && mother(0).pdgId == -1020000020 && sqrt(vx*vx+vy*vy) < 20")
#     )
process.genAntiSGranddaughterFilterAntiLambda = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("pdgId == -3122 && mother(0).pdgId == -1020000020 && sqrt(vx*vx+vy*vy) < 2.45")
     )
process.NumgenAntiSGranddaughterFilterAntiLambda = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterAntiLambda"),
    minNumber = cms.uint32(1),
  )

#cut on the presence of the two daughters
process.genAntiSGranddaughterFilterKsAntiLambdaPresent = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string(" pdgId == -1020000020 && numberOfDaughters() == 2 ")
     )
process.NumgenAntiSGranddaughterFilterKsAntiLambdaPresent = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterKsAntiLambdaPresent"),
    minNumber = cms.uint32(1),
  )


#make a cut on the granddaughters of the antiS: particles with too low momenta anyway have a reco efficiency close to 0 and also too large displaced particles have a reco efficiency of 0
process.genAntiSGranddaughterFilterKsPiMin = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("pdgId == -211 &&  abs(mother(0).pdgId) == 310 && mother(0).mother(0).pdgId == -1020000020 ")
     )
process.NumgenAntiSGranddaughterFilterKsPiMin = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterKsPiMin"),
    minNumber = cms.uint32(1),
  )

process.genAntiSGranddaughterFilterKsPiPlus = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("pdgId == 211 &&  abs(mother(0).pdgId) == 310 && mother(0).mother(0).pdgId == -1020000020 ")
     )
process.NumgenAntiSGranddaughterFilterKsPiPlus = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterKsPiPlus"),
    minNumber = cms.uint32(1),
  )

process.genAntiSGranddaughterFilterAntiLambdaPiPlus = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("pdgId == 211 &&  mother(0).pdgId == -3122 && mother(0).mother(0).pdgId == -1020000020 ")
     )
process.NumgenAntiSGranddaughterFilterAntiLambdaPiPlus = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterAntiLambdaPiPlus"),
    minNumber = cms.uint32(1),
  )

process.genAntiSGranddaughterFilterAntiLambdaAntiProton = cms.EDFilter("CandViewSelector",
     src = cms.InputTag("genParticlesPlusGEANT"),
     cut = cms.string("pdgId == -2212 &&  mother(0).pdgId == -3122 && mother(0).mother(0).pdgId == -1020000020 ")
     )
process.NumgenAntiSGranddaughterFilterAntiLambdaAntiProton = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genAntiSGranddaughterFilterAntiLambdaAntiProton"),
    minNumber = cms.uint32(1),
  )

# end of: make a cut on the granddaughters of the antiS: particles with too low momenta anyway have a reco efficiency close to 0 and also too large displaced particles have a reco efficiency of 1


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
#moved beamspot and vtx smearing to hepmc2gen step
#process.simulation_step = cms.Path(process.offlineBeamSpot*process.generatorSmeared*process.psim*process.genParticlesPlusGEANT)
process.simulation_step = cms.Path(process.psim*process.genParticlesPlusGEANT)
#process.simulation_step = cms.Path(process.psim*process.genParticlesPlusGEANT)
#process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step)
process.schedule = cms.Schedule(process.generation_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
## filter all path with the production filter sequence
#for path in process.paths:
#	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

from Configuration.DataProcessing.Utils import addMonitoring
process = addMonitoring(process)

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

# End adding early deletion
# For debug:
#print process.dumpPython()
