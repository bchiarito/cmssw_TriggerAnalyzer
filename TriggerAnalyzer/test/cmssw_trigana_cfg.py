import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register("searchString", 'HLT_', VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("input", 'file:./my_file.root', VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("trackLumis", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "")
options.register("analyzeObjects", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "")
options.register("analyzeModules", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "")
options.setDefault('maxEvents', 100)
options.parseArguments()

process = cms.Process("TrigAna")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = int(options.maxEvents / 10.0)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

readFiles = cms.untracked.vstring()
process.source = cms.Source("PoolSource", fileNames = readFiles)
readFiles.extend( [
    options.input
] );

process.ana = cms.EDAnalyzer("TriggerAnalyzer",
    # MiniAOD trigger collections
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects = cms.InputTag("selectedPatTrigger"),
    # configuration
    triggerString = cms.untracked.string(options.searchString),
    trackLumis = cms.untracked.bool(options.trackLumis),
    analyzeObjects = cms.untracked.bool(options.analyzeObjects),
    analyzeModules = cms.untracked.bool(options.analyzeModules),
)

process.p = cms.Path(process.ana)
