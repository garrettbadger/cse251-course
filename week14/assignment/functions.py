"""
Course: CSE 251, week 14
File: functions.py
Author: Garett Badger

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1
Try implementing without threads first. 
Once it works then you can add threads and speed it up.
<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
# def depth_fs_pedigree(family_id, tree):
#     # KEEP this function even if you don't implement it
#     # TODO - implement Depth first retrieval
#     # TODO - Printing out people and families that are retrieved from the server will help debugging
#     # take the queue and empty it and make threads for the function to call persons and family
#     # then join them and keep doing that until the queue doesn't have anything in it.
    
        
#     # family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
#     # family.start()
#     # family.join()
#     # family_object = Family(family.get_response())
#     # tree.add_family(family_object)
#     # people_list = family.get_response()
#     def dfs(family, id):
#         if family:
#             response = Request_thread(f'{TOP_API_URL}/family/{id}')
#             response.start()
#             response.join()
#             family_object = Family(response.get_response())
#             tree.add_family(family_object)
#             for i in family_object.get_children():
                
#                 response = Request_thread(f'{TOP_API_URL}/person/{id}')
#                 response.start()
#                 response.join()
#                 person_object = Person(response.get_response())
#                 tree.add_person(person_object)
#                 print(person_object)

#     dfs_thread = threading.Thread(target=dfs, args=(True, family_id,))
#     dfs_thread.start()
#     dfs_thread.join()
#     return tree
#     pass
"""
def depth_fs_pedigree(family_id, tree):
    
    visited = set()

    def dfs(family_id):
        if family_id in visited:
            return
        visited.add(family_id)

        # Request family information from the server
        response = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        response.start()
        response.join()
        if response is not None:
            print(response.get_response())
            family = Family(response.get_response())
            
            tree.add_family(family)

            # Recursively process the children families
            children_families = family.get_children()
            for child_family_id in children_families:
                dfs(child_family_id)

    # Perform multithreaded DFS
    dfs_thread = threading.Thread(target=dfs, args=(family_id,))
    dfs_thread.start()
    dfs_thread.join()

    return tree
"""
def depth_fs_pedigree(family_id, tree):
    req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req.start()
    req.join()

    fam_data = req.get_response()
    print(fam_data)
    reqs = []

   
    
    #get the children
    def dfs(person):
        if person.get_parentid() == None:
            return
        req = Request_thread(f'{TOP_API_URL}/family/{person.get_parentid()}')
        req.start()
        req.join()
        fam_data = req.get_response()
        print(f'Parent ID: {person.get_parentid()}')
        
        # if person.get_parentid() == fam_data['husband_id'] or person.get_parentid() == fam_data['wife_id']:
        #     return
       
        for id in fam_data['children'] + [fam_data['husband_id']] + [fam_data['wife_id']]:
            req = Request_thread(f'{TOP_API_URL}/person/{id}')
            req.start()
            reqs.append(req)
        for req in reqs:
            req.join()
            data = req.get_response()
            person = Person(data)
            tree.add_person(person)
            # print(f'Persons family ID: {person.get_parentid()} fam_data[id]: {fam_data["id"]}')
            if person.get_parentid() != fam_data['husband_id'] and person.get_parentid() != fam_data['wife_id'] and person.get_parentid() != None:
                dfs(person)

        fam = Family(fam_data)
        tree.add_family(fam)

    for id in [fam_data['husband_id']] + [fam_data['wife_id']]:
        req = Request_thread(f'{TOP_API_URL}/person/{id}')
        req.start()
        req.join()
        data = req.get_response()
        person = Person(data)
        dfs(person)
# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass