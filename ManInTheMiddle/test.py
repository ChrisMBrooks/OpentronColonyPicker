from NeuralNetClient import NeuralNetClient as nnc

nnc_client = nnc.NeuralNetClient(config = {})
#nnc_client.process_all_files()
#centre_point_locs = nnc_client.calculate_centre_points()
#print(centre_point_locs)

centre_point_locs = nnc_client.process_single_file(r'D:\Source\OpentronColonyPicker\ManInTheMiddle\NeuralNetClient\plate_image\WhatsApp Image 2022-12-08 at 17.45.54.jpeg')
print(centre_point_locs)