# Instructions:

## purpose: maintain PYTHONPATH and PATH to allow 
switching between anaconda and ROS python environment
This is to resolve the incompatibility between anaconda and ROS

## Set up

modify the file paths as needed (including the paths below and paths inside the bash & python files)

### add the following to the bashrc file

```bash
alias release_conda='source /home/username/apps/manage_path/release_conda.sh'
alias cage_conda='source /home/username/apps/manage_path/cage_conda.sh'
alias backup_path='source /home/username/apps/manage_path/backup_path.sh'
```
### add this line to the very end of the bashrc file
```bash
source /home/username/apps/manage_path/backup_path.sh
```
## Note
backup_paths.txt is regenerated every time bashrc is sourced 
e.g. opening new terminal/terminal tabs
