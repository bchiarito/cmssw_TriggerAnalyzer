// -*- C++ -*-
//
// Package:    TrigAna/TriggerAnalyzer
// Class:      TriggerAnalyzer
// 
/**\class TriggerAnalyzer TriggerAnalyzer.cc TrigAna/TriggerAnalyzer/plugins/TriggerAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Brandon Chiarito
//         Created:  Sat, 20 May 2017 19:16:01 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

#include <string>
#include <iostream>
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

using std::string;
using std::vector;
using std::set;

struct trigger_listing {
  string name;
  int prescale;
  int run;
  int event_count;
  set<int> lumis;
};

class TriggerAnalyzer : public edm::EDAnalyzer  {
   public:
      explicit TriggerAnalyzer(const edm::ParameterSet&);
      ~TriggerAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      void beginRun(const edm::Run&, const edm::EventSetup&);
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      bool have_and_inc_trigger(string, int, int, int);
      bool have_trigger(string, int, int, int);
      void add_trigger(string, int, int, int);

      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
      edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;

      vector<trigger_listing> found_triggers_;
};


//
// constructors and destructor
//
TriggerAnalyzer::TriggerAnalyzer(const edm::ParameterSet& iConfig)
:
   triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
   triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
   triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales")))
{
}


TriggerAnalyzer::~TriggerAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

void
TriggerAnalyzer::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  std::cerr << "entering beginRun()" << std::endl;
}

void
TriggerAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<edm::TriggerResults> triggerBits;
   edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
   edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;
   iEvent.getByToken(triggerBits_, triggerBits);
   iEvent.getByToken(triggerObjects_, triggerObjects);
   iEvent.getByToken(triggerPrescales_, triggerPrescales);

   string str_to_find = "HLT_Photon";
   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
   for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i)
   {
     string triggerName = names.triggerName(i);
     int ps = triggerPrescales->getPrescaleForIndex(i);
     std::size_t found = triggerName.find(str_to_find);
     if ( found==std::string::npos )
       continue;
     //check if trigger is already in list
     if( have_and_inc_trigger(triggerName, ps, iEvent.id().run(), iEvent.id().luminosityBlock()) )
       continue;
     //if not add to list
     add_trigger(triggerName, ps, iEvent.id().run(), iEvent.id().luminosityBlock());
   }
}

bool TriggerAnalyzer::have_and_inc_trigger(string iName, int iPrescale, int iRun, int iLumi)
{
  for(unsigned int i = 0; i < found_triggers_.size(); i++)
  {
    if( (found_triggers_[i].name == iName) &&
        (found_triggers_[i].prescale == iPrescale) &&
        (found_triggers_[i].run == iRun) ) {
      // increment event count
      found_triggers_[i].event_count++;
      // add to lumi list
      found_triggers_[i].lumis.insert(iLumi);
      return true;
    }
  }
  return false;
}

bool TriggerAnalyzer::have_trigger(string iName, int iPrescale, int iRun, int iLumi=0)
{
  for(unsigned int i = 0; i < found_triggers_.size(); i++)
  {
    if( (found_triggers_[i].name == iName) &&
        (found_triggers_[i].prescale == iPrescale) &&
        (found_triggers_[i].run == iRun) ) {
      return true;
    }
  }
  return false;
}


void TriggerAnalyzer::add_trigger(string iName, int iPrescale, int iRun, int iLumi)
{
  struct trigger_listing trig = { .name = iName, .prescale = iPrescale, .run = iRun, .event_count = 0 };
  trig.lumis.insert(iLumi);
  found_triggers_.push_back(trig);
}

// ------------ method called once each job just before starting event loop  ------------
void 
TriggerAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TriggerAnalyzer::endJob() 
{
  std::cerr << "entering endJob()" << std::endl;

  for(unsigned int i = 0; i < found_triggers_.size(); i++)
  {
    std::cout << "Name: " << found_triggers_[i].name;
    std::cout << " PS: " << found_triggers_[i].prescale;
    std::cout << " Run: " << found_triggers_[i].run;
    std::cout << " EventCount: " << found_triggers_[i].event_count;
    std::cout << " Lumis: ";
    for (set<int>::iterator it = found_triggers_[i].lumis.begin(); it != found_triggers_[i].lumis.end(); ++it)
      std::cout << ',' << *it;
    std::cout << std::endl;
  }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TriggerAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerAnalyzer);
