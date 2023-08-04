import json
from pathlib import Path

BONE_NAMES = {'HEAD': 'Head', 'BODY': 'Body', 'ARM0': 'RightArm', 'ARM1': 'LeftArm', 'LEG0': 'RightLeg', 'LEG1': 'LeftLeg'}
BONE_KEYS = list(BONE_NAMES.keys())
TEXTURE_WIDTH = 64
TEXTURE_HEIGHT = 64
VISIBLE_BOUNDS_WIDTH = 2
VISIBLE_BOUNDS_HEIGHT = 4
VISIBLE_BOUNDS_OFFSET = [0, 1, 0]

try:
    csm_path = Path(input("Path to CSM File: "))
    with csm_path.open("r") as f:
        input_str = f.read()
except FileNotFoundError:
    print(f"{csm_path} does not exist.")
    exit()

geometry = [{
    'description': {
        'identifier': 'geometry.unknown',
        'texture_width': TEXTURE_WIDTH,
        'texture_height': TEXTURE_HEIGHT,
        'visible_bounds_width': VISIBLE_BOUNDS_WIDTH,
        'visible_bounds_height': VISIBLE_BOUNDS_HEIGHT,
        'visible_bounds_offset': VISIBLE_BOUNDS_OFFSET
    },
    'bones': []
}]

lines = input_str.strip().split('\n')

i = 0
while i < len(lines):
    if not lines[i].isdigit() or lines[i] in BONE_KEYS:
        entry = lines[i+1:i+11]  # parse next 10 lines as entry
        bone_name = BONE_NAMES.get(entry[0], entry[0])
        bone = next((b for b in geometry[0]['bones'] if b['name'] == bone_name), None)
        if bone is None:
            bone = {'name': bone_name, 'pivot': [0, 24, 0], 'cubes': []}
            geometry[0]['bones'].append(bone)
        try:
            cube = {
                'origin': list(map(float, entry[2:5])),
                'size': list(map(float, entry[5:8])),
                'uv': list(map(float, entry[8:]))
            }
        except ValueError:
            print("\nInvalid CSM Format. Example of valid CSM format below ⬇\n")
            print(
                  'PckStudio.generateModel+ModelPart\n'
                  'BODY\n'
                  'PckStudio.generateModel+ModelPart\n'
                  '-2\n'
                  '-3\n'
                  '2\n'
                  '1\n'
                  '1\n'
                  '1\n'
                  '0\n'
                  '0\n'
                       )
            print("Make sure your CSM follows the correct format, and that there are no strings mixed in with the numbers.")  # Display the line number where the error occurred
            exit()
        bone['cubes'].append(cube)
        i += len(entry)
    else:
        i += 1

output = {
    'format_version': '1.12.0',
    'minecraft:geometry': geometry
}

try:
    with open('model.geo.json', 'w') as f:
        json.dump(output, f, indent=4)
except OSError:
    print("Could not save JSON file.")
    exit()

print("JSON Saved to 'model.geo.json'")
