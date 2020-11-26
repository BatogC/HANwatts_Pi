from webdav3.client import Client

options = {
 'webdav_hostname': "http://192.168.110.5:80/HANWattsFolder",
 'webdav_login':    "CristianBatog",
 'webdav_password': "x"
}
client = Client(options)
client.verify = False # To not check SSL certificates (Default = True)
#client.session.proxies(...) # To set proxy directly into the session (Optional)
#client.session.auth(...) # To set proxy auth directly into the session (Optional)
#client.execute_request("mkdir", 'directory_name')
files1 = client.list()
print (files1)