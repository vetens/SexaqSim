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
//
// $Id$
//
//
// G4 Model: Charge and strangness exchange based on G4LightMedia model
//           28 May 2006 V.Ivanchenko
//
// Modified:
// 25-Jul-06 V.Ivanchenko add 19 MeV low energy, below which S-wave is sampled
//
//

#ifndef G4SQNeutronAnnih_h
#define G4SQNeutronAnnih_h 1

// Class Description
// Final state production model for hadron nuclear coherent charge exchange;
// Class Description - End

#include "globals.hh"
#include "G4HadronicInteraction.hh"
#include "G4HadProjectile.hh"
#include "G4Nucleus.hh"
#include "G4IonTable.hh"

class G4ParticleDefinition;


class G4SQNeutronAnnih : public G4HadronicInteraction {

  public:

    G4SQNeutronAnnih();

    virtual ~G4SQNeutronAnnih();

    G4double momDistr(G4double x_in);

    virtual G4HadFinalState * ApplyYourself(
                   const G4HadProjectile & aTrack,
                   G4Nucleus & targetNucleus);

  private:

    G4ParticleDefinition* theSQ;
    G4ParticleDefinition* theK0S;
    G4ParticleDefinition* theAntiL;
    G4ParticleDefinition* theProton;

};

#endif
