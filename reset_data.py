import os
import pyfiglet

print(pyfiglet.figlet_format("gate enterance"))

while True:
    answer = input('[?] are you sure want to reset all data? [y/N]')

    if answer not in ['y', 'n', 'Y', 'N', '']:
        continue
    if answer in ['y', 'Y']:
        os.system('del /Q dataset\*')
        os.system('del /Q trainer\*')
        open('names.txt', 'w').write('None')
        print('[+] Data telah direset.')
        break
    break