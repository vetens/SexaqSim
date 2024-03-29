//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************


#include "G4SQInelasticProcess.hh"
#include "G4SQ.hh"

#include "G4Types.hh"
#include "G4SystemOfUnits.hh"
#include "G4HadProjectile.hh"
#include "G4ElementVector.hh"
#include "G4Track.hh"
#include "G4Step.hh"
#include "G4Element.hh"
#include "G4ParticleChange.hh"
#include "G4TransportationManager.hh"
#include "G4Navigator.hh"
#include "G4ProcessVector.hh"
#include "G4ProcessManager.hh"
#include "G4StableIsotopes.hh"
#include "G4HadTmpUtil.hh"
#include "G4NucleiProperties.hh"

#include "G4HadronicException.hh"
#include "G4HadronicProcessStore.hh"

#include <typeinfo>
#include <sstream>
#include <iostream>

#include <stdlib.h>

#include "G4HadronInelasticDataSet.hh"
#include "G4ParticleDefinition.hh"


// File-scope variable to capture environment variable at startup

static const char* G4Hadronic_Random_File = getenv("G4HADRONIC_RANDOM_FILE");

static const G4int resetprescale = 100;

//////////////////////////////////////////////////////////////////
G4SQInelasticProcess::G4SQInelasticProcess(double mass, const G4String& processName)
 : G4HadronicProcess(processName, fHadronic)
{
  SetProcessSubType(fHadronInelastic);	// Default unless subclass changes
  
  theTotalResult = new G4ParticleChange();
  theTotalResult->SetSecondaryWeightByProcess(true);
  theInteraction = 0;
  theCrossSectionDataStore = new G4CrossSectionDataStore();
  G4HadronicProcessStore::Instance()->Register(this);
  aScaleFactor = resetprescale;
  xBiasOn = false;
  G4SQInelasticProcess_debug_flag = false;

  GetEnergyMomentumCheckEnvvars();

  AddDataSet(new G4HadronInelasticDataSet());
  theParticle = G4SQ::SQ(mass);

}


G4SQInelasticProcess::~G4SQInelasticProcess()
{
  G4HadronicProcessStore::Instance()->DeRegister(this);
  delete theTotalResult;
  delete theCrossSectionDataStore;
}


G4bool G4SQInelasticProcess::IsApplicable(const G4ParticleDefinition& aP)
{
  return  theParticle->GetParticleType() == aP.GetParticleType();
}


void G4SQInelasticProcess::GetEnergyMomentumCheckEnvvars() {
  levelsSetByProcess = false;

  epReportLevel = getenv("G4Hadronic_epReportLevel") ?
    strtol(getenv("G4Hadronic_epReportLevel"),0,10) : 0;

  epCheckLevels.first = getenv("G4Hadronic_epCheckRelativeLevel") ?
    strtod(getenv("G4Hadronic_epCheckRelativeLevel"),0) : DBL_MAX;

  epCheckLevels.second = getenv("G4Hadronic_epCheckAbsoluteLevel") ?
    strtod(getenv("G4Hadronic_epCheckAbsoluteLevel"),0) : DBL_MAX;
}

void G4SQInelasticProcess::RegisterMe( G4HadronicInteraction *a )
{
  if(!a) { return; }
  try{GetManagerPointer()->RegisterMe( a );}
  catch(G4HadronicException & aE)
  {
    G4ExceptionDescription ed;
    aE.Report(ed);
    ed << "Unrecoverable error in " << GetProcessName()
       << " to register " << a->GetModelName() << G4endl;
    G4Exception("G4SQInelasticProcess::RegisterMe", "had001", FatalException,
		ed);
  }
  G4HadronicProcessStore::Instance()->RegisterInteraction(this, a);
}

void G4SQInelasticProcess::PreparePhysicsTable(const G4ParticleDefinition& p)
{
  if(getenv("G4SQInelasticProcess_debug")) {
    G4SQInelasticProcess_debug_flag = true;
  }
  G4HadronicProcessStore::Instance()->RegisterParticle(this, &p);
}

void G4SQInelasticProcess::BuildPhysicsTable(const G4ParticleDefinition& p)
{
  try
  {
    theCrossSectionDataStore->BuildPhysicsTable(p);
  }
  catch(G4HadronicException aR)
  {
    G4ExceptionDescription ed;
    aR.Report(ed);
    ed << " hadronic initialisation fails" << G4endl;
    G4Exception("G4SQInelasticProcess::BuildPhysicsTable", "had000", 
		FatalException,ed);
  }
  G4HadronicProcessStore::Instance()->PrintInfo(&p);
}


