import math

class triangle:
	def __init__(self, v_a, v_b, v_c, texels):			# need texels
		# distance between vertices and center of individual model: v_a (most outside) > v_b > v_c (most inside)
		self.vertex_a = v_a
		self.vertex_b = v_b
		self.vertex_c = v_c
		self.texels = texels							# need texels
		self.centroid = calculate_centroid(self.vertex_a, self.vertex_b, self.vertex_c)
		# a Bool value used in pairing triangles from two models
		self.paired = False

	# calculate centroid (i.e. center) of triangle
	def calculate_centroid(vertex_a, vertex_b, vertex_c):
		return [(vertex_a[0] + vertex_b[0] + vertex_c[0]) / 3.0,
			(vertex_a[1] + vertex_b[1] + vertex_c[1]) / 3.0,
			(vertex_a[2] + vertex_b[2] + vertex_c[2]) / 3.0]

def pair_triangles(tlist1, tlist2):
	# output list
	result = list()
	# find the closest two by comparing the weights
	min_triangle1 = -1
	min_triangle2 = -1
	min_tlist1 = [math.inf] * 3
	min_tlist2 = [math.inf] * 3
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
	result.append(list(tlist1[min_triangle1], tlist2[min_triangle2]))
	# mark as paired
	tlist1[min_triangle1].paired = True
	tlist2[min_triangle2].paired = True

	# loop through Model 1
	for i in range(0, len(tlist1)):
		min_triangle2 = -1
		dist = math.inf
		# assume the triangles in each tlist are in a direction along model sides
		prev_dist = math.inf
		for j in range(0, len(tlist2)):
			

if __name__ == '__main__':
	main()