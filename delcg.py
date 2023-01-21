import os
path = "C://Users//singhala//Downloads//RenameCG"
allfiles = os.listdir(path)
for i in range(len(allfiles)):
    if allfiles[i] == 'renamecg.py' or allfiles[i] == 'delcg.py':
        print("not going to delete this- "+ allfiles[i])
    else:
        os.remove(allfiles[i]) 