<!-- ABOUT THE PROJECT -->
## About

This is a script used to group and sort files based on the time they were added. Files created in a similar time, such as files that were scrapped from the internet, should have similar modified timestamps on them. This can be used to group them based on when the script was used to scrap those files.

### What does it really do?

It looks at the modified timestamp date of all the files, then groups the files that were all created within a desired (default: 120) second(s) interval.

Example:
```
Group 1:
File A - Modified Date: 1
File B - Modified Date: 121
File C - Modified Date: 241
File D - Modified Date: 361

Group 2:
File E - Modified Date: 400
```

Files A,B,C,D were in one group, because there is atleast one of them within 120 seconds within each other.
File E is not, so is therefore left out.


## Installation

### Prerequisites

* Python 3

#### Install via PIP

```
pip install git+https://github.com/shalebark/group_closesly_created_files.git
```

* This should install it in your python bin path as `group-close-files`

```
which group-close-files
```

## Usage

### CLI
```
group-close-files [OPTIONS] SRC_DIRECTORY DST_DIRECTORY
```

### FLAGS

| Short      | Long |       Description
| ----------- | ----------- | ----------- |
| -d | --time-difference | Number of seconds between the files. Default: 120  |
| -m   | --method  | Copy/Move. To copy or move the files. Default: copy |
| -n   | --min-group-size  | Minimal Size to count as a group. Default: 1 |

* If n is greater than 1, groups that are smaller than the minimal group size will not show in the output.

### Sample Output

```
1970-01-01_00:03:20:::2
1970-01-01_00:08:50:::1
1970-01-01_00:06:40:::1
1970-01-01_00:10:51:::1
```

Output is in YYYY-MM-DD_HH:mm:ss:::${number-of-files-in-group} notation.

The timestamp used is the oldest timestamp of the group.


