# CodeForces_Scripts

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
