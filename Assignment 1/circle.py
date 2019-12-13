# Alex Cherekdjian
# Professor Wang
# COEN 290
# October 17, 2019

from PIL import Image

# defining global (x,y) centers of circle and radius
radius = 100
x_center = 160
y_center = 120

def main(): 
	img = Image.new('RGB', (320, 240)) # creating black background
	pixels = img.load() 
	
	outline(pixels) # running circle outline algo
	fill(img, pixels) # running circle fill algo
	antiAlias(pixels) # running circle anti-alias algo

	img.show() # displaying the image


def outline(pixels):
	# defining constants used in midpoint algo
	d = (5/4) - radius 
	x = 0
	y = radius

	while y >= x:
		# printing pixels
		pixels[x_center + x, y_center + y] = (0,255,0)
		pixels[x_center + x, y_center - y] = (0,255,0)
		pixels[x_center - x, y_center + y] = (0,255,0)
		pixels[x_center - x, y_center - y] = (0,255,0)
		pixels[x_center + y, y_center + x] = (0,255,0)
		pixels[x_center + y, y_center - x] = (0,255,0)
		pixels[x_center - y, y_center + x] = (0,255,0)
		pixels[x_center - y, y_center - x] = (0,255,0)

		# if d less than 0, update midpoint to M(e), inc x, and y stays the same
		if d < 0:
			d += 2 * x + 3
			x += 1

		# if d greater than 0, update midpoint to M(se), inc x, and dec y
		else:
			d+= 2*(x - y) + 5
			x += 1
			y -= 1

def fill(img, pixels):
	# scanning through all y pixels on screen
	for temp_y in range(0, 240):

		# initializing constants
		inside = False
		temp_x = 0

		# circle edges case handeling, no filling to be done since just lines
		if temp_y == (y_center+radius) or temp_y == (y_center-radius):
			continue

		# scanning through all x pixels on screen 
		while temp_x < 320:

			# getting pixel color information
			xy = (temp_x,temp_y)
			pc = img.getpixel(xy)
			
			# if the pixel is the color green, edge has been found
			if pc[1] == 255:

				# check the next pixel color in case the circle edge is multi-pixeled
				xy_next = (temp_x+1,temp_y)
				pc_next = img.getpixel(xy_next)

				# if next pixel is green, still at circle edge, keep going until black pixel found
				while pc_next[1] == 255:
					temp_x+=1
					xy_next = (temp_x,temp_y)
					pc_next = img.getpixel(xy_next)

				# once black pixel found, toggle inside circle bool to start painting pixels green
				if inside == False:
					inside = True

				else:
					inside = False

			# if inside the circle then paint pixel
			if inside == True: 
				pixels[temp_x, temp_y] = (0,255,0)

			# go to next pixel
			temp_x+=1

def antiAlias(pixels):
	# scanning through all x and y pixels on screen  
	for y in range(0, 240):
		for x in range (0, 320):

			d = ((x-x_center)**2 + (y-y_center)**2)**0.5 # calculating the current pixels distance from the center of the circle
			alpha = d - radius # calculating how far from the edge of the circle the point is

			# small alpha = belongs to circle or is close to the center
			# large alpha = pixel is far from the center and more to background
			# if alpha is larger or smaller than 0, pixel is part of the main content of the circle
			if alpha > 0 and alpha < 1: 
				color_pixel = (0, round(255 * (1-alpha)),0) # adjusting color of green depending on the alpha
				pixels[x, y] = color_pixel # assigning new color to pixel


if __name__ == "__main__":
	main()
