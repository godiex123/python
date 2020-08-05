import sys
# print(objectInto([1, 2, 3, 4, 6, 7]))


# def thesame(array, c=0, i=0, obj={}):
#     i = len(array) - 1
#     while c < len(array):
#         if c == 0:
#             obj = {'value': array[i]}
#             c, i = c+1, i-1
#             thesame(array, c, i, obj)
#         else:
#             obj = {'value': array[i], 'rest': obj}
#             c, i = c+1, i-1
#             thesame(array, c, i, obj)
#     return obj


# print(thesame(["uno", "dos", "tres", "cuatro"]))

# text = sys.argv[1]

# def isPhoneNumber(text):
#     if len(text) != 12:
#         return False
#     for i in range(0, 3):
#         if not text[i].isdecimal():
#             return False
#     if text[3] != '-':
#         return False
#     for i in range(4, 7):
#         if not text[i].isdecimal():
#             return False
#     if text[7] != '-':
#         return False
#     for i in range(8, 12):
#         if not text[i].isdecimal():
#             return False
#     return True


# for i in range(len(text)):
#     chunck = text[i:i+12]
#     if isPhoneNumber(chunck):
#         print('Phone number found: ' + chunck)
# print('Done')


import pyperclip
import re


text = str(pyperclip.paste())

phoneRegex = re.compile(r'''( 
        (\+\d{0,}?|\d{0,}?)                 # area code
        (\s|-|\.)?                      # separator
        (\d{0,}(\s|-|\.)?\d{3}(\s|-|\.)?\d{4})
)''', re.VERBOSE)

emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+           # username
    @                           # symbol
    [a-zA-Z0-9.-]+              # domain name
    (\.[a-zA-Z]{2,4})           # dot-something
)''', re.VERBOSE)

matches = []
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1], groups[3]])#, groups[5], groups[6]])
    matches.append(phoneNum)
for groups in emailRegex.findall(text):
    matches.append(groups[0])

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard: ')
    print('\n'.join(matches))
else:
    print('No phone numbers or email addresses found')
    

    