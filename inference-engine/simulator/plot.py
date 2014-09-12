


people = ambient.people_points.round().astype(np.int32)
people_true = true_points.round().astype(np.int32)
people_false = false_points.round().astype(np.int32)

map_diff = 10
mks = 12

plt.xlim(-map_diff, ambient.map_size[0] + map_diff)
plt.ylim(-map_diff, ambient.map_size[1] + map_diff)

plt.plot(people[:, 0], people[:, 1], 'b^', label='People', markersize=mks+10)
plt.plot(people_false[:, 0], people_false[:, 1], 'ro', label='False People', markersize=mks)
plt.plot(people_true[:, 0], people_true[:, 1], 'go', label='True People', markersize=mks/2)
plt.show()
