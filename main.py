import os

import cv2
import matplotlib.pyplot as plt


input_file = './example.txt'

mask = cv2.imread('./mask.png', -1)

imgs_dir = '/media/phillip/FELIPE/youtube/computer_vision/08_illegal_lane_crossing_detection/code/input_lane_crossing/imgs'


def get_region(bbox, mask):
    x, y, w, h = bbox

    xc = int(x + (w / 2))
    yc = int(y + (h / 2))

    if mask[yc, xc, 3] == 255:
        if mask[yc, xc, 0] == 255:
            return -1
        else:
            return 1
    else:
        return 0


with open(input_file, 'r') as f:
    lines = [l[:-1] for l in f.readlines() if len(l) > 2]
    f.close()

cars = {}
for line_, line in enumerate(lines):
    lines[line_] = [int(float(_)) for _ in line.split(',')]
    lines[line_].append(get_region(lines[line_][2:6], mask))

    if lines[line_][1] not in cars.keys():
        cars[lines[line_][1]] = {'frame_nmr': [], 'lane_id': [], 'line_nmr': []}

    cars[lines[line_][1]]['frame_nmr'].append(lines[line_][0])
    cars[lines[line_][1]]['line_nmr'].append(line_)
    cars[lines[line_][1]]['lane_id'].append(lines[line_][-1])

for car in cars.keys():
    if -1 in cars[car]['lane_id'] and 1 in cars[car]['lane_id']:
        indx_lane_left = cars[car]['lane_id'].index(-1)
        indx_lane_right = cars[car]['lane_id'].index(1)
        lane_crossing_index = max(indx_lane_left, indx_lane_right)
        frame_number_crossing = cars[car]['frame_nmr'][lane_crossing_index]
        line_number_crossing = cars[car]['line_nmr'][lane_crossing_index]

        bbox = lines[line_number_crossing][2:6]
        x, y, w, h = bbox

        img = cv2.imread(os.path.join(imgs_dir, '{}.jpg'.format(str(frame_number_crossing).zfill(6))))

        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        plt.figure()
        plt.title(str(frame_number_crossing))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

plt.show()