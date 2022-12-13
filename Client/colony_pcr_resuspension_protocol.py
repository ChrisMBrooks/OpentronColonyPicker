from opentrons import protocol_api
metadata = {'apiLevel': '2.13',
            'protocolName': 'Colony PCR - Resuspension and Mix',
            'description': '''What it says on the tin.''',
            'author': 'SSB MRes - Gin and Tronic Tron'}

def transfer_colony_suspension(p300, sourceplate, destplate, sources:list, destinations:list):
    #Adding colony suspension to the PCR mix
    for i, source in enumerate(sources):
        p300.transfer(20, sourceplate.wells_by_name()[sources[i]], 
                      destplate.wells_by_name()[destinations[i]], new_tip = 'always')

def transfer_lb_to_suspension(p300, sourceplate, destplate, destinations:list):
    #Adding LB from the reservoir to the remaining colony suspension
    for destination in destinations: 
        p300.transfer(180, sourceplate.wells_by_name()['A1'], 
                      destplate.wells_by_name()[destination], new_tip = 'always', mix='always')

def run(protocol: protocol_api.ProtocolContext):
    
    #Define Labware
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    petriplate = protocol.load_labware('nest_96_wellplate_200ul_flat', 4)
    destplate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 5)
    lbplate = protocol.load_labware('nest_96_wellplate_2ml_deep', 2)
    lbres = protocol.load_labware('nest_12_reservoir_15ml',3)
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tips])
    
    
    # Perform Colony picking and adding to the Deep well plates A2,B2 and C2
    
    # Execute Remaining Sub Processes - Reagents Prep
    transfer_colony_suspension(p300, lbplate, destplate, ['A1', 'B1', 'C1'], ['A1', 'B1', 'C1'])
    
    transfer_lb_to_suspension(p300, lbres, lbplate, ['A1', 'B1', 'C1'])