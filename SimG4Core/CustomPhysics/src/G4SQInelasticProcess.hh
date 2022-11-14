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
//
// $Id: G4SQInelasticProcess.hh 67989 2013-03-13 10:54:03Z gcosmo $
//
// -------------------------------------------------------------------
//
// GEANT4 Class header file
//
// G4SQInelasticProcess
//
// This is the top level Hadronic Process class
// The inelastic, elastic, capture, and fission processes
// should derive from this class
//
// original by S.Lowette 2018-11-16


#ifndef G4SQInelasticProcess_h
#define G4SQInelasticProcess_h 1
 

#include "G4HadronicProcess.hh"
#include "G4SystemOfUnits.hh"


class G4ParticleDefinition;


class G4SQInelasticProcess : public G4HadronicProcess
{

 public:

  G4SQInelasticProcess(const G4String& processName="SQInelastic");

  virtual ~G4SQInelasticProcess();

  virtual G4bool IsApplicable(const G4ParticleDefinition& aParticleType);

  // register generator of secondaries
  void RegisterMe(G4HadronicInteraction* a);

  // get cross section per element
  inline
  G4double GetElementCrossSection(const G4DynamicParticle * part, 
				  const G4Element * elm, 
				  const G4Material* mat = 0)
  {
    G4double x = theCrossSectionDataStore->GetCrossSection(part, elm, mat);
    if(x < 0.0) { x = 0.0; }
    return x;
  }

  // obsolete method to get cross section per element
  inline
  G4double GetMicroscopicCrossSection(const G4DynamicParticle * part, 
				      const G4Element * elm, 
				      const G4Material* mat = 0)
  { return GetElementCrossSection(part, elm, mat); }

  // generic PostStepDoIt recommended for all derived classes
  virtual G4VParticleChange* PostStepDoIt(const G4Track& aTrack, 
					  const G4Step& aStep);

  // initialisation of physics tables and G4SQInelasticProcessStore
  virtual void PreparePhysicsTable(const G4ParticleDefinition&);

  // build physics tables and print out the configuration of the process
  virtual void BuildPhysicsTable(const G4ParticleDefinition&);

  // dump physics tables 
  inline void DumpPhysicsTable(const G4ParticleDefinition& p)
  { theCrossSectionDataStore->DumpPhysicsTable(p); }

  // add cross section data set
  inline void AddDataSet(G4VCrossSectionDataSet * aDataSet)
  { theCrossSectionDataStore->AddDataSet(aDataSet);}

  // access to the manager
  inline G4EnergyRangeManager *GetManagerPointer()
  { return &theEnergyRangeManager; }
          
  // get inverse cross section per volume
  G4double GetMeanFreePath(const G4Track &aTrack, G4double, 
			   G4ForceCondition *);

  // access to the target nucleus
  inline const G4Nucleus* GetTargetNucleus() const
  { return &targetNucleus; }
  
  //  G4ParticleDefinition* GetTargetDefinition();
  inline const G4Isotope* GetTargetIsotope()
  { return targetNucleus.GetIsotope(); }
  
  virtual void ProcessDescription(std::ostream& outFile) const;
 
protected:    

  // generic method to choose secondary generator 
  // recommended for all derived classes
  inline G4HadronicInteraction* ChooseHadronicInteraction(
      G4double kineticEnergy, G4Material* aMaterial, G4Element* anElement)
  { return theEnergyRangeManager.GetHadronicInteraction(kineticEnergy,
							aMaterial,anElement);
  }

  // access to the target nucleus
  inline G4Nucleus* GetTargetNucleusPointer() 
  { return &targetNucleus; }
  
public:

  void BiasCrossSectionByFactor(G4double aScale);

  // Energy-momentum non-conservation limits and reporting
  inline void SetEpReportLevel(G4int level)
  { epReportLevel = level; }

  inline void SetEnergyMomentumCheckLevels(G4double relativeLevel, G4double absoluteLevel)
  { epCheckLevels.first = relativeLevel;
    epCheckLevels.second = absoluteLevel;
    levelsSetByProcess = true;
  }

  inline std::pair<G4double, G4double> GetEnergyMomentumCheckLevels() const
  { return epCheckLevels; }

  // access to the cross section data store
  inline G4CrossSectionDataStore* GetCrossSectionDataStore()
    {return theCrossSectionDataStore;}

  inline void MultiplyCrossSectionBy(G4double factor)
  { aScaleFactor = factor; }

protected:

  void DumpState(const G4Track&, const G4String&, G4ExceptionDescription&);
            
  // obsolete method will be removed
  inline const G4EnergyRangeManager &GetEnergyRangeManager() const
  { return theEnergyRangeManager; }
    
  // obsolete method will be removed
  inline void SetEnergyRangeManager( const G4EnergyRangeManager &value )
  { theEnergyRangeManager = value; }

  // access to the chosen generator
  inline G4HadronicInteraction* GetHadronicInteraction() const
  { return theInteraction; }
    
  // access to the cross section data set
  inline G4double GetLastCrossSection() 
  { return theLastCrossSection; }

  // fill result
  void FillResult(G4HadFinalState* aR, const G4Track& aT);

  // Check the result for catastrophic energy non-conservation
  G4HadFinalState* CheckResult(const G4HadProjectile& thePro,
			       const G4Nucleus& targetNucleus, 
			       G4HadFinalState* result) const;

  // Check 4-momentum balance
  void CheckEnergyMomentumConservation(const G4Track&, const G4Nucleus&);

private:
  G4double XBiasSurvivalProbability();
  G4double XBiasSecondaryWeight();

  // hide assignment operator as private 
  G4SQInelasticProcess& operator=(const G4SQInelasticProcess& right);
  G4SQInelasticProcess(const G4SQInelasticProcess&);

  // Set E/p conservation check levels from environment variables
  void GetEnergyMomentumCheckEnvvars();

protected:

  G4HadProjectile thePro;

  G4ParticleChange* theTotalResult; 

  G4int epReportLevel;

private:
    
  G4ParticleDefinition* theParticle;

  G4EnergyRangeManager theEnergyRangeManager;
    
  G4HadronicInteraction* theInteraction;

  G4CrossSectionDataStore* theCrossSectionDataStore;
     
  G4Nucleus targetNucleus;

  bool G4SQInelasticProcess_debug_flag;

  // Energy-momentum checking
  std::pair<G4double, G4double> epCheckLevels;
  G4bool levelsSetByProcess;

  std::vector<G4VLeadingParticleBiasing *> theBias;
  
  G4double theInitialNumberOfInteractionLength;   

  G4double aScaleFactor;
  G4bool   xBiasOn;
  G4double theLastCrossSection;

};
 
#endif
 
