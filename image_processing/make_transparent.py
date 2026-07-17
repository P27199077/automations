from PIL import Image
import os
img_path = 'withered_plant.png'
dest_path = 'withered_transparent.png'

if os.path.exists(img_path):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Check if pixel is very close to white (RGB > 245)
        if item[0] > 245 and item[1] > 245 and item[2] > 245:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(dest_path, "PNG")
    print("SUCCESS: transparent withered.png created.")
else:
    print("ERROR: Source image not found.")
