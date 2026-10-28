# Lecture 1 practical execution

Mode: solo workspaces executed with Codex assistance.

Remote branch: `practice/run-40618585451-1/main`.

- Activity 1: Create, initialize and associate the remote - passed
- Activity 2: Clone two workspaces, commit and synchronize - passed
- Activity 3: Create feature branches, merge and synchronize HTML files - passed
- Activity 4: Amend, revert, reset and inspect a commit by hash - passed
- Activity 5: Rebase, resolve two real conflicts, integrate and clean local branches - passed

Two real overlapping rebase conflicts were resolved. The commands log includes before/after states and exit codes. No additional collaborators were invited.

```text
*   fa0de0d Activity 5: integrate resolved member 2 feature
|\  
| * 20f4450 Activity 5: edit the shared index heading on a feature branch
|/  
*   db8d2be Activity 5: integrate resolved member 1 feature
|\  
| * 17c4a83 Activity 5: edit the shared member1 paragraph on a feature branch
|/  
* 36dbd42 Activity 5: overlapping main-branch changes to demonstrate conflicts
| * ac5cfca Activity 4: unnecessary commit for reset demonstration
|/  
* b6a10f6 Revert "Activity 4: accidental addition for revert demonstration"
* ff54575 Activity 4: accidental addition for revert demonstration
* 7f195ce Activity 4: correct title and add missing description
| * 7e96a46 Activity 4: title update before amendment
|/  
*   7b3f131 Activity 3: merge member 2 feature
|\  
| * 811641a Activity 3: add simulated member 2 feature
|/  
*   b755ed2 Activity 3: merge member 1 feature
|\  
| * 61def8a Activity 3: add simulated member 1 feature
|/  
*   93f1d75 Activity 3: merge leader feature
|\  
| * 40c657c Activity 3: add leader HTML feature
|/  
* 392a34a Activity 2: commit from simulated member 2 workspace
* 64a672d Activity 2: commit from simulated member 1 workspace
* 517b08c Activity 1: initialize solo practice repository
* be9d663 Add Codex-assisted solo Git and workflow practical activities
* 1fc23f6 Initial commit
```
