import FWCore.ParameterSet.Config as cms

process = cms.Process("TrigAna")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

readFiles = cms.untracked.vstring()
process.source = cms.Source("PoolSource", fileNames = readFiles)
readFiles.extend( [
    #'root://cms-xrd-global.cern.ch//store/data/Run2016B/Tau/MINIAOD/03Feb2017_ver2-v2/100000/0208F470-7DEE-E611-A8ED-0CC47A4D7646.root' # Run B
    #'root://cms-xrd-global.cern.ch//store/data/Run2016H/Tau/MINIAOD/03Feb2017_ver2-v1/100000/00A17AC6-8AEB-E611-9A86-A0369F83627E.root' # Run H
    #'file:/cms/chiarito/eos/taustudy/miniaod/recopreselection/bkg_mc/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TauPreSelection/180504_184013/0000/MINIAOD_1.root'
    'root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/70000/00287FF4-0E40-E611-8D06-00266CFE78EC.root' # TT
] );

process.demo = cms.EDAnalyzer("TriggerAnalyzer",
    # MiniAOD trigger collections
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects = cms.InputTag("selectedPatTrigger"),
    # configuration
    triggerString = cms.untracked.string("HLT_IsoMu20"),
    trackLumis = cms.untracked.bool(False),
)

process.p = cms.Path(process.demo)
