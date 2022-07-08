#process 1

import subprocess,os

p = subprocess.Popen(["scp", "my_file.txt", "192.168.1.5:F:\Secure-File-Uploader_tkinter"])
sts = os.waitpid(p.pid, 0)


# process 2 - using ssh install scp

# from paramiko import SSHClient
# from SCP import SCPClient 
# ssh = SSHClient()
# ssh.load_system_host_keys()
# ssh.connect('user@server:path')
# with SCPClient(ssh.get_transport()) as scp:
#     scp.put('my_file.txt', 'my_file.txt') # Copy my_file.txt to the server

# or
# import os
# import paramiko

# ssh = paramiko.SSHClient() 
# ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
# ssh.connect(server, username=username, password=password)
# sftp = ssh.open_sftp()
# sftp.put(localpath, remotepath)
# sftp.close()
# ssh.close()

