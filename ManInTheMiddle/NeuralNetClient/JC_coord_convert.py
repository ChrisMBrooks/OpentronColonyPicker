import numpy
    
colony_i = []
with open('processed/scores0.csv') as scores:
    for i, score in enumerate(scores):
        if float(score) > 0.5:
            colony_i.append(i)
        if float(score) < 0.5:
                break

all_boxes = []
colony_boxes = []
with open('processed/boxes0.csv') as boxes:
    for box in boxes:
        all_boxes.append(box.strip().split('\n'))
    for i  in colony_i: colony_boxes.append(all_boxes[i]) 

for i, box in enumerate(colony_boxes):
    for coords in box: colony_boxes[i] = coords.split(',')
for box in colony_boxes:
    for i, coords in enumerate(box): box[i] = float(coords)
    
# coordinates stored in the form y1, x1, y1, x2 
centre_points = []
for box in colony_boxes:
    # yx coordinate of centre point
    ymid = (box[0]+box[2])/2
    xmid = (box[1]+box[3])/2
    centre_point = [ymid, xmid]
    centre_points.append(centre_point)

print(centre_points)