import os
path = "C://Users//singhala//Downloads//RenameCG"
allfiles = os.listdir(path)
#print(allfiles[1])
# firstfile = allfiles[1]
# ac_name = firstfile.split('_')
#print(ac_name[1])
#os.rename(allfiles[1],ac_name[1]+'.7z')
#print(range(len(allfiles)-1))

# for i in range(len(allfiles)):
#     if allfiles[i] == 'renamecg.py':
#         print("not going to delete this")
#     else:
#         os.remove(allfiles[i])    


for x in range(len(allfiles)-1):
    firstfile = allfiles[x]
    ac_name = firstfile.split('_')
    os.rename(allfiles[x],ac_name[1]+'.7z')
    print("renamed file "+allfiles[x] +" to "+ac_name[1])

renamed_files = os.listdir(path)
print(renamed_files)