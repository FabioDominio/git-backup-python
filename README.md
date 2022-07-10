# Git backup

This utility automates the backup of several git repositories from a selected git server.

For the moment, the utility can only backup all the Gitlab repositories the user is enabled to, providing a valid API *private token*.

## Installation

After cloning  or downloading the repository, install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
py git_backup.py TOKEN [DESTINATION]
```

with TOKEN the user's Gitlab API private token, and DESTINATION the *optional* destination folder path for the saved repositories. If not specified, the destination defaults to the current work directory.

## How it works

The utility is based on the request module to retrieve the user's groups and projects (respectively namespaces and repositories) by means of REST calls to the Gitlab v4 API, and on [GitPython](https://gitpython.readthedocs.io) to clone the retrieved repository urls into the selected destination folder.

Each repository is cloned both in *mirror* mode, to be restored completely in case of emergency or imported to another account or git server, and in the "normal" mode (the default git clone command) .

In both cases, the clone repositories are zipped and dated, and the temporary files deleted to save space.

The folder tree is the following:

DESTINATION

​			|---> GROUP_NAME_1

​								|--->GROUP_1_REPOSITORY_1_NAME

​																	|--->REPOSITORY_1_NAME_src_YYYYMMDD.zip  

​																	|--->REPOSITORY_1_NAME_repo_YYYYMMDD.zip