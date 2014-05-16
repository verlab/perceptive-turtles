import texture_filter_svm
import cv2

def run():
	# texture_folder = "textures/"
	# positive_textures = ["fire_texture.png"]
	# negative_textures = ["other1.png", "other2.png", "other3.png","other4.png", "other5.png", "other6.png","other7.png", "other8.png"]

	detector = texture_filter_svm.Detector()
	# detector.train_model(texture_folder, positive_textures, negative_textures).save("model_05")
	detector.load("model_05")

	counter = 0

	for x in xrange(0,206):
		frame = cv2.imread("data_%i.png" % counter)
		counter += 1

		output = detector.test_image( frame )

		cv2.imshow("image", output)
		cv2.imshow("test", frame)

		cv2.waitKey(1)

if __name__ == "__main__":
	run()
