import subprocess;

command = 'npm --version && pip --version';
process = subprocess.Popen('start cmd /k' + command, shell=True, stdout=subprocess.PIPE)