# importing required libraries
import os
from pathlib import Path
import shutil
import csv
import time 
import logging

logging.basicConfig(level=logging.INFO, filename='Log Data.log',filemode='w',format="%(asctime)s -- %(levelname)s -- %(message)s")

class FileManagementApp:

    def __init__(self,base_path: str):
        # setting the instance variable base_path
        self.base_path = base_path
    

    def move_and_rename(self,file_name: str, file_dir_path: str, destination_path: str) -> None:
        """ 
        This function will move the file to destination_path 
        
        file_name : name of the file that is to be moved
        file_dir_path : path of the directory in which file is present
        destination_path : path of the directory where the file is to be transfered 

        """

        # creating the path of the file if it is present inside the destination directory
        target_file_path = f"{destination_path}\{file_name}"

        # current path of the file
        file_path = f"{file_dir_path}\{file_name}"

        # counter variable to count the number of files with same name
        counter = 1

        # checking if the file already exists in the destination_path or not
        # to handle multiple files with same name 
        while os.path.exists(target_file_path):
            # concatenating counter variable at the end of the file_name 
            new_file_name = f"{Path(file_path).stem} ({counter}){Path(file_path).suffix}"

            # updating the target_file_path with the new file name
            target_file_path = f"{destination_path}\{new_file_name}" 

            # updating counter variable
            counter = counter + 1
        
        # if there are files with same name in the destination path
        if counter!=1:
            # changing the name of the file with the new file name
            os.rename(f"{file_dir_path}\{file_name}",f"{file_dir_path}\{new_file_name}")
            # moving the file from current path to destinaion path
            shutil.move(f"{file_dir_path}\{new_file_name}",destination_path)
        # if there are no files with same name in the destination path
        else:
            shutil.move(file_path ,destination_path)
 

    def file_consolidate(self) -> None:
        """This method will consolidate all the files into a single target folder and track specific details about each file in a CSV file"""

        # path of files that are going to be stored in different Output Folders
        details_file_path = 'Result\Detail\Details.csv'
        performance_file_path = 'Result\Performance\Performance.csv'
        log_file_path = 'Result\Log Data'
        new_file_location = f"{os.getcwd()}\Result\Target Folder"


        # opening the 'Details.csv' file to store the data of files
        with open(details_file_path,'a',newline='') as f1:
            logging.info('Creating the Details.csv file....')
            # creating an object of the CSV file to write data into it
            csv_writer = csv.writer(f1)
            # writing the headers of the CSV file 
            csv_writer.writerow(['File Name','File Format','File Size','Current Location','New Location'])

            # making variables to store the time taken for each processing step
            time_detail_extraction =0
            time_csv_creation =0 
            time_moving_files = 0

            # iterating through the files and directories present inside the provided path
            for dirpath,dirnames,files in os.walk(self.base_path):
                logging.debug(f'Entered into {dirpath}')

                # iterating through files present inside the given directory or in its subdirectory
                for file in files:
                    # path of the file 
                    cur_file_path = f"{dirpath}\{file}"
                    logging.debug(f'Dealing with {file}')

                    x= time.time()
                    # extracting the name and format of the file
                    Fname,Fformat = Path(cur_file_path).stem,Path(cur_file_path).suffix
                    # calculating the size of the file in KBs
                    Fsize = round(os.path.getsize(cur_file_path)/1024,2)
                    # adding the time taken in detail extraction of each file
                    time_detail_extraction = time_detail_extraction + (time.time()-x)

                      
                    # writing the extracted data into the CSV file
                    x = time.time()  
                    csv_writer.writerow([Fname,Fformat,Fsize,dirpath,new_file_location])
                    # adding the time taken in adding data into the CSV file of each file
                    time_csv_creation = time_csv_creation + (time.time()-x)
                    
                    x = time.time()
                    # moving file to the destination directory
                    self.move_and_rename(file,dirpath,new_file_location)
                    time_moving_files = time_moving_files + (time.time()-x)

            logging.info('Details.csv file created!')
            logging.debug(f'Time Taken for moving all the files is: {time_moving_files}')
            logging.debug(f'Time taken in creating the CSV file is: {time_csv_creation}')            
            logging.debug(f'Time taken in extracting the details of the files is: {time_detail_extraction}')
        
        with open(performance_file_path,'a',newline='') as f2:
            logging.info('Creating Performance.csv file .....')
            # making an object of Performance.csv file to write the data into it
            csv_writer = csv.writer(f2)
            # storing the information 
            csv_writer.writerow(['Moving Files','Extracting Details','CSV Creating'])
            csv_writer.writerow([time_moving_files,time_detail_extraction,time_csv_creation])
            logging.info('Performance.csv file Created!')
    
    


if __name__ == "__main__": 
    # takes the input of the directory path
    # base_path = input('Enter the Directory path: ')

    base_path = r"C:\Users\DARPAN\Downloads\My_directory"
    logging.debug(f'Entered path is {base_path}')

    try:
        # checking if the given path exists or not
        if os.path.exists(base_path):
            logging.info('provided path is valid!')

            # path of the directory where all the ouptut folders will be there
            result_directory = 'Result\\'
            
            # name of the output folders
            subdirectories = ['Target Folder','Detail','Performance','Log Data']

            # iterating through each of the output folders to create them
            logging.info('Creating Output Folders.....')
            for subdirectory in subdirectories:
                # making an 'WindowsPath' object
                path = Path(result_directory + subdirectory)
                # creating the output directories in the result_directory
                path.mkdir(parents=True)
            logging.info('Output Folders Created!')

            # building an instance of the FileManagementApp 
            app = FileManagementApp(base_path)
            # calling the file_consolidate method to perform the desired task
            logging.info('File Consolidation Task Started.....')
            app.file_consolidate()
            logging.info('File Consolidation Task Done !')
            
        # If the provided path does not exist,
        # we raise an exception.
        else:
            logging.error("User has entered invalid path!",exc_info=True)
            raise Exception("Provided path is not valid")

    except Exception as e:
        # printing the message of the exception
        print(e)