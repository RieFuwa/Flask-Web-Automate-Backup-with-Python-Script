import json
import os
import threading
import schedule
import shutil
from datetime import date
def getbackup():
    if(os.path.exists('backup.json')):
            with open('backup.json', 'r') as file:
                data_x = json.load(file)
                file.close()                          
    date_backup = date.today()
    str_date_backup = str(date_backup).replace('-','-')       
                          
    for data in data_x:
        path_output=data["input"]+'//'+str_date_backup+'-BACKUP'
        if(os.path.exists(path_output)):         
            try:
                os.remove(path_output)           
            except:
                shutil.rmtree(path_output)                
           
        shutil.copytree(data["input"], path_output)       
        print(path_output)
def timer():
    schedule.every(5).seconds.do(getbackup)
    while(True):
        schedule.run_pending()

timerStart = threading.Thread(target=timer)
timerStart.start()