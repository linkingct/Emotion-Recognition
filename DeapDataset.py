import os
import torch
import h5py
import numpy as np
from torch.utils.data import Dataset, DataLoader

import utils

class DeapDataset(Dataset):

	def __init__(self, root = "./DEAP_dataset", step = "train", seq_length = 3):

		if (step == "train"):
			self.dataset_filename = root + "_train.hdf"
		elif (step == "valid"):
			self.dataset_filename = root + "_valid.hdf"
		elif (setp == 'test'):
			self.dataset_filename = root + "_test.hdf"

		self.seq_length = seq_length

	def __len__(self):

		self.length = utils.read_hdf_processed_labels_return_size(self.dataset_filename) - self.seq_length 
		
		return self.length

	def __getitem__(self, idx):

		# Get item returns a sequence of samples
		data_seq = []
		label_seq = []			
		for i in range(self.seq_length):
			data_file = h5py.File(self.dataset_filename, 'r')

			data = data_file['data'][idx + i]
			label = data_file['labels_val'][idx + i]

			data_file.close()

			data_seq.append(data)
			label_seq.append(label)
					
		data_seq = np.asarray(data_seq)
		label_seq = np.asarray(label_seq[0])
		label_seq = torch.from_numpy(label_seq).long().view(-1, 1)
		sample = {'data': torch.from_numpy(data_seq).float(), 'label': label_seq}

		return sample



