from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.workArea = 'crab_multi_IsoMu_DATA'
config.section_('JobType')
config.JobType.psetName = 'cmssw_trigana_cfg.py'
config.JobType.pyCfgParams = ['searchString=HLT_IsoMu']
config.JobType.pluginName = 'Analysis'
config.section_('Data')
config.Data.outLFNDirBase = '/store/user/bchiari1/cms_area/tau/trigana/IsoMu_DATA/'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = -1
config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_MuonPhys.txt'
config.Data.publication = False
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T3_US_Rutgers'


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    config.General.requestName = 'SingleMuon_Run2016B_ver1'
    config.Data.outputDatasetTag = 'RunB_TauPreSelection_ver1'
    config.Data.inputDataset = '/SingleMuon/Run2016B-07Aug17_ver1-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016B_ver2'
    config.Data.outputDatasetTag = 'RunB_TauPreSelection_ver2'
    config.Data.inputDataset = '/SingleMuon/Run2016B-07Aug17_ver2-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016C'
    config.Data.outputDatasetTag = 'RunC_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016C-07Aug17-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016D'
    config.Data.outputDatasetTag = 'RunD_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016D-07Aug17-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016E'
    config.Data.outputDatasetTag = 'RunE_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016E-07Aug17-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016F'
    config.Data.outputDatasetTag = 'RunF_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016F-07Aug17-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016G'
    config.Data.outputDatasetTag = 'RunG_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016G-07Aug17-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SingleMuon_Run2016H'
    config.Data.outputDatasetTag = 'RunH_TauPreSelection'
    config.Data.inputDataset = '/SingleMuon/Run2016H-07Aug17-v1/MINIAOD'
    submit(config)
