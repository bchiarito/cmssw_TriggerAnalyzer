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

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <string>
#include <iostream>
//
// class declaration
//

using std::string;
using std::vector;
using std::set;
using std::cout;
using std::endl;

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

      vector<trigger_listing> foundTriggers;
      bool trackLumis;
      string triggerString;

      string processName; // process name of (HLT) process for which to get HLT configuration
      HLTConfigProvider hltConfig;
};


//
// constructors and destructor
//
TriggerAnalyzer::TriggerAnalyzer(const edm::ParameterSet& iConfig)
:
   triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
   triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
   triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
   trackLumis(iConfig.getUntrackedParameter<bool>("trackLumis")),
   triggerString(iConfig.getUntrackedParameter<string>("triggerString"))
{
   processName = "*";
}


TriggerAnalyzer::~TriggerAnalyzer()
{
 
}

void
TriggerAnalyzer::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  bool changed(true);
  if (hltConfig.init(iRun,iSetup,processName,changed)) {
    if (changed) {
     // The HLT config has actually changed wrt the previous Run, hence rebook histos, etc
    }
  } else {
    cout << " HLT config extraction failure with process name " << processName << endl;
    // In this case, all access methods will return empty values!
  }
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

  const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
  for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i)
  {
    string triggerName = names.triggerName(i);
    int ps = triggerPrescales->getPrescaleForIndex(i);
    std::size_t found = triggerName.find(triggerString);
    if ( found==std::string::npos )
      continue;
    // check if trigger is already in list
    if( have_and_inc_trigger(triggerName, ps, iEvent.id().run(), iEvent.id().luminosityBlock()) )
      continue;
    // if not add to list
    add_trigger(triggerName, ps, iEvent.id().run(), iEvent.id().luminosityBlock());
  }
}

bool TriggerAnalyzer::have_and_inc_trigger(string iName, int iPrescale, int iRun, int iLumi)
{
  for(unsigned int i = 0; i < foundTriggers.size(); i++)
  {
    if( (foundTriggers[i].name == iName) &&
        (foundTriggers[i].prescale == iPrescale) &&
        (foundTriggers[i].run == iRun) ) {
      // increment event count
      foundTriggers[i].event_count++;
      // add to lumi list
      if(trackLumis)
        foundTriggers[i].lumis.insert(iLumi);
      return true;
    }
  }
  return false;
}

bool TriggerAnalyzer::have_trigger(string iName, int iPrescale, int iRun, int iLumi=0)
{
  for(unsigned int i = 0; i < foundTriggers.size(); i++)
  {
    if( (foundTriggers[i].name == iName) &&
        (foundTriggers[i].prescale == iPrescale) &&
        (foundTriggers[i].run == iRun) ) {
      return true;
    }
  }
  return false;
}


void TriggerAnalyzer::add_trigger(string iName, int iPrescale, int iRun, int iLumi)
{
  struct trigger_listing trig = { .name = iName, .prescale = iPrescale, .run = iRun, .event_count = 1 };
  if(trackLumis)
    trig.lumis.insert(iLumi);
  foundTriggers.push_back(trig);
}

void 
TriggerAnalyzer::beginJob()
{
}

void 
TriggerAnalyzer::endJob() 
{
  cout << "found trigger list" << endl;
  for(unsigned int i = 0; i < foundTriggers.size(); i++)
  {
    cout << "Name: " << foundTriggers[i].name;
    cout << " PS: " << foundTriggers[i].prescale;
    cout << " Run: " << foundTriggers[i].run;
    cout << " EventCount: " << foundTriggers[i].event_count;
    cout << " Lumis: ";
    for (set<int>::iterator it = foundTriggers[i].lumis.begin(); it != foundTriggers[i].lumis.end(); ++it)
      cout << *it << ',';
    cout << endl;

    using std::setw;
    cout << "modules:" << endl;
    vector<string> modules = hltConfig.moduleLabels(foundTriggers[i].name);
    for(vector<string>::iterator it = modules.begin(); it != modules.end(); ++it) {
      string name = *it;
      if (hltConfig.moduleEDMType(name) != "EDProducer") continue;
      cout << setw(80) << name << " : " << setw(40) << hltConfig.moduleType(name) << " : " << setw(15) << hltConfig.moduleEDMType(name) << endl;
      cout << (hltConfig.modulePSet(name)).dump() << endl;
    }

    for(vector<string>::iterator it = modules.begin(); it != modules.end(); ++it) {
      string name = *it;
      if (hltConfig.moduleEDMType(name) != "EDFilter") continue;
      cout << setw(80) << name << " : " << setw(40) << hltConfig.moduleType(name) << " : " << setw(15) << hltConfig.moduleEDMType(name) << endl;
      cout << (hltConfig.modulePSet(name)).dump() << endl;
    }

    for(vector<string>::iterator it = modules.begin(); it != modules.end(); ++it) {
      string name = *it;
      if (hltConfig.moduleEDMType(name) == "EDFilter") continue;
      if (hltConfig.moduleEDMType(name) == "EDProducer") continue;
      cout << setw(80) << name << " : " << setw(40) << hltConfig.moduleType(name) << " : " << setw(15) << hltConfig.moduleEDMType(name) << endl;
    }
  }

  cout << hltConfig.moduleType("hltL1fL1sMu18L1Filtered0") << endl;
}

void
TriggerAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  // triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
  // triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
  // triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
  // config parameters
  desc.addUntracked<bool>("trackLumis", false);
  desc.addUntracked<string>("triggerString", "HLT_");
  desc.add<edm::InputTag>("bits");
  desc.add<edm::InputTag>("objects");
  desc.add<edm::InputTag>("prescales");

  descriptions.add("TriggerAnalyzer", desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerAnalyzer);
