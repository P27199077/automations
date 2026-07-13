from PIL import Image
import os

folder = '/Users/tanishagupta/Desktop/projects/pomodoro'
files = [f'stage{i}.png' for i in range(1, 7)] + ['withered.png']

for file in files:
    path = os.path.join(folder, file)
    if not os.path.exists(path):
        print(f"Skipping {file}: not found")
        continue
    
    print(f"Processing {file}...")
    img = Image.open(path).convert("RGBA")
    data = img.getdata()
    
    # Get top-left corner pixel as background color reference
    bg_color = data[0]
    bg_r, bg_g, bg_b = bg_color[0], bg_color[1], bg_color[2]
    
    newData = []
    removed_count = 0
    for item in data:
        r, g, b, a = item
        # Calculate distance in RGB space
        dist = ((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)**0.5
        
        # If color is close to background color, make it transparent
        if dist < 25: 
            newData.append((bg_r, bg_g, bg_b, 0))
            removed_count += 1
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(path, "PNG")
    print(f"Finished {file}: removed {removed_count} background pixels matching RGB({bg_r},{bg_g},{bg_b})")

print("All background removals completed successfully!")
