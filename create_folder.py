# coding: utf-8
'''
					     data  
					      ||
					cats-dogs-redux
                 ____________________________||__________________
                 |	 |	             |	                |
               train	test  	          valid              sample		 
	      ____|___                   _____|___          ______|_______     
              |       |                 |         |        |              |
           cats    dogs               cats     dogs    train            valid
                                               	     ___|___          ____|____    
                                               	    |       |        |         |
                                             	    cats   dogs     cats      dogs

'''
from glob import glob
from random import shuffle
import os, shutil
import zipfile


def train_valid_folders(path,percent=0.8,flag=0):
	train_path = os.path.join(path,'train')
	valid_path = os.path.join(path,'valid')
	
	if not os.path.exists(train_path):
		os.mkdir(train_path)
	if not os.path.exists(valid_path):
		os.mkdir(valid_path)	
    
	if flag:
		all_train = glob(os.path.join(path,'*.*'))
	else:
		all_train = glob(os.path.join(train_path,'*.*'))
	train_set,valid_set = get_split_set(all_train,percent)
	for f in valid_set:
		shutil.move(f,valid_path)
	if flag:
		for f in train_set:
			shutil.move(f,train_path)
				

def sample_folder(path, percent=0.05):
	train_path = os.path.join(path,'train')
	all_train = glob(os.path.join(train_path,'*.*'))
	sample_path = os.path.join(path,'sample')
	if not os.path.exists(sample_path):
		os.mkdir(sample_path)
	_,sample_set = get_split_set(all_train,percent)
	for f in sample_set:
		shutil.copy(f,sample_path)

def get_split_set(all_train,per):
	shuffle(all_train)
	n = len(all_train)
	split_point = int(per*n)
	return all_train[:split_point],all_train[split_point:]

def create_cats_dogs(path):
	cats_path = os.path.join(path,'cats')
	dogs_path = os.path.join(path,'dogs')
	os.mkdir(cats_path)
	os.mkdir(dogs_path)
	cat_files = glob(os.path.join(path,'cat.*'))
	dog_files = glob(os.path.join(path,'dog.*'))

	for f in cat_files:
		shutil.move(f,cats_path)
	for f in dog_files:
		shutil.move(f,dogs_path)    

def main():
	parent_path = '../../data/dogs-vs-cats-redux'
	train_zip_path = os.path.join(parent_path,'train.zip')
	test_zip_path = os.path.join(parent_path,'test.zip')
	train_valid_percent_split = 0.9
	train_sample_percent_split = 0.05	
	
	with zipfile.ZipFile(train_zip_path, "r") as z:
		z.extractall(parent_path)
	with zipfile.ZipFile(test_zip_path, "r") as z:
		z.extractall(parent_path)
	
    # Main train, valid Folders	
	path = parent_path	
	sample_folder(path,train_sample_percent_split)
	train_valid_folders(path,train_valid_percent_split)
	
	# Cats, Dog folders with train and valid folders of Train folder
	path = os.path.join(parent_path,'train')
	create_cats_dogs(path)
	path = os.path.join(parent_path,'valid')
	create_cats_dogs(path)

	
	# Train, Valid folders within Sample Folder
	path = os.path.join(parent_path,'sample')
	train_valid_folders(path,train_valid_percent_split,1)	
	
	# Cats, Dog folders with train folder of Sample 
	child_path = os.path.join(parent_path,'sample')
	train_path = os.path.join(child_path,'train')
	create_cats_dogs(train_path)

	# Cats, Dog folders with valid folder of Sample
	child_path = os.path.join(parent_path,'sample')
	valid_path = os.path.join(child_path,'valid')
	create_cats_dogs(valid_path)
	
	

if __name__ == '__main__':
	main()
