from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = False
config.General.transferLogs = True
config.General.workArea = 'photondata2016full_crab3jobs'
#config.General.requestName = ''
config.section_('JobType')
config.JobType.psetName = '../python/ConfFile_cfg.py'
config.JobType.pyCfgParams = []
config.JobType.pluginName = 'Analysis'
#config.JobType.inputFiles = ['PileupDataAug10thHistogram.root', 'PileUpMC.root', 'Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt']
#config.JobType.outputFiles = ['ExoDiPhotonAnalyzer.root']
config.section_('Data')
#config.Data.inputDataset = ''
config.Data.outputDatasetTag = ''
config.Data.outLFNDirBase = '/store/user/bchiari1/noreplica/'
config.Data.publication = False
config.Data.unitsPerJob = 1000000
config.Data.totalUnits = -1
config.Data.splitting = 'EventAwareLumiBased'
config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'


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

    config.General.requestName = 'SinglePhoton_2016_RunH2'
    config.Data.inputDataset = '/SinglePhoton/Run2016H-03Feb2017_ver2-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunH3'
    config.Data.inputDataset = '/SinglePhoton/Run2016H-03Feb2017_ver3-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunG'
    config.Data.inputDataset = '/SinglePhoton/Run2016G-03Feb2017-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunF'
    config.Data.inputDataset = '/SinglePhoton/Run2016F-18Apr2017-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunE'
    config.Data.inputDataset = '/SinglePhoton/Run2016E-03Feb2017-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunD'
    config.Data.inputDataset = '/SinglePhoton/Run2016D-03Feb2017-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunC'
    config.Data.inputDataset = '/SinglePhoton/Run2016C-03Feb2017-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunB1'
    config.Data.inputDataset = '/SinglePhoton/Run2016B-18Apr2017_ver1-v1/MINIAOD'
    submit(config)

    config.General.requestName = 'SinglePhoton_2016_RunB2'
    config.Data.inputDataset = '/SinglePhoton/Run2016B-03Feb2017_ver2-v2/MINIAOD'
    submit(config)
