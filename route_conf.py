import paramiko  
import re
import os

rapip="20.5.1.9"


def trs_file(vmip,file,dir):
    t = paramiko.Transport((vmip,22))
    t.connect(username = "_rcpadmin", password = "RCP_owner")       
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put(file, dir)

def reboot_vms(oamip, ccpip, cesip, uesip):
    vms=[]
    vms.append(ccpip)
    vms.append(cesip)
    vms.append(uesip)
    vms.append(oamip)
    for vm in vms:
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect(vm,22,"_rcpadmin", "RCP_owner")
        stdin, stdout, stderr = ssh.exec_command("reboot")    


def regular_find(pattern_text,search_text):
    pattern = re.compile(pattern_text)
    tmp=search_text
    for i in tmp:
        #print i
        search = pattern.search(i)    #pattern.findall(i)
        if search:
            print search.group()
            return search.group()      #print search    
    return None    


def get_fhip(vmip):
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(vmip,22,"_rcpadmin", "RCP_owner")
    stdin, stdout, stderr = ssh.exec_command("ifconfig fronthaul")
    fhip=regular_find("10.5.5.\d+", stdout.readlines())
    ssh.close
    return fhip




def get_vms_ip():
    ipbox=["192.168.2.2","192.168.2.3","192.168.2.4","192.168.2.5"]
    oamip=""
    ccpip=""
    cesip=""
    uesip=""
    for ip in range(4):
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect(ipbox[ip],22,"_rcpadmin", "RCP_owner")
        stdin, stdout, stderr = ssh.exec_command("ps -ef | grep CCS")
        outprint=stdout.readlines()
        if(regular_find("ccs_cp.appstart", outprint)):
            ccpip=ipbox[ip]
        if(regular_find("ccs_mgt.appstart", outprint)):
            oamip=ipbox[ip]  
        if(regular_find("ccs_up.appstart", outprint)):
            uesip=ipbox[ip]              
        if(regular_find("ccs_mix.appstart", outprint)):
            cesip=ipbox[ip]
        ssh.close
    return oamip,ccpip,cesip,uesip



############################################################################
#get vms_ip
print "getting vms ip"
oamip,ccpip,cesip,uesip=get_vms_ip()
oamfhip=get_fhip(oamip)
ccpfhip=get_fhip(ccpip)
uesfhip=get_fhip(uesip)
cesfhip=get_fhip(cesip)
print "oamip"+oamip
print "ccpip="+ccpip
print "cesip="+cesip
print "uesip="+uesip
print "oamfhip"+oamfhip
print "ccpfhip="+ccpfhip
print "cesfhip="+cesfhip
print "uesfhip="+uesfhip

##########################################################################
#config SysComRoute-.xml
print "Configuring SyscomRoute-xml"    
fp3=open("SysComRoute_tmp.xml","r")  
with open("SysComRoute-.xml","w") as fp4 :
    for s in fp3.readlines():  
        s=s.replace("oamip",oamip)
        s=s.replace("ccpip",ccpip)
        s=s.replace("uesip",uesip)
        s=s.replace("cesip",cesip)
        s=s.replace("oamfhip",oamfhip)
        s=s.replace("ccpfhip",ccpfhip)
        s=s.replace("uesfhip",uesfhip)
        s=s.replace("cesfhip",cesfhip)    
        s=s.replace("rapip",rapip)
        fp4.write(s) 
fp3.close()  


#####################################################################################
#trsport file to vms
print "transporting files to vms"
t = paramiko.Transport((oamip,22))
t.connect(username = "_rcpadmin", password = "RCP_owner")       
sftp=paramiko.SFTPClient.from_transport(t)
sftp.put("SysComRoute-.xml", "/opt/nokia/SS_RCPCCSMCU/SysComRoute-.xml")
#sftp.put("ccs_mgt.appstart", "/opt/nokia/SS_RCPCCSMCU/ccs_mgt.appstart")
#sftp.put("ccs_cp.appstart", "/opt/nokia/SS_RCPCCSMCU/ccs_cp.appstart")
t.close


t = paramiko.Transport((ccpip,22))
t.connect(username = "_rcpadmin", password = "RCP_owner")       
sftp=paramiko.SFTPClient.from_transport(t)
sftp.put("SysComRoute-.xml", "/opt/nokia/SS_RCPCCSMCU/SysComRoute-.xml")
#sftp.put("ccs_mgt.appstart", "/opt/nokia/SS_RCPCCSMCU/ccs_mgt.appstart")
#sftp.put("ccs_cp.appstart", "/opt/nokia/SS_RCPCCSMCU/ccs_cp.appstart")
t.close

t = paramiko.Transport((cesip,22))
t.connect(username = "_rcpadmin", password = "RCP_owner")       
sftp=paramiko.SFTPClient.from_transport(t)
sftp.put("SysComRoute-.xml", "/opt/nokia/SS_RCPCCSRT/SysComRoute-.xml")
#sftp.put("ccs_mix.appstart", "/opt/nokia/SS_RCPCCSRT/ccs_mix.appstart")
#sftp.put("ccs_up.appstart", "/opt/nokia/SS_RCPCCSRT/ccs_up.appstart")
t.close

t = paramiko.Transport((uesip,22))
t.connect(username = "_rcpadmin", password = "RCP_owner")       
sftp=paramiko.SFTPClient.from_transport(t)
sftp.put("SysComRoute-.xml", "/opt/nokia/SS_RCPCCSRT/SysComRoute-.xml")
#sftp.put("ccs_mix.appstart", "/opt/nokia/SS_RCPCCSRT/ccs_mix.appstart")
#sftp.put("ccs_up.appstart", "/opt/nokia/SS_RCPCCSRT/ccs_up.appstart")
t.close

###########################################################################################
#config vms_nid  step1
print "configuring nid to vms"
import write_nid
write_nid.write_nid(oamip, ccpip, cesip, uesip)


###########################################################################################
#reboot vms
print "rebooting"
reboot_vms(oamip, ccpip, cesip, uesip)