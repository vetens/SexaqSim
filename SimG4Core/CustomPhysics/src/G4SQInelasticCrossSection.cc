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
// By JPW, working, but to be cleaned up. @@@
// G.Folger, 29-sept-2006: extend to 1TeV, using a constant above 20GeV
// 22 Dec 2006 - DHW added isotope dependence
// G.Folger, 25-Nov-2009: extend to 100TeV, using a constant above 20GeV
// V.Ivanchenko, 18-Aug-2011: migration to new design and cleanup;
//                            make it applicable for Z>1
//

#include "G4SQInelasticCrossSection.hh"
#include "G4SystemOfUnits.hh"
#include "G4DynamicParticle.hh"
#include "G4SQ.hh"
#include "G4AntiSQ.hh"
#include "G4NistManager.hh"


G4SQInelasticCrossSection::G4SQInelasticCrossSection()
  : G4VCrossSectionDataSet("SQ-neutron")
{
  nist = G4NistManager::Instance();
  theSQ = G4SQ::SQ();
  theAntiSQ = G4AntiSQ::AntiSQ();
}


G4SQInelasticCrossSection::~G4SQInelasticCrossSection()
{}


G4bool G4SQInelasticCrossSection::IsElementApplicable(
                             const G4DynamicParticle* aPart, 
                             G4int Z, const G4Material*)
{
  return ((0 < Z) && 
          (aPart->GetDefinition() == theSQ || 
           aPart->GetDefinition() == theAntiSQ)
         );
}


G4double G4SQInelasticCrossSection::GetElementCrossSection(
                             const G4DynamicParticle* aPart, 
                             G4int Z, const G4Material*)
{
  // return zero fo particle instead of antiparticle
  // sexaquark interaction with matter expected really tiny
  if (aPart->GetDefinition() != theAntiSQ) return 0;

  // zero crosssection for particle at rest
  if(aPart->GetKineticEnergy() <= 0.0) { return 0.0; }
  //I don't want to interact on hydrogen
  if(Z <= 1){return 0.0;}

  // get the atomic weight (to estimate nr neutrons)
  G4double A = nist->GetAtomicMassAmu(Z);
  // increase the passed number of neutrons, so that we can mimic
  // a flat interaction probability as a function of neutron density
  // in the detector
  // it's a hack, but it's much more efficient than running millions
  // of events with a very low cross section
  //G4double coeff = 1e20;
  //const_cast<G4DynamicParticle*>(aPart)->SetMagneticMoment(aPart->GetMagneticMoment()+coeff*(A-Z));
  // now calculate the cross section

  //put the X section very low for the antiS to get a flat interaction rate, but also make it scale with the number of neutrons in the material, because we are going to interact on neutrons, not on protons
  G4double baseXS = (1.*(A-(G4double)Z)/(G4double)Z)*millibarn; //40. * millibarn;
  // the following scaled xsection makes that we get instead of an exponential
  // rather a flat interaction probability over an ensemble of particles
  // for all material (neutrons) in the detector
  G4double scaledXS = baseXS;// / (1 - baseXS * aPart->GetMagneticMoment());
//std::cout << "$$$ XSW scale " << scaledXS << " pt=" <<
//aPart->GetMomentum().perp()/GeV
//<< " eta=" << aPart->GetMomentum().eta() << std::endl;

  // now return the scaled cross section
  if (scaledXS < 0) {  // eventually this scaling violates unitarity
    return 1; // in which case we return a huge cross section
  } else {
    return scaledXS;
  }
}
