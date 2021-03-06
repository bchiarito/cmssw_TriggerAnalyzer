import FWCore.ParameterSet.Config as cms

process = cms.Process("TrigAna")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

readFiles = cms.untracked.vstring()
process.source = cms.Source("PoolSource", fileNames = readFiles)
readFiles.extend( [
'/store/data/Run2016D/SinglePhoton/MINIAOD/PromptReco-v2/000/276/315/00000/04274087-F944-E611-9018-02163E01457A.root',
'/store/data/Run2016D/SinglePhoton/MINIAOD/PromptReco-v2/000/276/811/00000/ECAD8525-A94C-E611-AB12-02163E01389A.root' ] );

process.demo = cms.EDAnalyzer("TriggerAnalyzer",
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects = cms.InputTag("selectedPatTrigger"),
)

process.p = cms.Path(process.demo)
