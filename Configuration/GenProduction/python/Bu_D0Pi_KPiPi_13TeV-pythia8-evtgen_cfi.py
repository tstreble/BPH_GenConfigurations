import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyB+','MyB-'),        
            operates_on_particles = cms.vint32(521),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bu_D0Pi_KPiPi.dec')
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('SoftQCD:nonDiffractive = on'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

###### Filters ##########
bufilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(521) ## Bu
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(521),  ## Bu
    DaughterIDs     = cms.untracked.vint32(-421, 211), ## D0 pi
    MinPt           = cms.untracked.vdouble(-1., -1.),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999.,  9999.)
)



d0filter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-321, 211), # K- pi+
    MaxEta = cms.untracked.vdouble(9999.0, 9999.0),
    MinEta = cms.untracked.vdouble(-9999.0, -9999.0),
    MinPt = cms.untracked.vdouble(-1.,-1.),
    MotherID = cms.untracked.int32(521), #Bu
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(421), # D0
    verbose = cms.untracked.int32(1)
)


mufilter = cms.EDFilter("PythiaFilter",  # bachelor muon with kinematic cuts.
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(5.),
    ParticleID = cms.untracked.int32(13),
)

ProductionFilterSequence = cms.Sequence(generator*bufilter*decayfilter*d0filter*mufilter)
