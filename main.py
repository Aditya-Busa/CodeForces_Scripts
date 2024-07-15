'''
Instructions : 

1.  Problem Rating limits can be set (Default 800-1400)
2.  You can set the lower_limit and upper_limit for no_of_people solved the question, by default it is 3500 to 20000, it is a good range for 800-1400 rated questions(the default rating limits)
3.  contestIds are what you see in the URL of the problem, You can set upper_limit and lower_limit for it, so that you can choose recent/old problems
    BY DEFAULT it is set to [0,1e9] , it just takes all contests
4.  It is irritating to find solved questions again in problemset, so you can put your
    CF user_handle below, you will get only unsolved questions now :) , this way, you can keep regenerating the list and you will have new unsolved problems
    If you still want solved problems also to appear in your problemset, toggle the 'do_you_want_only_unsolved' boolean variable to False
5.  Tags work in an OR fashion by-default, i.e. if a problem has any one of the tag you've mentioned, it will be selected into the problemset.
    If you want them to work in an AND fashion, toggle the tag_AND boolean variable to True
6.  While printing the problemset, tags are printed by default, if you wanted to hide the tags, then toggle the Hide_Tags to True
7.  The output is by-default sorted by contestId descending order, if you want it to be sorted according to rating,solved_count you can change the integer 'Sort_By' 
    Sort_By = 0 DEFAULT (descending by contestId)
    Sort_By = 1 ascending by rating
    Sort_By = -1 descending by rating
    Sort_By = 2 ascending by solved_count
    Sort_By = -2 descending by solved_count
    
How to run : 
    1. python3 main.py (If you don't have required libraries, error will pop up, do download them using 'pip3 install <library_name>')
    2. You will be asked for number of tags you want to enter
    3. Now you have to enter all the IDs of the tags you want to include, the list is available for your reference at the end of this code
    4. DONE, A problems.txt file will be created, check that.

'''

# [PARAMETERS TO CHANGE ARE GIVEN BELOW]
contest_id_lower_limit, contest_id_upper_limit = 0, 1000000000
rating_lower_limit, rating_upper_limit = 1100, 1600
no_of_AC_lower_limit, no_of_AC_upper_limit = 1500, 20000
user_handle = '_aditya_b'
do_you_want_only_unsolved = True
tag_AND = False
Hide_Tags = False
Sort_By = 1
# [PARAMETERS TO CHANGE ARE GIVEN ABOVE]


import requests as rq
import time

tagset = set()
solved_set = set()

def check_id_range(id_string):
    id_val = int(id_string)
    if id_val >= contest_id_lower_limit and id_val <= contest_id_upper_limit : return True
    return False

def check_rating_range(rating_string):
    rating_val = int(rating_string)
    if rating_val >= rating_lower_limit and rating_val <= rating_upper_limit : return True
    return False

def check_AC_range(solved_count_string):
    solved_count_val = int(solved_count_string)
    if solved_count_val >= no_of_AC_lower_limit and solved_count_val <= no_of_AC_upper_limit : return True
    return False

def get_solved():
    if not do_you_want_only_unsolved : return
    url = f"https://codeforces.com/api/user.status?handle={user_handle}"
    rs = rq.get(url)
    submissions = rs.json()["result"]
    
    for sub in submissions:
        if 'contestId' in sub and 'problem' in sub and 'index' in sub['problem'] and 'type' in sub['problem'] :
            contestId = sub['contestId']
            if not check_id_range(contestId) : continue
            problemId = sub['problem']['index']
            if sub['problem']['type'] != 'PROGRAMMING' : continue
            if 'verdict' in sub and sub['verdict'] == 'OK': solved_set.add(f'{contestId}{problemId}')

def check_unsolved(contestId, index):
    if not do_you_want_only_unsolved : return True
    problem_string = str(contestId) + str(index)
    if problem_string in solved_set : return False
    return True

def get_problem_url(contestId, index):
    url = f'https://codeforces.com/contest/{contestId}/problem/{index}'
    return url

