from rectpack import newPacker
from PIL import Image
import glob, os

# ---===Settings===---

# Directory to pack
path = r"D:\pics\temp" + "\\"
# Output path
outpath = r"D:\Programming\rectangle-packing" + "\\"

# width multiplier
mw = 2.4
# height multiplier
mh = 2.9



canvasw = int(round(1920*mw,0))
canvash = int(round(1080*mh,0))

rectangles = []

os.chdir(path)
for name in glob.glob("*.png"):
	im = Image.open(path + name)
	w,h = im.size
	rectangles.append((w,h,name))

incount = len(rectangles)

#init_bins = [(1920, 1080), (1920, 1080*2), (1920*2, 1080*2)]

init_bins = [(canvasw, canvash)]


# Packer: PACKING START------------------------------------------
# Packer: Create packer item
packer = newPacker(rotation=False)

# Packer: Add rectangles and bins
for r in rectangles:
	packer.add_rect(*r)

for b in init_bins:
	packer.add_bin(*b)

# Packer: Pack it
packer.pack()

# Get list of all rectangles (only this method shows "rid", just listing doesn't show idk why)
all_rects = packer.rect_list()

# Check if all input images are used
outcount = len(all_rects)
if incount != outcount:
	print("Base canvas is too small, can't fit!")
	print("Adjust 'mw' and 'mh' multipliers please!")
	print("Dimensions: {}x{}".format(canvasw,canvash))
	print("Fitted: {}/{}".format(outcount,incount))
	quit()
else:
	print("Packing success!")
	print("Dimensions: {}x{}".format(canvasw,canvash))
	print("Fitted: {}/{}".format(outcount,incount))


# Packer: PACKING FINISHED------------------------------------------

# PIL: START TO DRAW IMAGE------------------------------------------
nbins = len(packer)
imgs = []

# PIL: Create base image for each bin
for b in range(nbins):
	imgs.append(Image.new("RGBA",(packer[b].width, packer[b].height),(255,255,255)))
	#imgs[b].show()

# Draw rectangles' corresponding image files at base image
for rect in all_rects:
	b, x, y, w, h, rid = rect
	# b - Bin index
	# x - Rectangle bottom-left corner x coordinate
	# y - Rectangle bottom-left corner y coordinate
	# w - Rectangle width
	# h - Rectangle height
	# rid - User asigned rectangle id or None
	clip = Image.open(path+rid)
	imgs[b].paste(clip, (x,y))

# PIL: FINISH DRAWING IMAGE------------------------------------------



# Save each bin's image (Use when multiple bins are involved)
for b in range(nbins):
	print("Saving 'output{:02d}.png'...".format(b))
	imgs[b].save(outpath + 'output{:02d}.png'.format(b), "PNG")
	print("Saved 'output{:02d}.png'!".format(b))

# Display each bin's image (Use when multiple bins are involved)
#for b in range(nbins):
#	imgs[b].show()




