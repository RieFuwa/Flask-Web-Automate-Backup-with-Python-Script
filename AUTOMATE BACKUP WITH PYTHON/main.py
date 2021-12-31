from flask import Flask, render_template, request
from flask.helpers import url_for
import shutil
from datetime import date
import os
import sys
import zipfile
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='templates')
  
# When there is need, just change the directory
os.chdir(sys.path[0])  
#C:\Users\bedir\Desktop\
# src_dir,
# src_file_name,                 #zip kop. txt kop. addeğiş. istedigin yer.
# dst_file_name,                             #C:/Users/bedir/Desktop/bb/ C:/Users/bedir/Desktop/
#  dst_dir
   
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
   
	 
 
    
# Function for performing the
# backup of the files and folders
@app.route("/backup",methods=["POST"])
def take_backup():                             #C:/Users/bedir/Desktop/CC/
    src_dir=request.form["src_dir"]
    src_file_name=request.form["src_file_name"]
    dst_file_name=request.form["dst_file_name"]
    dst_dir=request.form["dst_dir"]   
     
        
    try:      
        # Extract the today's date
        today = date.today()  
        date_format = today.strftime("%d_%b_%Y_")    
        # Make the source directory,
        # where we wanna backup our files
        src_dir = src_dir+src_file_name #dosya yoluyla adi birleştiriyorum 
        # If user not enter any source file,
        # then just give the error message...
        if not src_file_name:
            print("Please give atleast the Source File Name")
            exit() 
        try:           
            # If user provides all the inputs
            if src_file_name and dst_file_name and src_dir and dst_dir:
                dst_dir = dst_dir+date_format+dst_file_name   
                print(dst_dir)             
                print("KONTROL 1")               
            # When User Enter Either 
            # 'None' or empty String ('')
            elif dst_file_name is None or not dst_file_name: #aynı dizindeyse dosya adi girilerek--- ad,yol,yeni yol--- ad,yol ----
                dst_file_name = src_file_name
                dst_dir = dst_dir+date_format+dst_file_name
                print(dst_dir)
                print("KONTROL 2")
            # When user Enter an a
            # name for the backup copy
            else: 
                dst_dir = dst_dir+date_format+dst_file_name #aynı dizindeyse sc sadece yeni adi--- farklı dizindeyse sc yeni adi ve dosya yolu --- sc'nin bulundugu yere kaydeder
                print(dst_dir)
                print("KONTROL 3")
            # Now, just copy the files
            # from source to destination
            shutil.copy2(src_dir, dst_dir) 
            print("Backup Successful!")                    
        except FileNotFoundError:
            print("File does not exists!,\
            please give the complete path")               
    # When we need to backup the folders only...
    except PermissionError:  
        dst_dir = dst_dir+date_format+dst_file_name         
        # Copy the whole folder
        # from source to destination
        src = os.path.join("c:/",src_dir)
        dst = os.path.join("c:/",dst_dir)
        shutil.copytree(src, dst)
        print("Folder backup Successful!")
            
    
    return redirect("/home")
if(__name__=='__main__'):
    app.run(host="0.0.0.0",port=5000,debug=True)           
    # When we need to backup the folders only...
    # except PermissionError:  
    #     dst_dir = dst_dir+date_format+dst_file_name         
    #     # Copy the whole folder
    #     # from source to destination
    #     shutil.copytree(src_file_name, dst_dir)
    #     print("Folder backup Successful!")
# Call the function
# y=str(input("Dosya yolunu giriniz: "))
# print(os.listdir(y))
# x=str(input("Dosya adini giriniz: "))
# a=str(input("Dosyanin yeni adini giriniz: "))
# z=str(input("Dosyanin kaydedeceginiz yere gidiniz: "))
# take_backup(y,x,a,z)