import cv2
import numpy as np

class SVM(object):
	def __init__(self):
		self.model = cv2.SVM()

	def load(self, fn):
		self.model.load(fn)

	def save(self, fn):
		self.model.save(fn)

	def train(self, samples, responses):
		params = dict( kernel_type = cv2.SVM_LINEAR,
									 svm_type = cv2.SVM_C_SVC,
									 C = 1 )

		self.model.train(samples, responses, params = params)

	def predict(self, samples):
		return np.float32( [self.model.predict(s) for s in samples])

class Detector(SVM):

	def __init__(self, window_size = 10):
		super(Detector, self).__init__()
		self.ws = window_size

	def serialize_image(self, img):

		descriptors = np.empty( shape = (0, self.ws * self.ws * 3 ), dtype = np.float32 )

		for x in xrange(0, img.shape[0], self.ws):
			for y in xrange(0, img.shape[1], self.ws):

				if x + self.ws > img.shape[0] or y + self.ws > img.shape[1]:
					continue

				roi = img[x:x + self.ws, y: y + self.ws ]
				roi = roi.reshape( (1, self.ws * self.ws * 3) )

				descriptors = np.concatenate( (descriptors, roi), axis = 0 )

		return descriptors

	def create_samples(self, texture_folder, file_names):

		samples = np.empty( shape = (0, self.ws * self.ws * 3), dtype = np.float32 )

		for idx, file_name in enumerate(file_names):

			img = cv2.imread( texture_folder + file_name )

			sample = self.serialize_image( img )
			samples = np.concatenate( (samples, sample), axis = 0 )

		return samples

	def train_model(self, texture_folder, positive_textures, negative_textures):

		positive_samples = self.create_samples(texture_folder, positive_textures)
		negative_samples = self.create_samples(texture_folder, negative_textures)

		positive_class = np.ones( shape = ( positive_samples.shape[0] ), dtype = np.float32 )
		negative_class = np.zeros( shape = ( negative_samples.shape[0] ), dtype = np.float32 )

		x_train = np.concatenate( (positive_samples, negative_samples), axis = 0 ).astype( np.float32 )
		y_train = np.concatenate( (positive_class, negative_class), axis = 0 )

		self.train(x_train, y_train)

		return self

	def test_image(self, img):

		output = np.zeros( shape = ( img.shape[0], img.shape[1], 1 ) )

		for x in xrange(0, img.shape[0], self.ws):
			for y in xrange(0, img.shape[1], self.ws):

				if x + self.ws > img.shape[0] or y + self.ws > img.shape[1]:
					continue

				roi = img[x:x + self.ws, y: y + self.ws ]
				roi = roi.reshape( (1, self.ws * self.ws * 3) ).astype( np.float32 )

				y_val = self.predict( roi )

				output[x:x + self.ws, y: y + self.ws] = (255 if y_val.any() else 0)

		return output
