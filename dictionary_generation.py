import os
from passwords import get_passwords

def associate_files_with_passcodes(directory, passcodes):
    # Get a list of all .crypt files in the directory
    crypt_files = [f for f in os.listdir(directory) if f.endswith('.crypt')]

    # Sort the crypt files numerically based on the number in their names
    crypt_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Create the dictionary associating crypt files with passcodes
    association = []
    for i, passcode in enumerate(passcodes):
        if i < len(crypt_files):
            association.append({"path": os.path.join(directory, crypt_files[i]), "password": passcode})

    return association


def get_dict():
    passcodes = get_passwords()  # Reverse if not already reversed in passwords.py
    # Proceed with your code
    directory = "./"
    result = associate_files_with_passcodes(directory, passcodes)
    return result

print(get_dict())