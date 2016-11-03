import paramiko
def write_nid(oamip,ccpip,cesip,uesip):
    with open("own_nid","w") as fp:
        fp.write("0xE040")
    t = paramiko.Transport((oamip,22))
    t.connect(username = "_rcpadmin", password = "RCP_owner")       
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put("own_nid", "/opt/nokia/etc/node_id/own_nid")
    
    with open("own_nid","w") as fp:
        fp.write("0xE050")
    t = paramiko.Transport((ccpip,22))
    t.connect(username = "_rcpadmin", password = "RCP_owner")       
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put("own_nid", "/opt/nokia/etc/node_id/own_nid")
    
    with open("own_nid","w") as fp:
        fp.write("0xE070")
    t = paramiko.Transport((cesip,22))
    t.connect(username = "_rcpadmin", password = "RCP_owner")       
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put("own_nid", "/opt/nokia/etc/node_id/own_nid")
    
    
    with open("own_nid","w") as fp:
        fp.write("0xE060")
    t = paramiko.Transport((uesip,22))
    t.connect(username = "_rcpadmin", password = "RCP_owner")       
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put("own_nid", "/opt/nokia/etc/node_id/own_nid")    

    print "write nid ok"
   