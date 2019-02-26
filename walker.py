# walker.py - deletes identical files at the top of a directory tree, and progresses down to the lowest copy
# path is the top directory of the operation
# extension is the file ext type to be operated upon. others will be excluded from eradication.
import os
import shutil
import logging
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from send2trash import send2trash

# User settings
path, extension = '', ''

def main(path, extension):
    
    try:
        # Destroy log from any previous operation.
        clear_log()
        # debug.WARN logs the file paths of destroyed files.
        logging.basicConfig(filename='log.txt', level=logging.WARN, format='%(asctime)s - %(levelname)s:\t%(message)s')
        ''' 
        Uncomment for testing. Path, and extension will be set to default values.
        '''
        # path, extension = test_suite() # test suite
        '''
        Primary Operation.
        '''
        total, ext_total = get_file_count(path, extension)
        bottom_up_walk(path, extension, total, ext_total)
        '''
        Destroy all emptry folders and directories.
        '''
        remove_empty_folders(path)
    # General Exception Handling.    
    except Exception as err: logging.error('\n\n\t\t\t[CRITICAL]\n\t\t\t{}\n\n'.format(err)); pass

# Deletes any pre-existing log file, and creates a new one.
def clear_log(): os.remove('log.txt') if os.path.exists('log.txt') else 0

def get_file_count(path, extension):
    print '\n\nRetriving Data Stats...\n'
    count = 0
    ext_count = 0
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(extension): ext_count += 1
            count += 1 
    print '\t\t\t\t\t[TOTAL]: {} files.\n\t\t\t\t\t{} [{}] files.\n'.format(count, ext_count, extension.upper())        
    return count, ext_count

def remove_empty_folders(path):
    # Destroys all empty directories when operation is finished.
    for root, directory, filename in os.walk(path, topdown=False):
        try: os.rmdir(root)
        except: continue
    
def bottom_up_walk(path, extension, total, ext_total):
    '''
    1. Selects a filename matching its correct extension from the bottom of the tree.
    2. Validates that the file exists, and then reads its contents into memory.
    3. Checks the file against every file starting from the top of the tree; except itself.
    '''
    count = 1
    for bottom_up_root, bottom_up_directory, bottom_up_filenames in os.walk(path, topdown=False):
        for bottom_file in bottom_up_filenames: # gets specific file.
            print '\n\nChecking file {} out of {} [TOTAL] files. =========================================== {} [{}] files...'.format(count, total, ext_total, extension.upper())
            if bottom_file.endswith(extension): # checks extension.
                bottom_name = bottom_file
                bottom_file = os.path.join(bottom_up_root, bottom_file) # gets absolute path.
                logging.info('\n\n[FILE] {}\nSearching for identical files...'.format(bottom_file))
                print '\n\n\tChecking for dupilcate files of...\n\t[{}]\n\t\t\t\t\t\tout of {} files total...\n'.format(os.path.basename(bottom_file).upper(), total)
                if os.path.exists(bottom_file): # verifies that the file exists.
                    bottom_file_text = read_(bottom_file) # reads the binary contents of the file.
                    top_down_walk(path, extension, bottom_file, bottom_file_text, total, ext_total, bottom_name) # cross checks the file.
            count += 1

def top_down_walk(path, extension, bottom_file, bottom_file_text, total, ext_total, bottom_name):
    '''
    1. For the bottom file selected: reads each filename matching its correct extension from the top of the tree.
    2. Checks first to make sure that the file being checked is not itself. If it is itself it moves to the next file.
    '''
    count = 1
    for top_down_root, top_down_directory, top_down_filenames in os.walk(path, topdown=True):
        for top_file in top_down_filenames: # gets specific file.
            if count == 1 or count%10000 == 0:
                print '\t\t\t[SEARCHED] {} out of {} files...'.format(count, total)
            count += 1
            if top_file.endswith(extension): # checks extension.
                top_name = top_file
                top_file = os.path.join(top_down_root, top_file) # gets absolute path.
                logging.debug('\n[BOTTOM]:\t{}\n[TOP]:\t\t{}'.format(bottom_file, top_file))
                if bottom_file == top_file: # file is not itself.
                    logging.debug('[TOP FILE IS BOTTOM FILE]')
                    continue
                else:
                    if fuzz.ratio(top_name, bottom_name) > 40:
                        logging.debug('checking for matching content...')
                        if (os.path.getsize(bottom_file) <= os.path.getsize(top_file) + 20000000) and (os.path.getsize(bottom_file) >= os.path.getsize(top_file) - 20000000):
                            process(top_file, bottom_file, bottom_file_text) # read binary content, and delete if identical.
                
def process(top_file, bottom_file, bottom_file_text):
    '''
    1. Reads the file.
    2. If the file has the same contents as the file being checks then it is deleted.
    3. all deletions are logged.
    '''
    if os.path.exists(top_file): # verifies that the file exists.
        name = os.path.basename(top_file)
        top_file_text = read_(top_file) # Read File
        if top_file_text == bottom_file_text: # test binary content for equality.
            send2trash(top_file) # delete file.
            logging.debug('\n\t\t\t[TOP FILE DELETED]\n')
            logging.warn('{}'.format(top_file)) # send record to log file.
            print '\t\t{} \t\t\t...has been [DELETED]'.format(name)
        else: logging.debug('[FAILED TO FIND MATCHING CONTENT]\n')

def read_(filename):
    # Reads the binary contents of a file.
    f = open(filename, 'rb')
    #text = f.read(2500000)
    text = f.read(10000000)
    f.close(); del f
    return text
    
def test_suite():
    '''
    For testing and debugging.
    Creates a directory tree, for testing.
    '''
    logging.debug('Entering test_suite mode...')
    path, extension = '/home/chris/test_tree', 'txt' # set default path.
    if os.path.exists('test_tree'): shutil.rmtree('test_tree') # removes conflicting path.
    os.mkdir('test_tree') # creates parent directory.
    os.chdir('test_tree') # moves os to the parent.
    for i in xrange(1, 11): # makes a first order level of sub directories.
        directory = os.path.join(os.getcwd(), str(i)) # creates sub directory name.
        os.mkdir(directory) # writes the sub directory to disk.
        if not i%2: # creates a second order level of sub directories for half of the sub dirs
            for k in xrange(1, 6):
                sub_dir = os.path.join(os.getcwd(), directory, str(k)) # creates sub directory name.
                os.mkdir(sub_dir) # writes the sub directory to disk.
                for l in xrange(1, 4): # creates text files with various content. In the second order level.
                    f = open('{}.txt'.format(os.path.join(sub_dir, str(l))), 'w')
                    if l%2 == 0: f.write('write something')
                    elif l%3 == 0: f.write('write something else')
                    else: f.write('something else')
                    f.close(); del f
        for j in xrange(1, 6): # creates text files with various content. In the first order level.
            f = open('{}.txt'.format(os.path.join(directory, str(j))), 'w')
            if j%2 == 0: f.write('write something else')
            elif j%3 == 0: f.write('i like tacos and pizza')
            elif j%5 == 0: f.write('write something')
            else: f.write('something else')
            f.close(); del f
    logging.debug('test_tree has been created. Returning to main, and starting walk.')
    return path, extension # pver write user settings with default values in main()
    
if __name__ == '__main__': main(path, extension)