G4double G4SQInelasticProcess::
GetMeanFreePath(const G4Track &aTrack, G4double, G4ForceCondition *)
{
  try
  {
    theLastCrossSection = aScaleFactor*
      theCrossSectionDataStore->GetCrossSection(aTrack.GetDynamicParticle(),
						aTrack.GetMaterial());
  }
  catch(G4HadronicException aR)
  {
    G4ExceptionDescription ed;
    aR.Report(ed);
    DumpState(aTrack,"GetMeanFreePath",ed);
    ed << " Cross section is not available" << G4endl;
    G4Exception("G4SQInelasticProcess::GetMeanFreePath", "had002", FatalException,
		ed);
  }
  G4double res = DBL_MAX;
  if( theLastCrossSection > 0.0 ) { res = 1.0/theLastCrossSection; }

  return res;
}


G4VParticleChange*
G4SQInelasticProcess::PostStepDoIt(const G4Track& aTrack, const G4Step& aStep)
{

  std::cout << "G4SQInelasticProcess::PostStepDoIt particle is going to interact at position" << aTrack.GetPosition()/cm << " momentumdirection eta: " << aTrack.GetMomentumDirection().eta() << std::endl;
  //std::cout << "G4SQInelasticProcess::PostStepDoIt particle is interacting in material : " << aTrack.GetMaterial() << std::endl; 
  // if primary is not Alive then do nothing
  theTotalResult->Clear();
  theTotalResult->Initialize(aTrack);
  theTotalResult->ProposeWeight(aTrack.GetWeight());
  if(aTrack.GetTrackStatus() != fAlive) {std::cout << "no interaction because primary is not alive" << std::endl; return theTotalResult; }


std::cout << "=== Interaction!?" << std::endl;

  if(aTrack.GetPosition().rho()/centimeter < 1) std::cout << "the rho of the track is < 1cm and it's going to interact..." << std::endl;

  // Find cross section at end of step and check if <= 0
  //
  G4DynamicParticle* aParticle = const_cast<G4DynamicParticle *>(aTrack.GetDynamicParticle());

  G4Material* aMaterial = aTrack.GetMaterial();

  G4Element* anElement = 0;
  try
  {
     anElement = theCrossSectionDataStore->SampleZandA(aParticle,
						       aMaterial,
						       targetNucleus);
  }
  catch(G4HadronicException & aR)
  {
    G4ExceptionDescription ed;
    aR.Report(ed);
    DumpState(aTrack,"SampleZandA",ed);
    ed << " PostStepDoIt failed on element selection" << G4endl;
    G4Exception("G4SQInelasticProcess::PostStepDoIt", "had003", FatalException,
		ed);
  }

  // check only for charged particles
  if(aParticle->GetDefinition()->GetPDGCharge() != 0.0) {
    if (GetElementCrossSection(aParticle, anElement, aMaterial) <= 0.0) {
      // No interaction
      return theTotalResult;
    }    
  }

  // Next check for illegal track status
  //
  if (aTrack.GetTrackStatus() != fAlive && aTrack.GetTrackStatus() != fSuspend) {
std::cout << "=== SL track status not ok: " << aTrack.GetTrackStatus() << std::endl;
    if (aTrack.GetTrackStatus() == fStopAndKill ||
        aTrack.GetTrackStatus() == fKillTrackAndSecondaries ||
        aTrack.GetTrackStatus() == fPostponeToNextEvent) {
      G4ExceptionDescription ed;
      ed << "G4SQInelasticProcess: track in unusable state - "
	 << aTrack.GetTrackStatus() << G4endl;
      ed << "G4SQInelasticProcess: returning unchanged track " << G4endl;
      DumpState(aTrack,"PostStepDoIt",ed);
      G4Exception("G4SQInelasticProcess::PostStepDoIt", "had004", JustWarning, ed);
    }
    // No warning for fStopButAlive which is a legal status here
    return theTotalResult;
  }

  // Go on to regular case
  //
  G4double originalEnergy = aParticle->GetKineticEnergy();
  G4double kineticEnergy = originalEnergy;

  // Get kinetic energy per nucleon for ions
  if(aParticle->GetParticleDefinition()->GetBaryonNumber() > 1.5)
          kineticEnergy/=aParticle->GetParticleDefinition()->GetBaryonNumber();

  try
  {
    theInteraction =
      ChooseHadronicInteraction( kineticEnergy, aMaterial, anElement );
  }
  catch(G4HadronicException & aE)
  {
    G4ExceptionDescription ed;
    aE.Report(ed);
    ed << "Target element "<<anElement->GetName()<<"  Z= "
       << targetNucleus.GetZ_asInt() << "  A= "
       << targetNucleus.GetA_asInt() << G4endl;
    DumpState(aTrack,"ChooseHadronicInteraction",ed);
    ed << " No HadronicInteraction found out" << G4endl;
    G4Exception("G4SQInelasticProcess::PostStepDoIt", "had005", FatalException,
		ed);
  }

  // Initialize the hadronic projectile from the track
  thePro.Initialise(aTrack);
  G4HadFinalState* result = 0;
  G4int reentryCount = 0;


  do
  {
    try
    {
      // Save random engine if requested for debugging
      if (G4Hadronic_Random_File) {
         CLHEP::HepRandom::saveEngineStatus(G4Hadronic_Random_File);
      }
      // Call the interaction
      result = theInteraction->ApplyYourself( thePro, targetNucleus);
      ++reentryCount;
    }
    catch(G4HadronicException aR)
    {
      G4ExceptionDescription ed;
      aR.Report(ed);
      ed << "Call for " << theInteraction->GetModelName() << G4endl;
      ed << "Target element "<<anElement->GetName()<<"  Z= "
	 << targetNucleus.GetZ_asInt()
	 << "  A= " << targetNucleus.GetA_asInt() << G4endl;
      DumpState(aTrack,"ApplyYourself",ed);
      ed << " ApplyYourself failed" << G4endl;
      G4Exception("G4SQInelasticProcess::PostStepDoIt", "had006", FatalException,
		  ed);
    }



      std::cout << "Call for " << theInteraction->GetModelName() << std::endl;
      std::cout << "Target element "<<anElement->GetName()<<"  Z= "
	 << targetNucleus.GetZ_asInt()
	 << "  A= " << targetNucleus.GetA_asInt() << std::endl;

std::cout << "$$$--- " << result->GetNumberOfSecondaries() << " " <<
  result->GetMomentumChange() << " " 
  << result->GetLocalEnergyDeposit() << " "
  << aTrack.GetPosition() << " "
  << aTrack.GetVertexPosition()
  << std::endl;

float r = aTrack.GetPosition().perp();
float z = fabs(aTrack.GetPosition().z());
std::cout << "In tracker volume? "
          << (r<(100*cm) && z<(200*cm)? "YES " : "NO  ")
          << "r=" << r/cm << " z=" << z/cm << std::endl;

    // Check the result for catastrophic energy non-conservation
    result = CheckResult(thePro,targetNucleus, result);
    if(reentryCount>100) {
      G4ExceptionDescription ed;
      ed << "Call for " << theInteraction->GetModelName() << G4endl;
      ed << "Target element "<<anElement->GetName()<<"  Z= "
	 << targetNucleus.GetZ_asInt()
	 << "  A= " << targetNucleus.GetA_asInt() << G4endl;
      DumpState(aTrack,"ApplyYourself",ed);
      ed << " ApplyYourself does not completed after 100 attempts" << G4endl;
      G4Exception("G4SQInelasticProcess::PostStepDoIt", "had006", FatalException,
		  ed);
    }
  }
  while(!result);
std::cout << "=== SL Interaction succeeded!" << std::endl;

  result->SetTrafoToLab(thePro.GetTrafoToLab());

  ClearNumberOfInteractionLengthLeft();

  FillResult(result, aTrack);

  if (epReportLevel != 0) {
    CheckEnergyMomentumConservation(aTrack, targetNucleus);
  }
  return theTotalResult;
}


