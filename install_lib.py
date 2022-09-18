import subprocess
with open('list_.txt','r') as file:
    lines=file.readlines()
# cmd=subprocess.Popen("pip list",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read().decode()
# print(cmd)
for line in lines:
    line=line.strip()
    index=line.index('=')
    line=line[:index]
    cmd=subprocess.Popen("pip install "+line,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    cmd=cmd.stdout.read().decode()+cmd.stderr.read().decode()
    print(cmd)