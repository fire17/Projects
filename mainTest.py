import Funcs as F


p = ["Projects Management"]

#F.Overwrite(p)

F.AddProject("Test Project")
F.AddProject()

for pr in p:
    F.AddProject(pr)