void G4SQInelasticProcess::ProcessDescription(std::ostream& outFile) const
{
  outFile << "The description for this process has not been written yet.\n";
}


G4double G4SQInelasticProcess::XBiasSurvivalProbability()
{
  G4double result = 0;
  G4double nLTraversed = GetTotalNumberOfInteractionLengthTraversed();
  G4double biasedProbability = 1.-std::exp(-nLTraversed);
  G4double realProbability = 1-std::exp(-nLTraversed/aScaleFactor);
  result = (biasedProbability-realProbability)/biasedProbability;
  return result;
}

G4double G4SQInelasticProcess::XBiasSecondaryWeight()
{
  G4double result = 0;
  G4double nLTraversed = GetTotalNumberOfInteractionLengthTraversed();
  result =
     1./aScaleFactor*std::exp(-nLTraversed/aScaleFactor*(1-1./aScaleFactor));
  return result;
}

void
G4SQInelasticProcess::FillResult(G4HadFinalState * aR, const G4Track & aT)
{
  theTotalResult->ProposeLocalEnergyDeposit(aR->GetLocalEnergyDeposit());

  G4double rotation = CLHEP::twopi*G4UniformRand();
  G4ThreeVector it(0., 0., 1.);

  G4double efinal = aR->GetEnergyChange();
  if(efinal < 0.0) { efinal = 0.0; }

  // check status of primary
  if(aR->GetStatusChange() == stopAndKill) {
    theTotalResult->ProposeTrackStatus(fStopAndKill);
    theTotalResult->ProposeEnergy( 0.0 );
std::cout << "=== SL track proposed to stop and kill" << std::endl;

    // check its final energy
  } else if(0.0 == efinal) {
    theTotalResult->ProposeEnergy( 0.0 );
    if(aT.GetParticleDefinition()->GetProcessManager()
       ->GetAtRestProcessVector()->size() > 0)
         { aParticleChange.ProposeTrackStatus(fStopButAlive); }
    else { aParticleChange.ProposeTrackStatus(fStopAndKill); 
std::cout << "=== SL track proposed to stop and kill (2)" << std::endl;
}

    // primary is not killed apply rotation and Lorentz transformation
  } else  {
    theTotalResult->ProposeTrackStatus(fAlive);
    G4double mass = aT.GetParticleDefinition()->GetPDGMass();
    G4double newE = efinal + mass;
    G4double newP = std::sqrt(efinal*(efinal + 2*mass));
    G4ThreeVector newPV = newP*aR->GetMomentumChange();
    G4LorentzVector newP4(newE, newPV);
    newP4.rotate(rotation, it);
    newP4 *= aR->GetTrafoToLab();
    theTotalResult->ProposeMomentumDirection(newP4.vect().unit());
    newE = newP4.e() - mass;
    if(G4SQInelasticProcess_debug_flag && newE <= 0.0) {
      G4ExceptionDescription ed;
      DumpState(aT,"Primary has zero energy after interaction",ed);
      G4Exception("G4SQInelasticProcess::FillResults", "had011", JustWarning, ed);
    }
    if(newE < 0.0) { newE = 0.0; }
    theTotalResult->ProposeEnergy( newE );
  }

  // check secondaries: apply rotation and Lorentz transformation
  G4int nSec = aR->GetNumberOfSecondaries();
  theTotalResult->SetNumberOfSecondaries(nSec);
  G4double weight = aT.GetWeight();

  if (nSec > 0) {
    G4double time0 = aT.GetGlobalTime();
    for (G4int i = 0; i < nSec; ++i) {
      G4LorentzVector theM = aR->GetSecondary(i)->GetParticle()->Get4Momentum();
      theM.rotate(rotation, it);
      theM *= aR->GetTrafoToLab();
      aR->GetSecondary(i)->GetParticle()->Set4Momentum(theM);

      // time of interaction starts from zero
      G4double time = aR->GetSecondary(i)->GetTime();
      if (time < 0.0) { time = 0.0; }

      // take into account global time
      time += time0;

      G4Track* track = new G4Track(aR->GetSecondary(i)->GetParticle(),
                                   time, aT.GetPosition());
      G4double newWeight = weight*aR->GetSecondary(i)->GetWeight();
	// G4cout << "#### ParticleDebug "
	// <<GetProcessName()<<" "
	// <<aR->GetSecondary(i)->GetParticle()->GetDefinition()->GetParticleName()<<" "
	// <<aScaleFactor<<" "
	// <<XBiasSurvivalProbability()<<" "
	// <<XBiasSecondaryWeight()<<" "
	// <<aT.GetWeight()<<" "
	// <<aR->GetSecondary(i)->GetWeight()<<" "
	// <<aR->GetSecondary(i)->GetParticle()->Get4Momentum()<<" "
	// <<G4endl;
      track->SetWeight(newWeight);
      track->SetTouchableHandle(aT.GetTouchableHandle());
      theTotalResult->AddSecondary(track);
      if (G4SQInelasticProcess_debug_flag) {
        G4double e = track->GetKineticEnergy();
        if (e <= 0.0) {
          G4ExceptionDescription ed;
          DumpState(aT,"Secondary has zero energy",ed);
          ed << "Secondary " << track->GetDefinition()->GetParticleName()
             << G4endl;
          G4Exception("G4SQInelasticProcess::FillResults", "had011", JustWarning,ed);
        }
      }
    }
  }

  aR->Clear();
  return;
}


