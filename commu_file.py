from _typeshed import Self
from FTP_client import connect_FTP as FTP
from Modbus_client import connect_Modbus as Mod
from INI_config import ini_config as ini

class commutnicate_app():
    def __init__(self):
        self.FTP_ip = "127.0.0.1"
        self.FTP_port = 21
        self.FTP_user = "****"
        self.FTP_psw = "****"
        self.device_name ="" #EMU-B20MC,EMU-B20SM
        self.MOd_ip ="127.0.0.1"
        self.type_connection = "Modbus"
        self.client_configParser = ini.ini_config()
    
    def setFTP_connect(self,ip,user,psw,port =21):
        self.FTP_ip = ip
        self.FTP_user = user
        self.FTP_psw = psw
        self.FTP_port =port

    def setModbus_connect(self,ip):
        self.MOd_ip = ip
    
    def setDevice_name_log(self,device_name):
        self.device_name = device_name

    def setPath_ini(self,read,write):
        self.client_configParser.setPath(read,write)

    def connnection_brige(self,con_type): #connect FTP&client type
        self.client_connectFTP = FTP.FTP_client()
        self.client_connectFTP.connect(self.FTP_ip,self.FTP_user,self.FTP_psw)
        #con_type = Modbus,MQTT
        self.type_connection = con_type
        if(self.type_connection == "Modbus"): 
            self.client_connect1 = Mod.Modbus_connect()
            self.client_connect1.connect_client(self.MOd_ip)
        elif(self.type_connection =="MQTT"): #undev. MQTT
            pass
        else :
            print("unknow type\n")

    def get_least_firmwareVer(self): #check FTP detail 
        version = self.client_connectFTP.check_firmware_ver_server()
        print("avaliable firmware version: ",version)
        return version
    
    def get_allDevice_least_update(self): #check FTP log return Json form
        log_update,log_key = self.client_connectFTP.sort_detail(self.device_name)
        print("rev. date log_update: ",log_update)
        return log_update,log_key
    
    def getInfo_device(self):
        if(self.type_connection) == "Modbus":
            mac,ver,status,id = self.client_connect1.get_info_device()
            print("\nmac : ",mac)
            print("\nversion : ",ver)
            print("\nid : ",id)
            for i in range(len(status)):
                print("\nstatus "+str(i)+" : ",status[i])
            return mac,ver,status,id
        elif(self.type_connection == "MQTT"):
            pass
        else:
            print("type not map, try again!")

    def getINI_file(self):
        data,key =self.client_configParser.read_INI_to_Json()
        return data,key

    def command_print_ini(self): #undev lack data input
        self.client_configParser.setDevice_name(self.device_name)
        self.client_configParser.setDevice_info()
        self.client_configParser.ini_print()
    
    def command_update_firmware(self):
        if(self.device_name == "Modbus"):
            self.client_connect1.update_firmware()
            print("current updating ....")
        elif (self.device_name == "MQTT"):
            pass
        else:
            print("type not map, try again!")

if __name__ == "__main__":
    ip = '*****'
    user = '*****'
    pws = '*****'
    device_name = "EMU-B20MC"
    Path_Download = "../transfer_file_log/"
    Path_server = "/"+device_name+"/fw/log"
    filename = "detail.txt" #test search
    