# SexaqSim
## Setup

This repository is meant to be used with CMSSW - the files herein should be copied into a separate directory with CMSSW 10_2_26 installed.

To clone this repository, do ``git clone https://github.com/vetens/SexaqSim.git``

I would recommend having it in a separate directory from this CMSSW, i.e. outside this directory you will set up CMSSW, and then copy these contents into the CMSSW directory

To set up the proper CMSSW environment - on a cluster which has CMSSW
installed, do:

```
cmsrel CMSSW_10_2_26
cd CMSSW_10_2_26/src
cmsenv
```

Then to check out the necessary packages for this simulation:

```
git cms-addpkg IOMC/Input
git cms-addpkg IOMC/EventVertexGenerators
git cms-addpkg SimG4Core/CustomPhysics
```
and make a directory for the configs you will use to run the simulation:

```
mkdir -p runGENSIM_Sexaq_withCuts/crab/
```

and copy the contents of this package into their corresponding folders in `CMSSW_10_2_26/src` - overwriting any pre-existing files of the same name, i.e. (still inside your CMSSW release directory) do:

```
cp -f <path to your SexaqSim package>/IOMC/Input/test/* IOMC/Input/test/.
cp -f <path to your SexaqSim package>/SimG4Core/CustomPhysics/data/* SimG4Core/CustomPhysics/data/.
cp -f <path to your SexaqSim package>/SimG4Core/CustomPhysics/interface/* SimG4Core/CustomPhysics/interface/.
cp -f <path to your SexaqSim package>/SimG4Core/CustomPhysics/src/* SimG4Core/CustomPhysics/src/.
cp -f <path to your SexaqSim package>/runGENSIM_Sexaq_withCuts/crab/* runGENSIM_Sexaq_withCuts/crab/.
```

Remember that to push changes to this repository, your edited files will have to be copied back to this directory and the old files overwritten. Unfortunately files must be copied back and forth in this way because the alternative would be cloning my full CMSSW repo with many more packages, which would take up much more time and space than with this method.

Next, download the Pileup fragment for MC made in B-parking conditions. Do:

```
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/BPH-RunIIFall18GS-00369 --retry 3 --create-dirs -o Configuration/GenProduction/python/BPH-RunIIFall18GS-00369-fragment.py
[ -s Configuration/GenProduction/python/BPH-RunIIFall18GS-00369-fragment.py ]
```

Once all files are copied over, it is time to build CMSSW with the custom Sexaquark physics implemented. Do:

```
scram b -j 8
cmsenv
```

and now you are prepared to run your simulation.


## Running the Simulation

Once CMSSW is built, one can simply go to the directory where the config is stored and run it using `cmsRun`:

```
cd runGENSIM_Sexaq_withCuts/crab/
cmsRun BPH-RunIIFall18GenSim-00369_Sexaq_cfg.py inputFiles=file:<Input GEN root file> outputFile=file:<Desired name of output GENSIM root file> maxEvents=<maxEvents (usually should do 4000)>
```

the `file:` prefix for output & input files refers to files which are local. Remotely accessed files (i.e. from storage on a remote T2) should instead have the `root:` prefix (grid certificate needed). 


## Multiple files through CRAB

Config file for CRAB jobs is `runGENSIM_Sexaq_withCuts/crab/crabConfig_MC_SIM_step_withBash_test_with_publication.py`. Once parameters have been edited to one's preference, with active VOMS certificate, in the `runGENSIM_Sexaq_withCuts/crab/` directory do:

```
crab submit crabConfig_MC_SIM_step_withBash_test_with_publication.py
```

## DIGIRECO step

Clone my analysis code in the same `CMSSW_10_2_26/src` area as above:

```
git clone https://github.com/vetens/SexaQAnalysis.git
```

Make sure you are on the `master` branch with `SexaQAnalysis` by running:

```
cd SexaQAnalysis/
git checkout master
cd ../
```

 and again run,

```
scram b -j 8
cmsenv
```

To build the new packages. 

Copy over ``runDIGIREKOSKIM_Sexaq_withCuts/crab`` and all its contents as with the GENSIM step. Just as with GENSIM, use the ``BPH-RunII<stuff>_cfg.py`` to run locally and the ``crabConfig<stuff>.py`` to run with CRAB. The reconstruction takes a VERY LONG TIME, so there is also a scaffolding for condor scripts to run your test job remotely. Just update  `condor_test.cfg` and `Test.sh` with your own environment and proxy info and submit with:

```
condor_submit condor_test.cfg
```

## NTuple Production

NTuple production macros are all in the `SexaQAnalysis` module, with the `cmsRun` configs in `AnalyzerAllSteps/test` and the plotting macros in `AnalyzerAllSteps/macros`.
