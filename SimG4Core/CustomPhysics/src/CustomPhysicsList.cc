#include "SimG4Core/CustomPhysics/interface/CustomPhysicsList.h"
#include "SimG4Core/CustomPhysics/interface/CustomParticleFactory.h"
#include "SimG4Core/CustomPhysics/interface/CustomParticle.h"
#include "SimG4Core/CustomPhysics/interface/DummyChargeFlipProcess.h"
#include "SimG4Core/CustomPhysics/interface/G4ProcessHelper.h"
#include "SimG4Core/CustomPhysics/interface/CustomPDGParser.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "G4Decay.hh"
#include "G4hMultipleScattering.hh"
#include "G4hIonisation.hh"
#include "G4ProcessManager.hh"

#include "G4LeptonConstructor.hh"
#include "G4MesonConstructor.hh"
#include "G4BaryonConstructor.hh"
#include "G4ShortLivedConstructor.hh"
#include "G4IonConstructor.hh"

#include "SimG4Core/CustomPhysics/interface/FullModelHadronicProcess.h"

#include "SimG4Core/CustomPhysics/src/G4SQInelasticProcess.hh"
#include "SimG4Core/CustomPhysics/src/G4SQLoopProcess.hh"
#include "SimG4Core/CustomPhysics/src/G4SQLoopProcessDiscr.hh"
#include "SimG4Core/CustomPhysics/src/G4SQNeutronAnnih.hh"
#include "SimG4Core/CustomPhysics/src/G4SQInelasticCrossSection.hh"

using namespace CLHEP;
 
G4ThreadLocal std::unique_ptr<G4ProcessHelper> CustomPhysicsList::myHelper;

CustomPhysicsList::CustomPhysicsList(const std::string& name,
                                     const edm::ParameterSet & p, bool apinew)  
  :  G4VPhysicsConstructor(name) 
{  
  myConfig = p;
  edm::FileInPath fp = p.getParameter<edm::FileInPath>("particlesDef");
  particleDefFilePath = fp.fullPath();
//  std::cout << particleDefFilePath << "- File accessed! Custom physics constructed successfully!" << std::endl;
  fParticleFactory.reset(new CustomParticleFactory());
  myHelper.reset(nullptr);

  edm::LogInfo("SimG4CoreCustomPhysics")
    << "CustomPhysicsList: Path for custom particle definition file: \n"
    <<particleDefFilePath << "\n";
}

CustomPhysicsList::~CustomPhysicsList() {
}
 
void CustomPhysicsList::ConstructParticle(){
  edm::LogInfo("SimG4CoreCustomPhysics")
  << "===== CustomPhysicsList::ConstructParticle ";
  fParticleFactory.get()->loadCustomParticles(particleDefFilePath);     
}
 
void CustomPhysicsList::ConstructProcess() {
  edm::LogInfo("SIMG4CoreCustomPhysics") << " CustomPhysicsList: adding CustomPhysics processes "
				<< "for the list of particles: \n";
//std::cout << "Beginning custom particle construction process" << std::endl;

  for (auto particle : fParticleFactory.get()->GetCustomParticles()) {
    CustomParticle* cp = dynamic_cast<CustomParticle*>(particle);
//    std::cout << "particle constructed: " << cp << std::endl;
    if(cp) {
      G4ProcessManager* pmanager = particle->GetProcessManager();
      edm::LogInfo("SimG4CoreCustomPhysics")
      <<"CustomPhysicsList: " << particle->GetParticleName()
      <<" PDGcode= " << particle->GetPDGEncoding()
      << " Mass= " << particle->GetPDGMass()/GeV <<" GeV.";
        
//Sexaquark implementation
    if (particle->GetParticleName() == "anti_sexaq") {

std::cout << "=-= SL sexaq FTW! =-= " 
          << particle->GetParticleType() << " "
          << particle->GetParticleName() << std::endl;

      if(pmanager) { //this is an important bit for the Sexaquark. Here the different interactions get defined
        G4SQInelasticProcess * sqInelPr = new G4SQInelasticProcess(particle->GetPDGMass()/GeV);
	G4SQNeutronAnnih * sqModel = new G4SQNeutronAnnih(particle->GetPDGMass()/GeV);
	sqInelPr->RegisterMe(sqModel);
	G4SQInelasticCrossSection * sqInelXS = new G4SQInelasticCrossSection(particle->GetPDGMass()/GeV);
	sqInelPr->AddDataSet(sqInelXS);
        pmanager->AddDiscreteProcess(sqInelPr);

	G4SQLoopProcess * sqLoopPr = new G4SQLoopProcess();
	pmanager->AddContinuousProcess(sqLoopPr);
	G4SQLoopProcessDiscr * sqLoopPrDiscr = new G4SQLoopProcessDiscr(particle->GetPDGMass()/GeV);
	pmanager->AddDiscreteProcess(sqLoopPrDiscr);
      }
      else  {edm::LogInfo("CustomPhysics") << "   No pmanager";}

    }
     else if (particle->GetParticleName() == "sexaq"){
	edm::LogInfo("CustomPhysics") << "   No pmanager implemented for sexaq, only for anti_sexaq";
     } 
     else {

std::cout << "=-= SL =-= " 
          << particle->GetParticleType() << " "
          << particle->GetParticleName() << std::endl;
     }
    }
   }
}
