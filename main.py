import sys
import numpy as np

class line:
	def __init__(self, pt1, pt2):
		self.x_0 = pt1[0]
		self.y_0 = pt1[1]
		self.z_0 = pt1[2]
		self.slope_x = pt2[0]-pt1[0]
		self.slope_y = pt2[1]-pt1[1]
		self.slope_z = pt2[2]-pt1[2]
		self.midpoint = cal_midpoint(pt1, pt2)

	def cal_midpoint(pt1, pt2):
		return [pt1[0]+(pt2[0]-pt1[0])/2.0,\
			pt1[1]+(pt2[1]-pt1[1])/2.0,\
			pt1[2]+(pt2[2]-pt1[2])/2.0]

class plane:
	# ax+by+cz+d=0
	def __int__(self, pt, line):
		self.a = line.slope_x
		self.b = line.slope_y
		self.c = line.slope_z
		self.d = -(line.slope_x*pt[0]+line.slope_y*pt[1]+line.slope_z*pt[2])

class triangle:
	# outermost_index is the two of numbers (0,1,2) to point out which two vertices make up the outermost side
	# for example, (0,2) means the side made up by v_a and v_c
	# outermost side is the side of the three sides that is (1) most closed to the edge to be stitched and (2) most distant from center of model
	def __init__(self, id, v_a, v_b, v_c, outermost_index, model_num, texel):			# need texel
		# id is generated outside the initialization
		self.id = id
		self.model_num = model_num
		# distance between vertices and center of individual model: v_a (most outside) > v_b > v_c (most inside)
		self.vertex_a = v_a
		self.vertex_b = v_b
		self.vertex_c = v_c
		self.texel = texel							# need texel
		self.centroid = calculate_centroid(self.vertex_a, self.vertex_b, self.vertex_c)
		self.outermost = (none, none)
		# the paired list will be filled when calling function add_paired_triangles
		self.paired_list = list()
		if (outermost_index[0] == outermost_index[1]):
			print ("Error: triangle ID " + str(self.id) + " from model " + str(self.model_num) + " has duplicated outermost_index.")
		else:
			if (outermost_index[0] == 0):
				self.outermost[0] = self.vertex_a
			elif (outermost_index[0] == 1):
				self.outermost[0] = self.vertex_b
			elif (outermost_index[0] == 2):
				self.outermost[0] = self.vertex_c
			else:
				print ("Error: triangle ID " + str(self.id) + " from model " + str(self.model_num) + " has invalid outermost_index[0].")
			if (outermost_index[1] == 0):
				self.outermost[1] = self.vertex_a
			elif (outermost_index[1] == 1):
				self.outermost[1] = self.vertex_b
			elif (outermost_index[1] == 2):
				self.outermost[1] = self.vertex_c
			else:
				print ("Error: triangle ID " + str(self.id) + " from model " + str(self.model_num) + " has invalid outermost_index[1].")

		# valid is a Bool value to show whether the object is valid upon initialization
		self.valid = False
		# how to check validity of texel?
		if (isinstance(self.id, int) && len(self.vertex_a)==len(self.vertex_b)==len(self.vertex_c)==3):
			self.valid = True

	# DO NOT USE __del__
	def discard_unpaired_triangles(tlist):
		for i in range(0, len(tlist)):
			if (len(tlist[i].paired_list) == 0):
				tlist[i].valid = False

	# calculate centroid (i.e. center) of triangle
	def calculate_centroid(vertex_a, vertex_b, vertex_c):
		return [(vertex_a[0] + vertex_b[0] + vertex_c[0]) / 3.0,\
			(vertex_a[1] + vertex_b[1] + vertex_c[1]) / 3.0,\
			(vertex_a[2] + vertex_b[2] + vertex_c[2]) / 3.0]

class quadrilateral:
	def __init__(self, id, v_a, v_b, v_c, v_d, texel):								# need texel
		self.id = id
		self.vertex_a = v_a
		self.vertex_b = v_b
		self.vertex_c = v_c
		self.vertex_d = v_d
		self.texel = texel															# need texel

		# valid is a Bool value to show whether the object is valid upon initialization
		self.valid = False
		# how to check validity of texel?
		if (isinstance(self.id, int) && len(self.vertex_a)==len(self.vertex_b)==len(self.vertex_c)==3):
			self.valid = True

	def assign_texture(self, texel):
		# extend texel
		self.texel = texel

