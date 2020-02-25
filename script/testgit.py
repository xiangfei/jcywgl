#coding=utf-8

import gitlab


gl = gitlab.Gitlab('http://git.jc', private_token='fFZjxzWn-osXh3PHzRBs', api_version='4')

projects = gl.projects.list()

# for project in projects:
#     print(project)

groups = gl.groups.list(all=True)
print(len(groups))

for group in groups:
    print(group.id, group.name)

#group = gl.groups.create({'name': 'group1', 'path': 'group1'})



print(group)
