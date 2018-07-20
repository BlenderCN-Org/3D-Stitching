import numpy as np

class triangle:
	def __init__(self, id, v_a, v_b, v_c, model_num, texels):			# need texels
		# id is generated outside the initialization
		self.id = id
		self.model_num = model_num
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
	result.append(list(tlist1[min_triangle1], tlist2[min_triangle2]))
	# mark as paired
	tlist1[min_triangle1].paired = True
	tlist2[min_triangle2].paired = True

	# loop through Model 1
	for i in range(0, len(tlist1)):
		found_pair = find_pair(tlist1[i], tlist2)
		if (found_pair[0]):
			print ("Error: Triangle " + str(i) + " in model 1 is not paired.")
			continue
		tlist1[i].paired = True
		tlist2[found_pair[1]].paired = True
		result.append(list(tlist1[i], tlist2[found_pair[1]]))

	# loop through Model 2
	for i in range(0, len(tlist2)):
		if (tlist2[i].paired == False):
			found_pair = find_pair(tlist2[i], tlist1)
			if (found_pair[0]):
				print ("Error: Triangle " + str(i) + " in model 2 is not paired.")
				continue
			tlist1[found_pair[1]].paired = True
			tlist2[i].paired = True
			result.append(list(tlist2[i], tlist1[found_pair[1]]))

	# Output result list of pairs
	opt_pair = open("pair_result.txt", "w")
	opt_pair.write("List of paired triangles\n")
	opt_pair.write("Total number of triangles paired: " + str(len(result)))
	for i in range(0, len(result)):
		opt_pair.write(str(result[i][0].id) + " (" + str(result[i][0].model_num) + ") -- " + str(result[i][1].id)\
		 + " (" + str(result[i][0].model_num) + ")")
	opt_pair.close()

	# Output any triangles that are not paired
	for i in range(0, len(tlist1)):
		if (tlist1[i].paired == False):
			print (str(tlist1[i].id) + " (" + str(tlist1[i][0].model_num) + ") is not paired.")
	for i in range(0, len(tlist2)):
		if (tlist2[i].paired == False):
			print (str(tlist2[i].id) + " (" + str(tlist2[i][0].model_num) + ") is not paired.")

	return result

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

if __name__ == '__main__':
	main()