void G4SQInelasticProcess::BiasCrossSectionByFactor(G4double aScale)
{
  xBiasOn = true;
  aScaleFactor = aScale;
  G4String it = GetProcessName();
  if( (it != "PhotonInelastic") &&
      (it != "ElectroNuclear") &&
      (it != "PositronNuclear") )
    {
      G4ExceptionDescription ed;
      G4Exception("G4SQInelasticProcess::BiasCrossSectionByFactor", "had009", FatalException, ed,
		  "Cross-section biasing available only for gamma and electro nuclear reactions.");
    }
  if(aScale<100)
    {
      G4ExceptionDescription ed;
      G4Exception("G4SQInelasticProcess::BiasCrossSectionByFactor", "had010", JustWarning,ed,
		  "Cross-section bias readjusted to be above safe limit. New value is 100");
      aScaleFactor = 100.;
    }
}

G4HadFinalState* G4SQInelasticProcess::CheckResult(const G4HadProjectile & aPro,const G4Nucleus &aNucleus, G4HadFinalState * result) const
{
   // check for catastrophic energy non-conservation, to re-sample the interaction

   G4HadronicInteraction * theModel = GetHadronicInteraction();
std::cout << "%%% SL checkresult: " << theModel << std::endl;
   G4double nuclearMass(0);
   if (theModel){

      // Compute final-state total energy
      G4double finalE(0.);
      G4int nSec = result->GetNumberOfSecondaries();

      nuclearMass = G4NucleiProperties::GetNuclearMass(aNucleus.GetA_asInt(),
                                                       aNucleus.GetZ_asInt());
      if (result->GetStatusChange() != stopAndKill) {
       	// Interaction didn't complete, returned "do nothing" state          => reset nucleus
        //  or  the primary survived the interaction (e.g. electro-nuclear ) => keep  nucleus
         finalE=result->GetLocalEnergyDeposit() +
		aPro.GetDefinition()->GetPDGMass() + result->GetEnergyChange();
std::cout << "%%% SL interaction not complete: " << finalE << std::endl;
         if( nSec == 0 ){
            // Since there are no secondaries, there is no recoil nucleus.
            // To check energy balance we must neglect the initial nucleus too.
            nuclearMass=0.0;
         }
      }
      for (G4int i = 0; i < nSec; i++) {
         finalE += result->GetSecondary(i)->GetParticle()->GetTotalEnergy();
std::cout << "%%% SL sec: " 
<< result->GetSecondary(i)->GetParticle()->GetPDGcode() << "\t"
<< result->GetSecondary(i)->GetParticle()->GetTotalEnergy() / GeV
<< std::endl;
      }
      G4double deltaE= nuclearMass +  aPro.GetTotalEnergy() -  finalE;
std::cout << "%%% SL TOT E: " << nuclearMass / GeV << " " << aPro.GetTotalEnergy() / GeV << " " << finalE / GeV << std::endl;
std::cout << "%%% SL deltaE: " << deltaE / GeV << std::endl;

      std::pair<G4double, G4double> checkLevels = theModel->GetFatalEnergyCheckLevels();	// (relative, absolute)
      if (std::abs(deltaE) > checkLevels.second && std::abs(deltaE) > checkLevels.first*aPro.GetKineticEnergy()){
         // do not delete result, this is a pointer to a data member;
// SL SL SL tmp switchoff         result=0;
         G4ExceptionDescription desc;
         desc << "Warning: Bad energy non-conservation detected, will "
              << (epReportLevel<0 ? "abort the event" :	"re-sample the interaction") << G4endl
              << " Process / Model: " <<  GetProcessName()<< " / " << theModel->GetModelName() << G4endl
              << " Primary: " << aPro.GetDefinition()->GetParticleName()
              << " (" << aPro.GetDefinition()->GetPDGEncoding() << "),"
              << " E= " <<  aPro.Get4Momentum().e()
              << ", target nucleus (" << aNucleus.GetZ_asInt() << ","<< aNucleus.GetA_asInt() << ")" << G4endl
              << " E(initial - final) = " << deltaE << " MeV." << G4endl;
         G4Exception("G4SQInelasticProcess:CheckResult()", "had012", epReportLevel<0 ? EventMustBeAborted : JustWarning,desc);
      }
   }
   return result;
}