def pair_triangles(tlist1, tlist2):
	# find the closest two by comparing the weights
	min_triangle1 = -1
	min_triangle2 = -1
	min_tlist1 = [np.inf] * 3
	min_tlist2 = [np.inf] * 3
	for i in range(0, len(tlist1)):
		if ((tlist1[i].centroid[0] < min_tlist1[0]) || (tlist1[i].centroid[1] < min_tlist1[1])\
		 || (tlist1[i].centroid[2] < min_tlist1[2])):
			min_triangle1 = i
			min_tlist1 = tlist1[i].centroid
	for i in range(0, len(tlist2)):
		if ((tlist2[i].centroid[0] < min_tlist2[0]) || (tlist2[i].centroid[1] < min_tlist2[1])\
		 || (tlist2[i].centroid[2] < min_tlist2[2])):
			min_triangle2 = i
			min_tlist2 = tlist2[i].centroid

	# start pairing
	tlist1[min_triangle1].paired_list.add(tlist2[min_triangle2])
	tlist2[min_triangle2].paired_list.add(tlist1[min_triangle1])

	# loop through Model 1
	for i in range(0, len(tlist1)):
		found_pair = find_pair(tlist1[i], tlist2)
		if (found_pair[0]):
			print ("Error: Triangle " + str(i) + " in model 1 is not paired.")
			continue
		tlist1[i].paired_list.add(tlist2[found_pair[1]])
		tlist2[found_pair[1]].paired_list.add(tlist1[i])

	# loop through Model 2
	for i in range(0, len(tlist2)):
		if (len(tlist2[i].paired_list) == 0):
			found_pair = find_pair(tlist2[i], tlist1)
			if (found_pair[0]):
				print ("Error: Triangle " + str(i) + " in model 2 is not paired.")
				continue
			tlist2[i].paired_list.add(tlist1[found_pair[1]])
			tlist1[found_pair[1]].paired_list.add(tlist2[i])

	# Output result list of pairs in a new txt file
	opt_pair = open("pair_result.txt", "w")
	opt_pair.write("List of paired triangles\n")
	for i in range(0, len(tlist1)):
		tmp_out = str(tlist1[i].id) + " (Model 1) -- "
		for triangle in tlist1[i].paired_list:
			tmp_out += str(triangle.id) + " "
		opt_pair.write(tmp_out)
	for i in range(0, len(tlist2)):
		tmp_out = str(tlist2[i].id) + " (Model 2) -- "
		for triangle in tlist2[i].paired_list:
			tmp_out += str(triangle.id) + " "
		opt_pair.write(tmp_out)
	opt_pair.close()

	# Output any triangles that are not paired in terminal
	for i in range(0, len(tlist1)):
		if (len(tlist1[i].paired_list) == 0):
			print (str(tlist1[i].id) + " (" + str(tlist1[i][0].model_num) + ") is not paired.")
	for i in range(0, len(tlist2)):
		if (len(tlist2[i].paired_list) == 0):
			print (str(tlist2[i].id) + " (" + str(tlist2[i][0].model_num) + ") is not paired.")

# Find the triangle from tlist to pair with the triangle target
def find_pair(target, tlist):
	min_triangle = -1
	dist = np.inf
	# assume the triangles in tlist are in a direction along model sides
	prev_dist = np.inf
	for j in range(0, len(tlist)):
		dist = point_distance(target, tlist[j])
		if (dist > prev_dist):
			break
		prev_dist = dist
		min_triangle = j
	# if no triangle is available to be paired, return False
	if (min_triangle == -1):
		return (False, -1)
	return (True, min_triangle)

def point_distance(point1, point2):
	a = np.array((point1.centroid[0], point1.centroid[1], point1.centroid[2]))
	b = np.array((point2.centroid[0], point2.centroid[1], point2.centroid[2]))
	return np.linalg.norm(a-b)

def generate_quadrilateral(tri1, tri2, id1=-1, id2=-1):
	# check validity of triangles
	if (!tri1.valid && !tri2.valid):
		# be careful with the returned Bool
		return False

	whole = cal_outermost_quadrilateral(tri1, tri2)
	return divide_quadrilateral(whole, tri1, tri2, id1, id2)

