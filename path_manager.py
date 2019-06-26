"""
Instructions:

purpose: maintain PYTHONPATH and PATH to allow 
switching between anaconda and ROS python environment
This is to resolve the incompatibility between anaconda and ROS


modify file path as needed

# add the following to the bashrc file
alias release_conda='source /home/username/apps/manage_path/release_conda.sh'
alias cage_conda='source /home/username/apps/manage_path/cage_conda.sh'
alias backup_path='source /home/username/apps/manage_path/backup_path.sh'

# add this line to the very end of the bashrc file
source /home/username/apps/manage_path/backup_path.sh


backup_paths.txt is regenerated every time bashrc is sourced 
e.g. opening new terminal/terminal tabs
"""

import os
import sys


### conda does not mess with PYTHONPATH, it hard links everything with PATH env variable
conda_path = '/media/username/DATA1/apps/anaconda3/bin'
ros_path = '/opt/ros/kinetic/bin'
source_bash_path = '/home/username/apps/manage_path/source_paths.sh'
backup_paths = '/home/username/apps/manage_path/backup_paths.txt'
bashrc_path = '/home/username/.bashrc'
bashrc_copy = '/home/username/apps/manage_path/bashrc_copy'

# by default, the path of the itself is added to the beginning of the pythonpath
self_path = '/home/username/apps/manage_path' 

bash_cmds = []

def merge2syspath(pythonpath):
    syspath = sys.path
    for pypath in pythonpath:
        if not (pypath in pythonpath):
            syspath.append(pypath)
    return syspath

def filter_pythonpath(pythonpath, version, invert=False):
    filtered = []
    for path in pythonpath:
        if version in path:
            if not invert:
                filtered.append(path)
        elif invert:
            filtered.append(path)
    return filtered

def get_pythonpath():
    """
    return pythonpath: a list of string
    """
    lines = None
    with open(bashrc_path, 'r') as f:
        lines = f.readlines()

    pythonpath = [] 
    for line in lines:
        if "export PYTHONPATH" in line:
            tmp = extract_path_from_bashrc(line)
            for each_path in tmp:
                if each_path != '':
                    pythonpath.append(each_path)
    return merge2syspath(pythonpath)

def read_pythonpath_from_backup():
    lines = None
    with open(backup_paths, 'r') as f:
        lines = f.readlines()

    pythonpath = [] 
    for line in lines:
        if "export PYTHONPATH" in line:
            tmp = extract_path_from_bashrc(line)
            for each_path in tmp:
                if each_path != '':
                    pythonpath.append(each_path)
    return pythonpath

def extract_path_from_bashrc(bashrc_line):
    ## remove all comments from the bash line
    ## get the position of the first #
    comment_pos = bashrc_line.find('#')
    bashrc_line = bashrc_line[:comment_pos]
    # if len(bashrc_line):
    #     return None
    pypath = bashrc_line.replace('export PYTHONPATH=', '')
    pypath = pypath.replace('${PYTHONPATH}', '')
    pypath = pypath.replace('$PYTHONPATH', '')
    pypath = pypath.replace("\n", "")

    # pypath = pypath.replace(":", "")
    pypath = pypath.split(':')
    return pypath

def export_pythonpath(pythonpath):
    """
    pythonpath: a list of string
    """
    cmd = "export PYTHONPATH="
    for path in pythonpath:
        cmd += path
        cmd += ':'
    cmd = cmd[:-1] # remove the last :
#    print(cmd)
    os.system(cmd)
    
def update_pythonpath_bash(pythonpath):
    """
    pythonpath: a list of string
    """
    cmd = "export PYTHONPATH="
    for path in pythonpath:
        if not (self_path in path):
            cmd += path
            cmd += ':'
    cmd = cmd[:-1] # remove the last :
    bash_cmds.append(cmd)

def finish_bash(filename):
    with open(filename, 'w+') as f:
        for cmd in bash_cmds:
            f.write(cmd + '\n')

def has_conda_on():
    sys_path = os.environ['PATH']
    ros_idx = sys_path.find('/opt/ros/kinetic/bin')
    conda_idx = sys_path.find(conda_path)
    if conda_idx != -1 and conda_idx < ros_idx:
        return True
    return False

def prepend_conda_path():
    if has_conda_on():
        print('Conda already activated')
    else:
        sys_path = os.environ['PATH']
        # remove the conda path
        sys_path = sys_path.replace(conda_path, '')
        sys_path = sys_path.replace('::', ':')
        # put the conda path to the beginning of path
        sys_path = conda_path + ':' + sys_path
        sys_path = sys_path.replace('::', ':')
        bash_cmds.append('export PATH={}'.format(sys_path))

def append_conda_path():
    if not ( has_conda_on() ):
        print('Conda already deactivated')
    else:
        sys_path = os.environ['PATH']
        # remove the conda path
        sys_path = sys_path.replace(conda_path, '')
        sys_path = sys_path.replace('::', ':')
        # put the conda path to the end of path
        sys_path = sys_path + ':' + conda_path
        sys_path = sys_path.replace('::', ':')
        bash_cmds.append('export PATH={}'.format(sys_path))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="either 'release' or 'cage' to activate or deactivate conda from ROS")
args = parser.parse_args()

if args.mode == 'release':
    pythonpath = read_pythonpath_from_backup()
    print('releasing anaconda from cage')
    ### activate python3 anaconda
    update_pythonpath_bash(filter_pythonpath(pythonpath, '2.7', invert=True))
    prepend_conda_path()
    finish_bash(source_bash_path)
elif args.mode == 'cage':
    pythonpath = read_pythonpath_from_backup()
    print('locking anaconda to cage')
    ## deactivate python3 anaconda
    update_pythonpath_bash(filter_pythonpath(pythonpath, '2.7', invert=False))
    append_conda_path()
    finish_bash(source_bash_path)
elif args.mode == 'backup':
    # print('backing up PYTHONPATH to \n {}'.format(backup_paths))
    ### backup PYTHONPATH
    pythonpath = get_pythonpath()
    update_pythonpath_bash(pythonpath)
    finish_bash(backup_paths)
else:
    print('nothing performed')