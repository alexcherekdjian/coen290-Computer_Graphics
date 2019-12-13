# Alex Cherekdjian 
# Professor Wang
# COEN 290
# December 7, 2019

from utils import Sphere, Point, Vector, RGB_Float
from PIL import Image
from math import sqrt

# global picture width and height
img_width = 320
img_height = 240

def main():
	# creating a new image
	img = Image.new('RGB', (img_width, img_height), (20,20,20)) # creating dark grey background
	pixels = img.load() 

	# sphere 1 definition
	center1 = Point(120,120, -50)
	radius1 = 60
	color1 = RGB_Float(0.0, 0.0, 1.0)

	# sphere 2 definition
	center2 = Point(240, 180, -50)
	radius2 = 50
	color2 = RGB_Float(0.0, 1.0, 0.0)
	
	# sphere 3 definition
	center3 = Point(20, 50, -50)
	radius3 = 20
	color3 = RGB_Float(1.0, 1.0, 0.0)

	# init spheres
	sphere1 = Sphere(center1, radius1, color1)
	sphere2 = Sphere(center2, radius2, color2)
	sphere3 = Sphere(center3, radius3, color3)

	# creating sphere list
	sphere_list = [sphere1, sphere2, sphere3]

	# running raycasting algorithm
	rayCasting(pixels, sphere_list)

	# displaying the image
	img.save("result", "PNG")
	img.show()

def rayCasting(pixels, sphere_list):
	global img_width, img_height

	# defining eye, light position, and light RGB
	eye = Point(160,120,140)
	light_RGB = RGB_Float(255,255,255) # white light
	light_V = Vector(5000, 0, 0) # y = 0

	# for every sphere go through every pixel
	for sphere in sphere_list:
		for x in range(0, img_width):
			for  y in range(0, img_height):

				# used in case pixel is not apart of a shadow or background
				color_point = True

				# u vector calculation
				u = Vector(x - eye.x, y - eye.y, 0 - eye.z)
				u_unit = unitVector(u)

				# B calculation
				B = calculateB(eye, sphere, u_unit)

				# C calculation
				C = calculateC(eye, sphere)

				# calculating intersection check
				b_squared_minus_four_c = B**2 - 4 * C
				
				# for each point chech b^2-4c is positive, if not its in the background so ignore point
				if b_squared_minus_four_c >= 0:

					# get the square root
					sqrt_b_squared_minus_four_c = sqrt(b_squared_minus_four_c) 

					# find the correct value for t (closest intersection point)
					t_minus = (-B - sqrt_b_squared_minus_four_c) / 2
					t_plus = (-B + sqrt_b_squared_minus_four_c) / 2

					if t_minus < t_plus:
						t = t_minus
					else:
						t = t_plus

					# calculate intersection
					intersection = Point(eye.x + t * u_unit.x, eye.y + t * u_unit.y, eye.z + t * u_unit.z)

					# for every sphere other than itself, check for intersections
					for sphere_test in sphere_list:

						# checking whether sphere is itself
						if sphere == sphere_test:
							continue

						# if the sphere is not in front of the sphere we are testing, then skip
						distance_test = sqrt((light_V.x - sphere_test.center.x)**2 + (light_V.y - sphere_test.center.y)**2\
								+ (light_V.z - sphere_test.center.z)**2)

						distance_sphere = sqrt((light_V.x - sphere.center.x)**2 + (light_V.y - sphere.center.y)**2\
								+ (light_V.z - sphere.center.z)**2)

						if distance_sphere < distance_test:
							continue

						# calculate u check vector
						u_check = Vector(light_V.x - intersection.x, light_V.y - intersection.y, light_V.z - intersection.z)
						check_unit = unitVector(u_check)

						# calculate B
						B_temp = calculateB(intersection, sphere_test, check_unit)

						# calculate C
						C_temp = calculateC(intersection, sphere_test)

						# calculate intersection test
						b_squared_minus_four_c_temp = B_temp**2 - 4 * C_temp

						# if true, another sphere intersects light, so set pixel black, if not check other spheres
						if b_squared_minus_four_c_temp >= 0:
							pixels[x, y] = (0,0,0)

							# if pixel colored black, no need to run pixel coloring algorithm
							color_point = False
							break
					
					# if pixel is not in a shadow or apart of the background, find the color for pixel
					if color_point:

						# calculate normal vector and unit light vector
						N = Point(intersection.x - sphere.center.x, intersection.y - sphere.center.y, intersection.z - sphere.center.z)
						n_unit = unitVector(N)
						light_V_unit = unitVector(light_V)


						# calculate angle
						cos_A = n_unit.x * light_V_unit.x + n_unit.y * light_V_unit.y + n_unit.z * light_V_unit.z

						# clamp angle if below zero 
						if cos_A < 0:
							cos_A = 0

						# calculate the new color
						new_color = RGB_Float(sphere.color.r * light_RGB.r * cos_A, \
							sphere.color.g * light_RGB.g * cos_A, sphere.color.b * light_RGB.b * cos_A)

						# assign pixel to that color
						pixels[x, y] = (int(new_color.r), int(new_color.g), int(new_color.b))

def unitVector(vector):
	# used to calculate the unit vector 
	vector_len = sqrt(vector.x**2 + vector.y**2 + vector.z**2)
	vector_unit = Vector(vector.x / vector_len, vector.y / vector_len, vector.z / vector_len)
	return vector_unit

def calculateB(vector, sphere, unit):
	# used to calculate B
	B = 2 * ((vector.x - sphere.center.x) * unit.x + (vector.y - sphere.center.y) \
					* unit.y + (vector.z - sphere.center.z) * unit.z)
	return B

def calculateC(vector, sphere):
	# used to calculate C
	C = (vector.x - sphere.center.x)**2 + (vector.y - sphere.center.y)**2 \
				+ (vector.z - sphere.center.z)**2 - (sphere.radius)**2
	return C


if __name__ == "__main__":
	main()