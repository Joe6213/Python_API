import requests
import json
import time
# 取得Token

class API:
    #API class can access the web server to grab microgid data, by 劉
    def __init__(self,ip:str) -> None:
        ''' __init__ is the function that construct the class
            Parameters
            ----------
            self.token: string
                        The string that server require to access database and need to update,
                        when each call.
                        Can be updated by GetAccessToken().
            
            self.ip:    string
                        Content the server IP, need to input by user.
        '''
        self.token="0"
        self.ip=ip
    def GetAccessToken(self)-> str: 
        ''' GetAccessToken is the function that get the token from server.
            Parameters
            ----------
            url: string
                The server api url, that use to access the token.
            headers: json
                The header that the server need.
            data: json
                The data that server need to login.
                username admin
                password admin
            recieve: json
                The data that server return.
                Access token content in key:['data']
            
            Returns
            -------
            type:       string
            describe:   The server api access token
                
        '''
        url = 'http://'+self.ip+"/api/auth/login" 
        headers = {
            'Authorization': 'access_token myToken'
        }
        data = {
            "username":"admin",
            "password":"admin"
        }
        recieve = requests.post(url, headers=headers, data=data)
        self.token=recieve.json()["data"]
        

    # 讀取資料
    def ReadAPI(self,device:str)-> json :
        '''ReadAPI is the function that access server to get latest data.
            Parameter
            ---------
            device: string
                The device that the data from.
                Example:"pcs100hv_1700214814785941" -> "DeviceClass_SerialNumber"
            url: string
                The server api url, that use to get data.
            headers: json
                The header that the server need.
                And need to content the token to access.
                Example:
                    {
                        'Content-Type':'application/json',
                        'Authorization': 'Bearer <YOUR_TOKEN>'
                        }
            data: json
                The data that what data should server get.
                Example:
                    {
                        'formula':'pcs100hv_1700214814785941', #'formula':'Deice_SerialNumber'
                        }
            recieve: json
                The data that server return.
                Data you need content in key:['data']
            
            Returns
            -------
            type:       json
            describe:   All data in the system.
        '''
        self.GetAccessToken() 
        url = "http://"+self.ip+"/api/plugin-center/devices/openRealData" 
        headers = {
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        data = {
            'formula':str(device)
        }
        data=json.dumps(data)
        recieve_data = requests.post(url, headers=headers, data=data)
        return recieve_data.json()

    def WriteAPI(self,device:str,address:str,input_data:float)-> json:
        '''WriteAPI is the function that access server to overwrite data.
            Parameter
            ---------
            device: string
                The device that the data from.
                Example:"pcs100hv_1700214814785941" -> "DeviceClass_SerialNumber"
            url: string
                The server api url, that use to get data.
            headers: json
                The header that the server need.
                And need to content the token to access.
                Example:
                    {
                        'Content-Type':'application/json',
                        'Authorization': 'Bearer <YOUR_TOKEN>'
                        }
            data: json
                The data that what data should server overwrite.
                Example:
                    {
                        'formula':'pcs100hv_1700214814785941_W100', #'formula':'Deice_SerialNumber_Address'
                        'value':'100'                               #'value':'ValueThatYouWantToOverWrite'
                        }
            recieve: json
                The data that server return.
                Data that tell is fail or not
            
            Returns
            -------
            type:       json
            describe:   The data that tell is success orvewrite or not.
        '''
        self.GetAccessToken()
        url = "http://"+self.ip+"/api/plugin-center/devices/openWrite" 
        headers = {
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        data = {
            'formula':device+'_{}'.format(address),
            'value':str(input_data)
        }
        data=json.dumps(data)
        recieve_data = requests.post(url, headers=headers, data=data)
        return recieve_data.json()

if __name__ == '__main__':
    api=API('140.115.65.34:8001')
    #recieve=api.ReadAPI("pcs100hv_1700214814785941")
    # print(recieve)
    i=0
    while(True):
        # recieve=api.WriteAPI('electronicontrol_2023120400','W100',i)
        start=time.time()
        recieve=api.ReadAPI('pcs100hv_1700214814785941')['data']
        print(recieve)
        print('\n\n\n\n\n',time.time()-start)
        i+=1
        time.sleep(0.5)

    # print(api.token)
    