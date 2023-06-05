# Beach Volleyball Stats Generator
This script takes in a text file of beach vb raw player actions and generates stats.

## Example input/output

Example input can be seen in the `.txt` file but it looks like this:
```
N 1jfs A 3p T 3s A 1sl
T 1jfs N 3p S 3s N 1kl
S 2.5jfs T 0.5p N 1b
S 1jfs T 3p A 3s T 0hda S 0.5d A 3p T 3p A 1hda
```

Here is an example output that it gives:
```
{'A': {'attack': ['0', '0', '0', '1'],
       'block': [],
       'dig': ['3', '2'],
       'pass': ['3', '3', '3', '3', '3', '2', '3', '2', '2'],
       'serve': ['1', '2', '1', '1', '4', '1', '2'],
       'set': ['3', '3', '2', '3', '3'],
       'sideout': []},
 'N': {'attack': ['0', '0', '1'],
       'block': [],
       'dig': ['1', '2', '2'],
       'pass': ['3', '1', '3', '3', '2', '2', '1'],
       'serve': ['1', '1', '1', '1'],
       'set': ['3', '3', '2', '2', '3', '3', '3'],
       'sideout': []},
 'S': {'attack': ['0', '0'],
       'block': [],
       'dig': ['3', '3'],
       'pass': ['3', '3', '2', '2', '2', '3', '3'],
       'serve': ['1', '4', '1', '1'],
       'set': ['3', '1', '3', '3', '2', '3', '3', '3', '2'],
       'sideout': []},
 'T': {'attack': ['0', '0', '0'],
       'block': [],
       'dig': ['1'],
       'pass': ['3', '3', '3', '3', '2', '2', '3'],
       'serve': ['1', '1', '4', '4'],
       'set': ['3', '3', '3', '3', '3', '2', '3', '3', '2', '2'],
       'sideout': []}}
```

## Running instructions
In a terminal:
1. First clone the repo
```
git clone git@github.com:nholaday/bvb_stats.git
```

Change directory into the the project, then run by supplying the file name as an argument
``` 
python bvbstats.py 05-04-23-stats.txt
```
