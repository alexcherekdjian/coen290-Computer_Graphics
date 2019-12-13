# Alex Cherekdjian
# Professor Wang
# COEN 290
# November 17, 2019

from PIL import Image, ImageDraw
import csv

def draw_pixel(x,y, color):
    pixels[x,y] = (color,0,0)

# creating new workspace
img = Image.new('RGB', (600, 600))
pixels = img.load()

# this list hold all vertices - [[x1, y1, z1], [x2, y2, z2],......]
vertices = []

#read in face vertices
with open('face-vertices.data') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # read in all the vertex values
    for row in csv_reader:    
        vertices.append(row)

    # list for storing all the vertex prime values
    vertex_prime = []

    # calculate and draw all points
    for point in vertices:

        # | x' = x/(1-(z/d)) | y' = y/(1-(z/d)) | z' = 0 | d = 1
        point[0] = round(float(point[0]) / (1- float(point[2])) * -600) + 300 # x prime calc and scaling to fit in window
        point[1] = round(float(point[1]) / (1- float(point[2])) * -600) + 280 # y prime calc and scaling to fit in window
        point[2] = 0 # z prime

        # add new point to vertex prime list for face-indexes later
        vertex_prime.append(point)

        # draw the point
        draw_pixel(point[0], point[1], 255)

# read in all face indexs
with open('face-index.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # init draw variable
    draw = ImageDraw.Draw(img)

    # drawing lines from each index
    for index in csv_reader:

        # get vertex corresponding to index read
        vertex_0 = vertex_prime[int(index[0])]
        vertex_1 = vertex_prime[int(index[1])]
        vertex_2 = vertex_prime[int(index[2])]

        # draw lines from those vertex, should create a triangle 
        draw.line((vertex_0[0], vertex_0[1], vertex_1[0], vertex_1[1]), fill=255) # vertex 0 - 1
        draw.line((vertex_1[0], vertex_1[1], vertex_2[0], vertex_2[1]), fill=255) # vertex 1 - 2
        draw.line((vertex_2[0], vertex_2[1], vertex_0[0], vertex_0[1]), fill=255) # vertex 2 - 0

# show to final image
img.show()
