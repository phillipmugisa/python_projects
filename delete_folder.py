import os
import sys

def get_directory_path():
	try:
		return sys.argv[1]
	except Exception as err:
		raise("No directory path passed")
		sys.exit()

def delete_directory_files(directory):
	# move to directory location
	os.chdir(directory)

	print('Files in this directory')
	if os.listdir(directory):
		for file in os.listdir(directory):
			os.remove(file)
			print("{0} -- DELETED".format(file))
	else:
		print('no contents')

def delete_directory(directory):
	try:
		#directories = directory.split('/') or directory.split(r"\\")
		#get current directory name
		#directory_name = directories[-1]
		
		# get parent directory path
		#parent_directory = directory.replace('/'+directory_name, '')
		# move to parent directory
		#os.chdir(parent_directory)

		# delete directory
		os.rmdir(directory)
		
	except Exception as err:
		print(err)
		sys.exit()	

def main():
	directory_path = get_directory_path()
	delete_directory_files(directory_path)	
	delete_directory(directory_path)


if __name__ == '__main__':
	main()