def cal_outermost_quadrilateral(tri1, tri2):
	# compute the correct order to align four vertices
	diff_1 = [0, 0, 0]
	diff_2 = [0, 0, 0]
	# x_2-x_1+x_4-x_3, y_2-y_1+y_4-y_3, z_2-z_1+z_4-z_3
	for i in range (0, 3):
		diff_1[i] = tri1.outermost[1][i]-tri1.outermost[0][i]+tri2.outermost[1][i]-tri2.outermost[0][i]
	# x_2-x_1+x_3-x_4, y_2-y_1+y_3-y_4, z_2-z_1+z_3-z_4
	for i in range (0, 3):
		diff_2[i] = tri1.outermost[1][i]-tri1.outermost[0][i]+tri2.outermost[0][i]-tri2.outermost[1][i]

	if (diff_1[0]**2+diff_1[1]**2+diff_1[2]**2 >= diff_2[0]**2+diff_2[1]**2+diff_2[2]**2):
		# id here is not used in following steps, so set to default -1
		return quadrilateral(-1, tri1.outermost[0], tri1.outermost[1], tri2.outermost[0], tri2.outermost[1], tri1.texel)
	else:
		return quadrilateral(-1, tri1.outermost[0], tri1.outermost[1], tri2.outermost[1], tri2.outermost[0], tri2.texel)

def divide_quadrilateral(quad, tri1, tri2, id1=-1, id2=-1, texel1, texel2):						# need texel
	line_of_centroids = line(tri1.centroid, tri2.centroid)
	orthogonal_plane = plane(line_of_centroids.midpoint, line_of_centroids)
	cross_line = find_line_cross_quad_and_plane(quad, orthogonal_plane)
	# need texel
	extended1 = quadrilateral(id1, quad.v_a, quad.v_b, pt2, pt1, None)
	extended2 = quadrilateral(id2, pt1, pt2, quad.v_c, quad.v_d, None)
	# extend_texture should be called afterwards, because should pair all triangles at the first pace
	return tuple(extended1, extended2)

def extend_texture(quad, texel):
	quad.assign_texture(texel)

def find_line_cross_quad_and_plane(quad, plane):
	t1 = (plane.d+plane.a*quad.v_a[0]+plane.b*quad.v_a[1]+plane.c*quad.v_a[2])*1.0/(plane.a*quad.v_a[0]-plane.a*quad.v_d[0]+plane.b*quad.v_a[1]-plane.b*quad.v_d[1]+plane.c*quad.v_a[2]-plane.c*quad.v_d[2])
	t2 = (plane.d+plane.a*quad.v_b[0]+plane.b*quad.v_b[1]+plane.c*quad.v_b[2])*1.0/(plane.a*quad.v_b[0]-plane.a*quad.v_c[0]+plane.b*quad.v_b[1]-plane.b*quad.v_c[1]+plane.c*quad.v_b[2]-plane.c*quad.v_c[2])
	pt1 = [t1*quad.v_d[0]+(1.0-t1)*quad.v_a[0], t1*quad.v_d[1]+(1.0-t1)*quad.v_a[1], t1*quad.v_d[2]+(1.0-t1)*quad.v_a[2]]
	pt2 = [t2*quad.v_c[0]+(1.0-t2)*quad.v_b[0], t2*quad.v_c[1]+(1.0-t2)*quad.v_b[1], t2*quad.v_c[2]+(1.0-t2)*quad.v_b[2]]
	return tuple(tuple(pt1, pt2), line(pt1, pt2))

def main():
	if (len(sys.argv) != 3):
		print ("Usage: main.py [input_obj] [output_obj]")
		return 1
	# Test to open input file

	# Test to create output file

	# Create two triangle lists in global
	'''
	*** Blender API opens input obj ***
	tlist1
	tlist2
	'''
	# Pair triangle lists
	pair_triangles(tlist1, tlist2)
	# Generate quadrilaterals

	# Compute textures
	'''
	*** Blender API and additional script ***
	'''
	# Extend texture

	# Discard unpaired triangles by check attribute valid in triangle object

	# Output obj file
	'''
	Blender API
	'''
	return 0

if __name__ == '__main__':
	main()