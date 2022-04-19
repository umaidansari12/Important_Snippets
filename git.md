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