def generate_problem_list():
    rs = rq.get('https://codeforces.com/api/problemset.problems')
    
    all_problems = rs.json()['result']['problems'] 
    all_problem_statistics = rs.json()['result']['problemStatistics']
    problem_list = []

    for problem,problem_stat in zip(all_problems,all_problem_statistics):
        if problem['type'] != "PROGRAMMING" : continue
        if "rating" in problem and "tags" in problem and "contestId" in problem and "index" in problem and check_rating_range(problem['rating']) and check_id_range(problem['contestId']) and check_AC_range(problem_stat['solvedCount']):
            taglist = problem['tags']
            if not check_unsolved(problem['contestId'], problem['index']): continue
            cnt = 0
            for tag in taglist : 
                if tag in tagset: 
                    cnt += 1
            minimum = 1
            if tag_AND : minimum = len(tagset)
            if cnt >= minimum : problem_list.append([get_problem_url(problem['contestId'], problem['index']), problem['rating'],problem_stat['solvedCount'],taglist])

    return problem_list

if __name__ == '__main__':


    ntags = int(input("How many tags do you want to add : "))
    all_tags = ["2-sat", "binary search", "bitmasks", "brute force", "chinese remainder theorem", "combinatorics", "constructive algorithms", "data structures", "dfs and similar", "divide and conquer", "dp", "dsu", "expression parsing", "fft", "flows", "games", "geometry", "graph matchings", "graphs", "greedy", "hashing", "implementation", "interactive", "math", "matrices", "meet-in-the-middle", "number theory", "probabilities", "schedules", "shortest paths", "sortings", "string suffix structures", "strings", "ternary search", "trees", "two pointers"]
    while ntags <= 0 : 
        print("ntags can't be <= 0")
        ntags = int(input("How many tags do you want to add : "))
    
    for i in range(ntags):
        tag_i = int(input(f'Enter tag ID {i+1} : ')) # SEE BELOW FOR TAG ID
        while tag_i > 35 or tag_i < 0:
            print("Invalid tag_i")
            tag_i = int(input(f'Enter tag ID {i+1} : ')) 
        print(f"You've selected {all_tags[tag_i]}")
        tagset.add(all_tags[tag_i])
    
    time.sleep(1)
    
    print("Problem List Generation has started...")
    get_solved()
    print("Created set of all your accepted submissions :)")
    
    problem_list = generate_problem_list()
    serial_no = 1
    file_path = 'problems.txt'
    
    if Sort_By != 0 : problem_list = sorted(problem_list,key=lambda item : int(Sort_By)* item[abs(Sort_By)])
    
    with open(file_path, 'w') as file:
        for problem in  problem_list:
            if Hide_Tags : file.write(f"{serial_no}. {problem[0]} RATING : {problem[1]} SolvedCount : {problem[2]} tags : You told to Hide Them\n")
            else : file.write(f"{serial_no}. {problem[0]} RATING : {problem[1]} SolvedCount : {problem[2]} tags : {problem[3]}\n")
            serial_no += 1
    
    print("Problem List Generation has finished, check problems.txt")

'''
    0 : 2-sat 
    1 : binary search
    2 : bitmasks
    3 : brute force
    4 : chinese remainder theorem
    5 : combinatorics
    6 : constructive algorithms
    7 : data structures
    8 : dfs and similar
    9 : divide and conquer
    10 : dp
    11 : dsu
    12 : expression parsing
    13 : fft
    14 : flows
    15 : games
    16 : geometry
    17 : graph matchings
    18 : graphs
    19 : greedy
    20 : hashing
    21 : implementation
    22 : interactive
    23 : math
    24 : matrices
    25 : meet-in-the-middle
    26 : number theory
    27 : probabilities
    28 : schedules
    29 : shortest paths
    30 : sortings
    31 : string suffix structures
    32 : strings
    33 : ternary search
    34 : trees
    35 : two pointers
'''