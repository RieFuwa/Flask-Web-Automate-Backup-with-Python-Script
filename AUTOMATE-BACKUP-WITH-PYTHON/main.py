from flask import Flask, render_template, request
from flask.helpers import url_for
import shutil
from datetime import date
import os
import sys
import zipfile
import json
import threading
import schedule
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='templates')
  
os.chdir(sys.path[0])  
 
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
                
@app.route("/home")  
def home():
    return render_template("home.html")
    
@app.route("/zip",methods=["POST"])
def	doprocess():
    source_folder=request.form["source_folder"]
    target_zip=request.form["target_zip"]
    try:
        zipf = zipfile.ZipFile(target_zip, "w")
        for subdir, dirs, files in os.walk(source_folder):
	        for file in files:
		        print (os.path.join(subdir, file))
		        zipf.write(os.path.join(subdir, file))
    except Error:
        print("hata")
    return redirect("/home")

@app.route("/day",methods=["POST"])
def	dayBackup():
    
    src_dir=request.form["src_dir"]
  
    jsonObj={'input':str(src_dir)}
    if(os.path.exists('backup.json')):
            with open('backup.json', 'r') as file:
                data_x = json.load(file)
                file.close()
    else:
            data_x = []
    with open('backup.json', 'w') as file:
            data_x.append(jsonObj)
            json.dump(data_x, file, ensure_ascii=False, indent=4)
            file.close()
        
    return redirect("/home")

@app.route("/backup",methods=["POST"])
def take_backup():                            
    src_dir=request.form["src_dir"]
    src_file_name=request.form["src_file_name"]
    dst_file_name=request.form["dst_file_name"]
    dst_dir=request.form["dst_dir"]   
          
    try:      

        today = date.today()  
        date_format = today.strftime("%d_%b_%Y_")    
        src_dir = src_dir+src_file_name

        if not src_file_name:
            print("Please give atleast the Source File Name")
            exit() 
        try:     
                  
            if src_file_name and dst_file_name and src_dir and dst_dir:
                dst_dir = dst_dir+date_format+dst_file_name   
                print(dst_dir)             
                print("KONTROL 1")               
            elif dst_file_name is None or not dst_file_name: 
                dst_file_name = src_file_name
                dst_dir = dst_dir+date_format+dst_file_name
                print(dst_dir)
                print("KONTROL 2")
            else: 
                dst_dir = dst_dir+date_format+dst_file_name 
                print(dst_dir)
                print("KONTROL 3")
            shutil.copy2(src_dir, dst_dir) 
            print("Backup Successful!")                    
        except FileNotFoundError:
            print("File does not exists!,\
            please give the complete path")        
                   
    except PermissionError:  
        dst_dir = dst_dir+date_format+dst_file_name         

        src = os.path.join("c:/",src_dir)
        dst = os.path.join("c:/",dst_dir)
        shutil.copytree(src, dst)
        print("Folder backup Successful!")
               
    return redirect("/home")
if(__name__=='__main__'):
    app.run(host="0.0.0.0",port=5000,debug=True)
    timerStart = threading.Thread(target=timer)
    timerStart.start()       