void
G4SQInelasticProcess::CheckEnergyMomentumConservation(const G4Track& aTrack,
                                                   const G4Nucleus& aNucleus)
{
  G4int target_A=aNucleus.GetA_asInt();
  G4int target_Z=aNucleus.GetZ_asInt();
  G4double targetMass = G4NucleiProperties::GetNuclearMass(target_A,target_Z);
  G4LorentzVector target4mom(0, 0, 0, targetMass);

  G4LorentzVector projectile4mom = aTrack.GetDynamicParticle()->Get4Momentum();
  G4int track_A = aTrack.GetDefinition()->GetBaryonNumber();
  G4int track_Z = G4lrint(aTrack.GetDefinition()->GetPDGCharge());

  G4int initial_A = target_A + track_A;
  G4int initial_Z = target_Z + track_Z;

  G4LorentzVector initial4mom = projectile4mom + target4mom;

  // Compute final-state momentum for scattering and "do nothing" results
  G4LorentzVector final4mom;
  G4int final_A(0), final_Z(0);

  G4int nSec = theTotalResult->GetNumberOfSecondaries();
  if (theTotalResult->GetTrackStatus() != fStopAndKill) {  // If it is Alive
     // Either interaction didn't complete, returned "do nothing" state
     //  or    the primary survived the interaction (e.g. electro-nucleus )
     G4Track temp(aTrack);

     // Use the final energy / momentum
     temp.SetMomentumDirection(*theTotalResult->GetMomentumDirection());
     temp.SetKineticEnergy(theTotalResult->GetEnergy());

     if( nSec == 0 ){
        // Interaction didn't complete, returned "do nothing" state
        //   - or suppressed recoil  (e.g. Neutron elastic )
        final4mom = temp.GetDynamicParticle()->Get4Momentum() + target4mom;
        final_A = initial_A;
        final_Z = initial_Z;
     }else{
        // The primary remains in final state (e.g. electro-nucleus )
        final4mom = temp.GetDynamicParticle()->Get4Momentum();
        final_A = track_A;
        final_Z = track_Z;
        // Expect that the target nucleus will have interacted,
        //  and its products, including recoil, will be included in secondaries.
     }
  }
  if( nSec > 0 ) {
    G4Track* sec;

    for (G4int i = 0; i < nSec; i++) {
      sec = theTotalResult->GetSecondary(i);
      final4mom += sec->GetDynamicParticle()->Get4Momentum();
      final_A += sec->GetDefinition()->GetBaryonNumber();
      final_Z += G4lrint(sec->GetDefinition()->GetPDGCharge());
    }
  }

  // Get level-checking information (used to cut-off relative checks)
  G4String processName = GetProcessName();
  G4HadronicInteraction* theModel = GetHadronicInteraction();
  G4String modelName("none");
  if (theModel) modelName = theModel->GetModelName();
  std::pair<G4double, G4double> checkLevels = epCheckLevels;
  if (!levelsSetByProcess) {
    if (theModel) checkLevels = theModel->GetEnergyMomentumCheckLevels();
    checkLevels.first= std::min(checkLevels.first,  epCheckLevels.first);
    checkLevels.second=std::min(checkLevels.second, epCheckLevels.second);
  }

  // Compute absolute total-energy difference, and relative kinetic-energy
  G4bool checkRelative = (aTrack.GetKineticEnergy() > checkLevels.second);

  G4LorentzVector diff = initial4mom - final4mom;
  G4double absolute = diff.e();
  G4double relative = checkRelative ? absolute/aTrack.GetKineticEnergy() : 0.;

  G4double absolute_mom = diff.vect().mag();
  G4double relative_mom = checkRelative ? absolute_mom/aTrack.GetMomentum().mag() : 0.;

  // Evaluate relative and absolute conservation
  G4bool relPass = true;
  G4String relResult = "pass";
  if (  std::abs(relative) > checkLevels.first
	 || std::abs(relative_mom) > checkLevels.first) {
    relPass = false;
    relResult = checkRelative ? "fail" : "N/A";
  }

  G4bool absPass = true;
  G4String absResult = "pass";
  if (   std::abs(absolute) > checkLevels.second
      || std::abs(absolute_mom) > checkLevels.second ) {
    absPass = false ;
    absResult = "fail";
  }

  G4bool chargePass = true;
  G4String chargeResult = "pass";
  if (   (initial_A-final_A)!=0
      || (initial_Z-final_Z)!=0 ) {
    chargePass = checkLevels.second < DBL_MAX ? false : true;
    chargeResult = "fail";
   }

  G4bool conservationPass = (relPass || absPass) && chargePass;

  std::stringstream Myout;
  G4bool Myout_notempty(false);
  // Options for level of reporting detail:
  //  0. off
  //  1. report only when E/p not conserved
  //  2. report regardless of E/p conservation
  //  3. report only when E/p not conserved, with model names, process names, and limits
  //  4. report regardless of E/p conservation, with model names, process names, and limits
  //  negative -1.., as above, but send output to stderr

  if(   std::abs(epReportLevel) == 4
	||	( std::abs(epReportLevel) == 3 && ! conservationPass ) ){
      Myout << " Process: " << processName << " , Model: " <<  modelName << G4endl;
      Myout << " Primary: " << aTrack.GetParticleDefinition()->GetParticleName()
            << " (" << aTrack.GetParticleDefinition()->GetPDGEncoding() << "),"
            << " E= " <<  aTrack.GetDynamicParticle()->Get4Momentum().e()
	    << ", target nucleus (" << aNucleus.GetZ_asInt() << ","
	    << aNucleus.GetA_asInt() << ")" << G4endl;
      Myout_notempty=true;
  }
  if (  std::abs(epReportLevel) == 4
	 || std::abs(epReportLevel) == 2
	 || ! conservationPass ){

      Myout << "   "<< relResult  <<" relative, limit " << checkLevels.first << ", values E/T(0) = "
             << relative << " p/p(0)= " << relative_mom  << G4endl;
      Myout << "   "<< absResult << " absolute, limit (MeV) " << checkLevels.second/MeV << ", values E / p (MeV) = "
             << absolute/MeV << " / " << absolute_mom/MeV << " 3mom: " << (diff.vect())*1./MeV <<  G4endl;
      Myout << "   "<< chargeResult << " charge/baryon number balance " << (initial_Z-final_Z) << " / " << (initial_A-final_A) << " "<<  G4endl;
      Myout_notempty=true;

  }
  Myout.flush();
  if ( Myout_notempty ) {
     if (epReportLevel > 0)      G4cout << Myout.str()<< G4endl;
     else if (epReportLevel < 0) G4cerr << Myout.str()<< G4endl;
  }
}


