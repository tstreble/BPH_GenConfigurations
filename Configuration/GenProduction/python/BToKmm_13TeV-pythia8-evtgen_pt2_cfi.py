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
            operates_on_particles = cms.vint32(),    
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyB+        B+
Alias      MyB-        B-
ChargeConj MyB-        MyB+
#
Decay MyB+
1.000  K+      mu+     mu-    PHOTOS BTOSLLBALL;
Enddecay
CDecay MyB-
#
End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
                                        'PTFilter:filter = on', # this turn on the filter
                                        'PTFilter:quarkToFilter = 5', # PDG id of q quark
                                        'PTFilter:scaleToFilter = 1.0'),
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
    NumberDaughters = cms.untracked.int32(3),
    ParticleID      = cms.untracked.int32(521),  ## Bu
    DaughterIDs     = cms.untracked.vint32(321, 13, -13), ## K+ mu- mu+
    MinPt           = cms.untracked.vdouble(2., 2., 2.),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5, -2.5),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5, 2.5)
)
    
mufilter = cms.EDFilter("MCMultiParticleFilter",
            src = cms.untracked.InputTag("generator", "unsmeared"),   
            Status = cms.vint32(1),
            ParticleID = cms.vint32(13),
            PtMin = cms.vdouble(0.),
            NumRequired = cms.int32(3),
            EtaMax = cms.vdouble(999.),
            AcceptMore = cms.bool(True)
            )

mufilterPt5 = cms.EDFilter("PythiaFilter",  # bachelor muon with kinematic cuts.
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(5.),
    ParticleID = cms.untracked.int32(13),
)

ProductionFilterSequence = cms.Sequence(generator*bufilter*decayfilter*mufilter*mufilterPt5)
#ProductionFilterSequence = cms.Sequence(generator*decayfilter*mufilter)
