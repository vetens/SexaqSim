#!/usr/bin/env cmsRun

## Original Author: Andrea Carlo Marini
## Porting to 92X HepMC 2 Gen 
## Date of porting: Mon Jul  3 11:52:22 CEST 2017
## Example of hepmc -> gen file
import os,sys
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
#options.inputFiles = 'file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/Sexaquark_13TeV_trial2/crmc_Sexaq_100.hepmc', 'file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/Sexaquark_13TeV_trial2/crmc_Sexaq_102.hepmc'
options.parseArguments()

#if True:
#    print('-> You are using a 2 process file to unzip/untar events on the fly')
#    #cmd = "mkfifo /tmp/amarini/hepmc10K.dat"
#    #cmd = "cat hepmc10K.dat.gz | gunzip -c > /tmp/amarini/hepmc10K.dat"
#    from subprocess import call, check_output
#    import threading
#    import time
#    def call_exe(cmd):
#        print("-> Executing cmd: '"+cmd+"'")
#        st=call(cmd,shell=True)
#        print("-> End cmd: status=",st)
#        return
#    cmd="rm /tmp/"+os.environ['USER']+"/hepmc10K.dat"
#    call(cmd,shell=True)
#    cmd="mkfifo /tmp/"+os.environ['USER']+"/hepmc10K.dat"
#    call(cmd,shell=True)
#    exe="cat /tmp/"+os.environ['USER']+"/hepmc.dat.tgz | gunzip -c > /tmp/"+os.environ['USER']+"/hepmc10K.dat &"
#    t = threading.Thread(target=call_exe, args= ( [exe] )  )
#    t.start()
#    print("(sleep 1s to allow start of pipes)")
#    time.sleep(1)



import FWCore.ParameterSet.Config as cms

process = cms.Process("GEN")


process.source = cms.Source("MCFileSource",
		    #fileNames = cms.untracked.vstring('file:hepmc100.dat'),
			#fileNames = cms.untracked.vstring('file:../../../crmc_eposlhc_347761894_p_p_6500.hepmc'),
			fileNames = cms.untracked.vstring(options.inputFiles),
			)


maxEvents=options.maxEvents
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxEvents))


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(500)

process.GEN = cms.OutputModule("PoolOutputModule",
		#fileName = cms.untracked.string("HepMC_Gen.root"),
		fileName = cms.untracked.string(options.outputFile),
        	SelectEvents = cms.untracked.PSet(
                SelectEvents = cms.vstring('p')
                )
	)



process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('RecoVertex.BeamSpotProducer.BeamSpot_cfi')

process.genParticles = cms.EDProducer("GenParticleProducer",
                src = cms.InputTag("source", "generator"),
                abortOnUnknownPDGCode = cms.untracked.bool(False)
                )

process.antisexaqev = cms.EDFilter("PdgIdCandViewSelector",
    src = cms.InputTag("genParticles"),
    pdgId = cms.vint32(-1020000020)  # replaced in loop
)

process.NumAntiSexaqevFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("antisexaqev"),
    minNumber = cms.uint32(1),
  )
process.MaxNumAntiSexaqevFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("antisexaqev"),
    minNumber = cms.uint32(2),
  )

process.etaptmin= cms.EDFilter("EtaPtMinCandViewSelector",
    src = cms.InputTag("antisexaqev"),
    minNumber = cms.uint32(1),
    ptMin = cms.double(0.),
    etaMin = cms.double(-5),
    etaMax = cms.double(5),
  )



######### Smearing Vertex example
#stanadard configuration
#from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import GaussVtxSmearingParameters,VtxSmearedCommon
#VtxSmearedCommon.src=cms.InputTag("source")
#process.generatorSmeared = cms.EDProducer("GaussEvtVtxGenerator",
#    GaussVtxSmearingParameters,
#    VtxSmearedCommon
#    )

#adaped by Jarne/Wren:
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')

