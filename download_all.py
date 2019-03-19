from argparse import ArgumentParser
import os

# Python 3.0 and later
try:
    from configparser import *

# Python 2.7
except ImportError:
    from ConfigParser import *

# Arguments
def getArguments():
    parser = ArgumentParser(description='Download a movie trailer from Apple or YouTube for all folders in a directory')
    parser.add_argument("-d", "--directory", dest="directory", help="Directory used to find movie titles and years", metavar="DIRECTORY")
    args = parser.parse_args()
    return {
        'directory': args.directory,
    }

# Settings
def getSettings():
    config = ConfigParser()
    config.read(os.path.split(os.path.abspath(__file__))[0]+'/settings.ini')
    return {
        'python_path': config.get('DEFAULT', 'python_path')
    }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = getSettings()

    # Make sure a directory was passed
    if arguments['directory'] != None:

        # Iterate through items in directory
        for item in os.listdir(arguments['directory']):

            # Make sure the item is a directory
            if os.path.isdir(arguments['directory']+'/'+item):

                # Get variables for the download script
                title = item[0:item.rfind('(')].rstrip()
                year = item[item.rindex('(')+1:].split(')')[0].strip()
                directory = arguments['directory']+'/'+item

                # Make sure the trailer has not already been downloaded
                if not os.path.exists(directory+'/'+title+' ('+year+')-trailer.mp4'):

                    # Print current item
                    print(item)

                    # Download trailer for item
                    os.system(settings['python_path']+' '+os.path.split(os.path.abspath(__file__))[0]+'/download.py --title "'+title+'" --year "'+year+'" --directory "'+directory+'"')

    else:

        print('\033[91mERROR:\033[0m you must pass a directory to the script')

# Run
if __name__ == '__main__':
    main()