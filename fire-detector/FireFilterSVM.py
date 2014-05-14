import cv2
import numpy as np

class StatModel(object):
	'''parent class - starting point to add abstraction'''
	def load(self, fn):
		self.model.load(fn)
	def save(self, fn):
		self.model.save(fn)

class SVM(StatModel):
	'''wrapper for OpenCV SimpleVectorMachine algorithm'''
	def __init__(self):
		self.model = cv2.SVM()

	def train(self, samples, responses):
		#setting algorithm parameters

		params = dict( kernel_type = cv2.SVM_LINEAR,
									 svm_type = cv2.SVM_C_SVC,
									 C = 1 )

		self.model.train(samples, responses, params = params)

	def predict(self, samples):
		return np.float32( [self.model.predict(s) for s in samples])

def serialize_image(img, window_size):

	descriptors = np.empty( shape = (0, window_size * window_size * 3 ), dtype = np.float32 )

	for x in xrange(0, img.shape[0], window_size):
		for y in xrange(0, img.shape[1], window_size):

			if x + window_size > img.shape[0] or y + window_size > img.shape[1]:
				continue

			roi = img[x:x + window_size, y: y + window_size ]
			roi = roi.reshape( (1, window_size * window_size * 3) )

			descriptors = np.concatenate( (descriptors, roi), axis = 0 )

	return descriptors

def create_samples(texture_folder, file_names, window_size):

	samples = np.empty( shape = (0, window_size * window_size * 3), dtype = np.float32 )

	for idx, file_name in enumerate(file_names):

		img = cv2.imread( texture_folder + file_name )

		sample = serialize_image( img, window_size )
		samples = np.concatenate( (samples, sample), axis = 0 )

	return samples

def test_image(svm, img, window_size):

	output = np.zeros( shape = ( img.shape[0], img.shape[1], 1 ) )

	for x in xrange(0, img.shape[0], window_size):
		for y in xrange(0, img.shape[1], window_size):

			if x + window_size > img.shape[0] or y + window_size > img.shape[1]:
				continue

			roi = img[x:x + window_size, y: y + window_size ]
			roi = roi.reshape( (1, window_size * window_size * 3) ).astype( np.float32 )

			y_val = svm.predict( roi )

			output[x:x + window_size, y: y + window_size] = (255 if y_val.any() else 0)

	return output

def run():

	# samples = np.array(np.random.random((4,2)), dtype = np.float32)
	# y_train = np.array([1.,0.,0.,1.], dtype = np.float32)

	window_size = 5
	# texture_folder = "img/textures/"

	# positive_textures = ["fire_texture.png"]
	# negative_textures = ["other1.png", "other2.png", "other3.png",
	# 										 "other4.png", "other5.png", "other6.png",
	# 										 "other7.png", "other8.png"]
	# test_textures = ["test1_texture.png", "grass_target.jpg"]

	# positive_samples = create_samples(texture_folder, positive_textures, window_size)
	# negative_samples = create_samples(texture_folder, negative_textures, window_size)
	# test_samples = create_samples(texture_folder, test_textures, window_size)

	# positive_class = np.ones( shape = ( positive_samples.shape[0] ), dtype = np.float32 )
	# negative_class = np.zeros( shape = ( negative_samples.shape[0] ), dtype = np.float32 )

	# x_train = np.concatenate( (positive_samples, negative_samples), axis = 0 ).astype( np.float32 )
	# y_train = np.concatenate( (positive_class, negative_class), axis = 0 )

	# print x_train.shape
	# print y_train.shape

	clf = SVM()
	# clf.train(x_train, y_train)
	# clf.save("model_02")

	clf.load("model_02")

	# image = cv2.imread("fogo/5.png")

	# output = test_image(clf, image, window_size)

	# cv2.imwrite("fogo/result_5.png", output)

	# capture = cv2.VideoCapture(0)

	counter = 0

	for x in xrange(0,136):
		frame = cv2.imread("new_data/data_%i.png" % counter)
		counter += 1

		output = test_image(clf, frame, window_size)

		cv2.imshow("test", frame)
		cv2.imshow("image", output)

		cv2.waitKey(1)

	# while capture.isOpened():
	# 	ref, frame = capture.read()

	# 	output = test_image(clf, frame, window_size)

	# 	cv2.imshow("test", frame)
	# 	cv2.imshow("image", output)

	# 	cv2.imwrite("new_data2/data_%i.png" % counter, frame)
	# 	counter += 1

	# 	if cv2.waitKey(1) & 0xFF == ord('q'):
	# 		break

	# capture.release()
	# cv2.destroyAllWindows()

	# y_val = clf.predict( test_samples )
	# print y_val[ y_val == 0.0 ].size
	# print y_val[ y_val == 1.0 ].size

if __name__ == "__main__":
	run()
