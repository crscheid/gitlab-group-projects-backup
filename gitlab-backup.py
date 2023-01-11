# Gitlab Group Project Backup
#
# This python script downloads all of the repositories from a particular
# group into a /data directory. Note that for ease of use it will use the full
# paths of the repositories for the naming convention.
#
# This script also unpacks projects within subgroups.

import requests
import shutil

from os import environ

gitlab_token = environ['GITLAB_TOKEN']
group_id = environ['GITLAB_GROUP_ID']

backup_archive = False
if 'BACKUP_ARCHIVED' in environ:
    if environ['BACKUP_ARCHIVED'] == 'yes':
        backup_archive = True


def get_subgroups_for_group_id(group_id: int):

    print(f"Checking group: {group_id}")

    # Add itself to the group list
    group_list = [group_id]

    r = requests.get(url=f'https://gitlab.com/api/v4/groups/{group_id}/subgroups', headers={"Private-Token":gitlab_token})
    group_data = r.json()

    if len(group_data) > 0:
        print(f"  Retrieved {len(group_data)} subgroups for group id: {group_id}")

        for group_item in group_data:
            sub_group_list = get_subgroups_for_group_id(group_item['id'])
            group_list = group_list + sub_group_list

    return group_list

# Use this to track all groups
allGroups = get_subgroups_for_group_id(group_id)

print(f"Retrieved {len(allGroups)} groups: {allGroups}")

for group_id in allGroups:

    print(f"Processing group id: {group_id}")

    r = requests.get(url=f'https://gitlab.com/api/v4/groups/{group_id}/projects', headers={"Private-Token":gitlab_token})
    data = r.json()

    for item in data:
        if item['archived'] and not backup_archive:
            print(f"  ProjectID: {item['id']} Name: {item['path_with_namespace']} - Skipping Archive")
        else:
            local_filename = '/data/' + item['path_with_namespace'].replace('/','-') + ".zip"
            print(f"  ProjectID: {item['id']} Name: {item['path_with_namespace']} - Downloading to {local_filename}")

            url = f"https://gitlab.com/api/v4/projects/{item['id']}/repository/archive.zip"

            with requests.get(url, stream=True, headers={"Private-Token":gitlab_token}) as r:
                with open(local_filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
