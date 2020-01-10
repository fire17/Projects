FN = "D:\\Projects\\projects.txt"
def OpenProjects():
    ps = OpenFile()
    pp = []
    for s in ps:
        pp.append(s.split("\n")[0])
    return pp

def OpenFile(filename = None):
    global FN
    if filename is None:
        f = FN
    else:
        f = filename
    f = open(f,"r")
    fl = f.readlines()
    #print("@@@@@@@@@")
    #print(fl)
    #print("@@@@@@@@@")
    f.close()

    return fl

def Overwrite(lines, filename = None):
    global FN
    if filename is None:
        f = FN
    else:
        f = filename
    f = open(f,"w+")
    f.writelines(lines)
    f.close()

def AddProject(ProjectName = "New Project"):
    projects = OpenProjects()
    print("!")
    print(projects)
    print("!")
    projects.append(ProjectName+"\n")
    print(projects)
    Overwrite(projects)
