import os
import argparse
import logging
import asyncio
import shutil


async def read_folder(source_folder, target_folder):
    #Read all files and paths
    for root_folder, _, files in os.walk(source_folder):
        #Read every file and start to copy files to new dir
        for file in files:
            source_path = os.path.join(root_folder, file)
            await copy_file(source_path, target_folder)

async def copy_file(source_path, target_folder):
    #Get extension
    _, extension = os.path.splitext(source_path)
    destination_folder = os.path.join(target_folder, extension[1:])
    
    #Make special dir
    os.makedirs(destination_folder, exist_ok=True)
    destination_path = os.path.join(destination_folder, os.path.basename(source_path))

    try:
        await asyncio.to_thread(shutil.copy, source_path, destination_path)
        logging.info(f"Copied {source_path} to {destination_path}")
    except Exception as e:
        logging.error(f"Error copying {source_path}: {e}")

async def main(source_folder, target_folder):
    #Create dir if not exist
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder, exist_ok=True)
        target_folder = os.path.basename(target_folder)
        logging.info(f"Target folder '{target_folder}' created.")

    #Start sorting
    await read_folder(source_folder, target_folder)

# To start enter - > python<version> main.py ./data ./sorted_data OR add them after start - > python<version> main.py 
if __name__ == "__main__":
    logging.basicConfig(filename='files_sorting.log', level=logging.INFO, format='%(asctime)s - !%(levelname)s!: %(message)s')

    parser = argparse.ArgumentParser(description="File sorting script")
    parser.add_argument("source_folder", nargs='?', help="Source folder path")
    parser.add_argument("target_folder", nargs='?', help="Target folder path")
    args = parser.parse_args()

    #Check folders
    while True:
        if not args.source_folder:
            source_folder = input("Please enter the source folder path: ")
        else:
            source_folder = args.source_folder

        if not args.target_folder:
            target_folder = input("Please enter the target folder path (if folder doesn`t exist it will be created): ")
        else:
            target_folder = args.target_folder

        if os.path.isdir(source_folder):
            asyncio.run(main(source_folder, target_folder))
            break
        else:
            print("The source folder do not exist. Please enter valid folder path.")

    
