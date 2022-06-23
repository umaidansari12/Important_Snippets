## Git Commands
```
git checkout .
Usage : If you have'nt staged file for local changes and you want to remove those changes and just pull the latest from remote repository 
```

```
git stash
Usage : stores all the local recent changes and resets the state to prior commit state
```

```
git stash pop
Usage : to retrieve all the files that are put into stash 
Takes the files in a stash, places them back into the development workspace and deletes the stash from history;
```

```
git stash apply 
Usage : Takes the files in a stash and places them back into the development workspace, but does not delete the stash from history;
```

```
git remote -v
show remote url name
```

```
git remote add upstream git@github.com:VahanInc/Data-Engineering.git
```

```
git clone git@github.com:umaidansari12/Data-Engineering.git
```

```
git status
```

```
git push --set-upstream origin feature/DATA-159/staffing_s3_file_url
```

```
git push -u origin feature/DATA-159/staffing_s3_file_url
```

```
git branch
```

```
Cmd 1 : git checkout filename ( files changes revert to last commit )
For all files : git checkout -f

Cmd 2: git log (what commits you have written)
For seeing specific no. of commit info : git log -p -no.ofcommits

Cmd 3: git diff (compares working tree with staging area)

Cmd 4: git diff --staged   (compares staging area with last commit)
Cmd 5: git commit -a -m “msg” (skip staging area and direct commit the changes)

Cmd 6: git rm –cached filename ( remove file  from git tracking tree)
Cmd 7: git rm filename (remove file from hard disk)
Cmd 8: git status -s (tells small status for working tree)
Cmd 9 : git branch branchName ( create branch)
Cmd 10: git branch (shows total branches and currently we are where)
Cmd 11: git checkout branchName ( switched to this branch)
Cmd 12: git checkout master (switched to master branch)
Cmd 13: git merge branchName ( when you are in master branch then you can use it to merge your branch with master)
Cmd 14: git checkout -b branchName ( branch is created and switched to this branch)
```