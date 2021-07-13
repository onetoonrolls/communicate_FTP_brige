import configparser
import re
   
class ini_config():
   
    def __init__(self):
        self.data =  configparser.ConfigParser() #inherit parser object
        self.device_name = ""
        self.status = []
        self.FTP_data ={}
        self.device_info = {}
        self.version = []
        self.id = []
        self.ip = []
        self.mac = []
        self.path_write = "INI_config/ini_storage/"
        self.path_read = "INI_config/ini_storage/example.ini"

    def setDevice_name(self,device):
        self.device_name = device

    def setStatus(self,status_rev):
        status ={}
        MES = status_rev[0]
        SDC = status_rev[1]
        NTP = status_rev[2]
        TCP = status_rev[3]
        status["MES"]= MES
        status["SDC"]= SDC
        status["NTP"]= NTP
        status["TCP"]= TCP
        self.status.append(status)

    def setFTP_data(self,FTP):
        self.FTP_data["port"]= FTP

    def setId_device(self,ID):
        self.id.append(ID)
    
    def setVersion(self,ver):
        self.version.append(ver)

    def setDevice_basicDetail(self,id,ip,mac):
        self.ip.append(ip)
        self.mac.append(mac) 
        self.id.append(id) 
    
    def setDevice_info(self,ip,mac,id,sta,C_ver):
        self.setDevice_basicDetail(id,ip,mac)
        self.setStatus(sta)
        self.setVersion(C_ver)

    def setPath(self,read,write): #if string same = same path,if string NULL = no change path
        if(read =="same"):
            read = write
        elif(read =="NULL"):
            read = self.path_read
        elif(write =="same"):
            write = read
        elif(write =="NULL"):
            write = self.path_write
        self.path_read = read
        self.path_write = write

    def ini_print(self):
        file_name = self.path_write+'config_'+self.device_name+'.ini'
        self.setPath("same",file_name)
        self.data.read(self.path_read)
        print(self.data.sections())
        if(self.data.sections() !=[]): #check data not overwrite
            for section in self.data.sections(): #get old data
                for key,value in self.data.items(section):
                    if(key =="ip"):
                        self.ip.append(value)
                        #print("value ip: ",value)
                    elif(key =="mac"):
                        self.mac.append(value)
                        #print("value mac: ",value)
                    elif(key =="id"):
                        self.id.append(value)
                        #print("value id: ",value)
                    elif(key =="status"):
                        self.status.append(value)
                        #print("value status: ",value)
                    elif(key =="c_version"):
                        self.version.append(value)
                        #print("value ver: ",value)
                    else:    
                        print("key not macth; key: ",key,value)

        for i in range(len(self.data.sections())+1): #create section topic in new file
            
            self.data[self.device_name+"-"+str(i+1)]={
                "ip" : self.ip[i],
                "mac" : self.mac[i],
                "id" : self.id[i],
                "status" : self.status[i],
                "c_version" : self.version[i]
            }

        with open(file_name, 'w') as configfile: #write file
            self.data.write(configfile)
            print("ini file printed")

    #convert .ini file to Json
    def read_INI_to_Json(self):
        print("current read file: ",self.path_read)
        dic_con = {} #original convert data form
        new_dic_con ={} #soil data from ini file
        self.data.read(self.path_read)
        print(self.data.read(self.path_read))
        #return all section in .ini file
        for section in self.data.sections():
            print("section",section)
            dic_con[section] ={}
            for key,value in self.data.items(section):
                dic_con[section][key]=value
        key_obj = new_dic_con.keys()

        return dic_con,key_obj

if __name__ == "__main__":
    stataus = ["nor","nor","nor","nor"]
    #FTP = {"port":21,"server":"ndrs"}
    a = ini_config()
    #a.setPath("INI_config/ini_storage/example.ini","INI_config/ini_storage/")
    #a.setDevice_info("127.0.0.1","0x14E52E02A","0x0008",stataus,"0x0123")
    #a.ini_print()
    a.setPath("INI_config/ini_storage/config_EMU-B20MC.ini","NULL")
    readINI,keyReadINI = a.read_INI_to_Json()
    print("\nkey INI file : ",keyReadINI)
    print("\nobj INI file : ",readINI)