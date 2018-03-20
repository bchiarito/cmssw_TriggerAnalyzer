import FWCore.ParameterSet.Config as cms

process = cms.Process("TrigAna")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

readFiles = cms.untracked.vstring()
process.source = cms.Source("PoolSource", fileNames = readFiles)
readFiles.extend( [
#'root://cms-xrd-global.cern.ch//store/data/Run2016B/Tau/MINIAOD/03Feb2017_ver2-v2/100000/0208F470-7DEE-E611-A8ED-0CC47A4D7646.root' # Run B
'root://cms-xrd-global.cern.ch//store/data/Run2016H/Tau/MINIAOD/03Feb2017_ver2-v1/100000/00A17AC6-8AEB-E611-9A86-A0369F83627E.root' # Run H
] );

process.demo = cms.EDAnalyzer("TriggerAnalyzer",
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects = cms.InputTag("selectedPatTrigger"),
)

process.p = cms.Path(process.demo)
