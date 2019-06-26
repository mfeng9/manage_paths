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