from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import Realistic25ns13TeVEarly2018CollisionVtxSmearingParameters,VtxSmearedCommon
VtxSmearedCommon.src=cms.InputTag("source", "generator")
process.generatorSmeared = cms.EDProducer("BetafuncEvtVtxGenerator",
    Realistic25ns13TeVEarly2018CollisionVtxSmearingParameters,
    VtxSmearedCommon
    )

#from PV distribution in data: SingleMuon_Run2016H - the actual x location of the beampipe: 0.05803-0.124
#from PV distribution in data: SingleMuon_Run2016H - the actual y location of the beampipe: 0.1075-0.027
#from PV distribution in data: SingleMuon_Run2016H 
#process.generatorSmeared= cms.EDProducer("BetafuncEvtVtxGenerator",
#    Phi = cms.double(0.0),
#    BetaStar = cms.double(65.0),
#    Emittance = cms.double(5.411e-08),
#    Alpha = cms.double(0.0),
#    SigmaZ = cms.double(5.3),
#    TimeOffset = cms.double(0.0),
#    X0 = cms.double(-0.06597),
#    Y0 = cms.double(0.0805),
#    Z0 = cms.double(-1.0985),
#    src = cms.InputTag("source"),
#    readDB = cms.bool(False)
#)


process.load('Configuration.StandardSequences.Services_cff')
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
        generatorSmeared  = cms.PSet( initialSeed = cms.untracked.uint32(1243987),
            engineName = cms.untracked.string('TRandom3'),
            ),
        )

#process.fiducial = cms.EDFilter("EtaPtMinPdgIdCandSelector",
#  src = cms.InputTag("source", "generator"),
#  ptMin = cms.double(0.),
#  etaMin = cms.double(-999),
#  etaMax = cms.double(999),
#  pdgId = cms.vint32(-1020000020)
#)
#
#process.NumAntiSexaqevFilter = cms.EDFilter("CandViewCountFilter",
#    src = cms.InputTag("source", "generator"),
#    minNumber = cms.uint32(1)
#  )


###################
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
#trying without max number filter
#process.p = cms.Path(process.genParticles * process.offlineBeamSpot * process.generatorSmeared * process.antisexaqev * process.NumAntiSexaqevFilter * ~process.MaxNumAntiSexaqevFilter * process.etaptmin)
process.p = cms.Path(process.genParticles * process.offlineBeamSpot * process.generatorSmeared * process.antisexaqev * process.NumAntiSexaqevFilter * process.etaptmin)
#Trying without max number or eta filter
#process.p = cms.Path(process.genParticles * process.offlineBeamSpot * process.generatorSmeared * process.antisexaqev * process.NumAntiSexaqevFilter)
#process.p = cms.Path(process.genParticles * process.generatorSmeared  )
process.outpath = cms.EndPath(process.GEN)

### TO DO: add the following
# (amarini/hepmc_portTo9X)
# add the following line after the sim and digi loading
# generator needs to be smeared if you want vertex smearing, you'll have:
#       Type                                  Module               Label         Process   
#       -----------------------------------------------------------------------------------
#       GenEventInfoProduct                   "source"             "generator"   "GEN"     
#       edm::HepMCProduct                     "generatorSmeared"   ""            "GEN"     
#       edm::HepMCProduct                     "source"             "generator"   "GEN"   
# NOT needed to be changed if you smear the generator
#process.g4SimHits.HepMCProductLabel = cms.InputTag("source")
#process.g4SimHits.Generator.HepMCProductLabel = cms.InputTag("source")
#process.genParticles.src=  cms.InputTag("source","generator","GEN")


### ADD in the different step the following  (always!)
#
#process.AODSIMoutput.outputCommands.extend([
#		'keep GenRunInfoProduct_*_*_*',
#        	'keep GenLumiInfoProduct_*_*_*',
#		'keep GenEventInfoProduct_*_*_*',
#		])
#
#process.MINIAODSIMoutput.outputcommands.extend([
#       'keep GenRunInfoProduct_*_*_*',
#       'keep GenLumiInfoProduct_*_*_*',
#       'keep GenEventInfoProduct_*_*_*',
#	])
#
# and finally in the ntuples
#process.myanalyzer.generator = cms.InputTag("source","generator")

#print process.dumpPython()
