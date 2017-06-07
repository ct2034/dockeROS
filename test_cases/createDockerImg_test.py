import subprocess
import docker
import os
import shutil

def createDockerImg(image, ip,port, rospackage):

    ip_str = "tcp://" + ip + ":" + port
    #cli = docker.Client(base_url=ip_str)    
    # reading base docker commands
    print "Docker file does not exist. Creating docker file..."
    copysh_path = os.path.abspath("basedocker") + "/ros_entrypoint.sh"
    
    base_path = os.path.abspath("basedocker") + "/Dockerfile"
    rd_base = open(base_path, "r")
    contents = rd_base.readlines()
    rd_base.close()

    # reading docker file of specific launch files from ros packages
    folder_cmd = "find ~ -type d -name " + rospackage + "_Dockerfile >> tmpfile" #"rospack find " + rospackage + " >> tmpfile"
    subprocess.call(folder_cmd, shell=True)
    pathtmpfile = os.path.abspath("tmpfile")
    tmpfile = open(pathtmpfile, "r")
    pkg_path = tmpfile.read()
    tmpfile.close()
    pkg_path = pkg_path[:-1]
    os.remove(pathtmpfile)
    pkg_path = pkg_path + "/Dockerfile"
    print "!!!!!!!!!!"
    print pkg_path
    dock_read = open(pkg_path, "r")
    tmp_contents = dock_read.readlines()
    dock_read.close()
    idx = 9
    for i in range(len(tmp_contents)):
        contents.insert(idx, tmp_contents[i])
        idx = idx + 1

    # pkgdocker = op
    os.mkdir(rospackage + "_docker")
    tmppath = os.getcwd() + '/' + rospackage + "_docker"
    print tmppath
    tmentrysh = tmppath +  "/ros_entrypoint.sh"
    shutil.copyfile(copysh_path,tmentrysh)
    os.chdir(tmppath)
    make_exec = "chmod +x ros_entrypoint.sh"
    subprocess.call(make_exec,shell=True)
    file = open('Dockerfile', 'w')
    contents = "".join(contents)
    file.write(contents)
    file.close()
    tarcode = "tar zcf Dockerfile.tar.gz Dockerfile ros_entrypoint.sh"
    subprocess.call(tarcode, shell=True)
    buildcode = "curl -v -X POST -H " + '"Content-Type:application/tar"' + \
        " --data-binary '@Dockerfile.tar.gz' http://" + ip + ":" + port + "/build?t=" + image
            
    status = subprocess.call(buildcode, shell=True)
    if (status == 0):
        return True
    else:
        return False
        
def test_answer():
    assert createDockerImg("teleop_twist_keyboard_dockerfile", '10.2.1.1','1139','teleop_twist_keyboard') == False 
