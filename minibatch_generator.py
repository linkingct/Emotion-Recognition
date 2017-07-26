import numpy as np
import h5py
import os

import torch



class minibatch_generator:

	def __init__(self, minibatch_size = 32, dataset_filename = "DEAP_dataset", dataset_size = 80640, train_prop = 0.7, valid_prop = 0.2):
		
		self.dataset_filename = dataset_filename
		self.dataset_filename_train = self.dataset_filename + "_train.hdf"
		self.dataset_filename_valid = self.dataset_filename + "_valid.hdf"
		self.dataset_size = dataset_size
		self.train_prop = 0.7
		self.valid_prop = 0.2
		self.minibatch_size = minibatch_size


	def minibatch_generator_train(self): #80640 = 32 sub x 63 segments/trial x 40 trials		
	
		number_of_slices = int(np.ceil((self.dataset_size*self.train_prop)/self.minibatch_size))

		while True:
			open_file = h5py.File(self.dataset_filename_train, 'r')
			print(open_file['data'].shape)
			print(open_file['labels'].shape)

			for i in xrange(0, number_of_slices):
				data_minibatch_train = open_file['data'][i*self.minibatch_size:min((i + 1)*self.minibatch_size, self.dataset_size*0.7)]
				labels_minibatch_train = open_file['labels'][i*self.minibatch_size:min((i + 1)*self.minibatch_size, self.dataset_size*0.7)]
       			
				data_minibatch_train = torch.from_numpy(data_minibatch_train)
				data_minibatch_train = data_minibatch_train.float()

				labels_minibatch_train = torch.from_numpy(labels_minibatch_train)
				labels_minibatch_train = labels_minibatch_train.float()

       				yield (data_minibatch_train, labels_minibatch_train)

			open_file.close()

	def minibatch_generator_valid(self): #80640 = 32 sub x 63 segments/trial x 40 trials		
	
		number_of_slices = int(np.ceil((self.dataset_size*self.valid_prop)/self.minibatch_size))
	
		while True:
			open_file = h5py.File(self.dataset_filename_valid, 'r')

			for i in xrange(0, number_of_slices):
				data_minibatch_valid = open_file['data'][i*self.minibatch_size:min((i + 1)*self.minibatch_size, self.dataset_size*0.9)]
				labels_minibatch_valid = open_file['labels'][i*self.minibatch_size:min((i + 1)*self.minibatch_size, self.dataset_7size*0.9)]

				data_minibatch_valid = torch.from_numpy(data_minibatch_valid)
				data_minibatch_valid = data_minibatch_valid.float()

				labels_minibatch_valid = torch.from_numpy(labels_minibatch_valid)
				labels_minibatch_valid = labels_minibatch_valid.float()
       			
       				yield (data_minibatch_valid, labels_minibatch_valid)

			open_file.close()