void G4SQInelasticProcess::DumpState(const G4Track& aTrack,
				  const G4String& method,
				  G4ExceptionDescription& ed)
{
  ed << "Unrecoverable error in the method " << method << " of "
     << GetProcessName() << G4endl;
  ed << "TrackID= "<< aTrack.GetTrackID() << "  ParentID= "
     << aTrack.GetParentID()
     << "  " << aTrack.GetParticleDefinition()->GetParticleName()
     << G4endl;
  ed << "Ekin(GeV)= " << aTrack.GetKineticEnergy()/CLHEP::GeV
     << ";  direction= " << aTrack.GetMomentumDirection() << G4endl;
  ed << "Position(mm)= " << aTrack.GetPosition()/CLHEP::mm << ";";

  if (aTrack.GetMaterial()) {
    ed << "  material " << aTrack.GetMaterial()->GetName();
  }
  ed << G4endl;

  if (aTrack.GetVolume()) {
    ed << "PhysicalVolume  <" << aTrack.GetVolume()->GetName()
       << ">" << G4endl;
  }
}
/* 
G4ParticleDefinition* G4SQInelasticProcess::GetTargetDefinition()
{
  const G4Nucleus* nuc = GetTargetNucleus();
  G4int Z = nuc->GetZ_asInt();
  G4int A = nuc->GetA_asInt();
  return G4ParticleTable::GetParticleTable()->GetIon(Z,A,0*eV);
}
*/
/* end of file */
