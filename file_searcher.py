import os
import sys

target = input('Please enter a file for searching: ')
file_found = False
try:
    while True:
        directory = input('Which directory do you want to search: ')
        if not os.path.exists(directory):
            print('Your input directory not in Windows')
        else:
            break

    print("***I'm searching for file, in specified directories***")
    for root, dirs, files in os.walk(directory):
        for file in files:

            if file.startswith(target):
                file_ext = os.path.join(root, file)
                print('File found:', file_ext)
                file_found = True

    if not file_found:
        print('File not found!')
        sys.exit()

except KeyboardInterrupt:
    print('\nProcess forcly stopped by user..')
