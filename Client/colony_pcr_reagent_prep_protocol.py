from opentrons import protocol_api
metadata = {'apiLevel': '2.13',
            'protocolName': 'Colony PCR - Regent Prep',
            'description': '''What it says on the tin.''',
            'author': 'SSB MRes - Gin and Tronic Tron'}
# Part 1 - Reagents 

def transfer_reagents_to_temp_block(p300, sourceplate, destplate, reagents:list):
    #Mixing of the PCR mix reagents to one destination on the same plate
    for reagent in reagents: 
        p300.transfer(100, sourceplate.wells_by_name()[reagent], 
                      destplate.wells_by_name()['A8'], new_tip = 'always') 

def transfer_reagents_from_temp_block(p300, sourceplate, destplate, destinations:list):
    #Distribution of PCR mix from plate on temperature module to destination pcr plate
    p300.pick_up_tip()
    for destination in destinations: 
        p300.transfer(30, sourceplate.wells_by_name()['A8'], 
                      destplate.wells_by_name()[destination], new_tip = 'never')
    p300.drop_tip()
    
def transfer_water_to_deep_well_plate(p300, sourceplate, destplate, destinations:list):
    #Adding nuclease free water from temperature module plate to Deepwell plate
    p300.pick_up_tip() 
    for destination in destinations: 
        p300.transfer(40, sourceplate.wells_by_name()['D1'], 
                      destplate.wells_by_name()[destination], new_tip = 'never')
    p300.drop_tip()

def run(protocol: protocol_api.ProtocolContext):
    
    #Define Labware
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    petriplate = protocol.load_labware('nest_96_wellplate_200ul_flat', 4)
    destplate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 5)
    lbplate = protocol.load_labware('nest_96_wellplate_2ml_deep', 2)
    lbres = protocol.load_labware('nest_12_reservoir_15ml',3)
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tips])
    
    #Add the temperature module
    temp_mod = protocol.load_module('temperature module', 7)
    sourceplate = temp_mod.load_labware('nest_96_wellplate_200ul_flat')
    
    #Set the temperature module
    temp_mod.set_temperature(4)
    
    # Execute Remaining Sub Processes - Reagents Prep
    transfer_reagents_to_temp_block(p300, sourceplate, sourceplate, ['A1', 'B1', 'C1'])
    
    transfer_reagents_from_temp_block(p300, sourceplate, destplate, ['A1', 'B1', 'C1', 'D1'])
    
    transfer_water_to_deep_well_plate(p300, sourceplate, lbplate, ['A1', 'B1', 'C1'])
    
    #Transfer the Negative Control
    p300.transfer(20, sourceplate.wells_by_name()['D1'], 
                  destplate.wells_by_name()['D1'], new_tip = 'always') #Negative control
    