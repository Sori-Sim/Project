#success: register -> email + image url
#need work: improve templates
#need work: delete file

from flask import Flask, render_template, request, redirect
import pymysql
import boto3
import json
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
import os

ENDPOINT = "appdb.cfavunhs5tsa.us-east-1.rds.amazonaws.com"
PORT = "3306"
USR = "admin"
PASSWORD = "password1"
DBNAME = "appdb"
ACCESS_KEY = "AKIA26DYSGGADLEFRRL2"
SECRET_KEY = "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"
AWS_REGION = 'us-east-1'
BUCKET_NAME = 'appdemoclould23'
SNS_TOPIC_NAME = 'newSNStest2'

app = Flask(__name__)

@app.route('/')
def main():
     return render_template("login.html")

@app.route('/notfound')
def notfound():
     return render_template("usernotfound.html")

@app.route('/login')
def login():
    render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")  

# Create the "images" folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

@app.route('/add', methods=["POST"])
def add():
    email = request.form.get("email")
    password= request.form.get("password")
    desc=request.form.get("description")
  #  imagepath=request.form.get("imagefilepath")
    f = request.files['file']
     
    try:
        conn =  pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
        cur = conn.cursor()
        
        # Get the S3 key for the uploaded image
        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        s3_key = f"images/{secure_filename(f.filename)}"  # Set the correct folder path on S3
        s3_client.upload_fileobj(f, BUCKET_NAME, s3_key)
        print("Image uploaded to S3 successfully")

        # Use s3_key instead of filename in the SQL query
        cur.execute("INSERT INTO userdetails(email,password,description,imagelocation) VALUES('"+email+"','"+password+"','"+desc+"', '"+s3_key+"');")
        print("Insert Success")
        conn.commit()
    
    except Exception as e:
        print("ERROR " + format(e))
        return redirect("/")
        
    sns_client = boto3.client(
        'sns',
        region_name = AWS_REGION,
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )    
        
    topic = sns_client.create_topic(Name=SNS_TOPIC_NAME)
    topic_arn = topic["TopicArn"]
    
    # Dynamically get the email endpoint from the form input 
    # -> for sending anemail new user
    endpoint_email = request.form.get("email")
    subscritpion = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=endpoint_email,
        ReturnSubscriptionArn=True)['SubscriptionArn']
    
     # Generate S3 key for the uploaded image
     # Set the correct folder path on S3
    s3_key = f"images/{secure_filename(f.filename)}"  
        
    lambda_client = boto3.client('lambda',
        region_name=AWS_REGION)

    lambda_payload={"email":email,"arn":topic_arn, "s3_key": s3_key}
    lambda_client.invoke(FunctionName='mylambdatest', 
                     InvocationType='Event',
                     Payload=json.dumps(lambda_payload))

    return redirect("/")

        
@app.route('/mainpage',methods=["GET"])
def mainpage():
    email= request.args.get('email')
    password= request.args.get('password')
    print(email,password)
    try:
            conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
            cur = conn.cursor()
            qry= "SELECT * FROM userdetails Where email ='"+email+"' AND password = '"+password+"';"
            print(qry)
            cur.execute("SELECT * FROM userdetails;")
            query_results = cur.fetchall()
            print(query_results)
            cur.execute("SELECT * FROM userdetails Where email ='"+email+"' AND password = '"+password+"';")
            query_results = cur.fetchall()
            print(query_results)
            if len(query_results)==1:
               return render_template("mainpage.html")
            else:
                return redirect("/notfound")
    except Exception as e:
            print("Database connection failed due to {}".format(e))
            return redirect("/")

@app.route('/search',methods=["POST"])
def search():
    email = request.form.get("email")
    print(email)
    return redirect("/viewdetails/"+str(email))

@app.route('/viewdetails/<email>')
def viewdetails(email):

    try:
            conn =  pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
            cur = conn.cursor()
            cur.execute("SELECT * FROM userdetails Where email ='"+email+"';")
            conn.commit()
            query_results = cur.fetchall()
            print(query_results)
            client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
            url = client.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': 'appdemoclould23',
                                            'Key': 'images/'+str(query_results[0][3]),
                                        },                                  
                                        ExpiresIn=3600)
            url=str(url).split('?')[0]  # Get url for the pic
            item={'email':query_results[0][0],'password':query_results[0][1],'desc':query_results[0][2],'link':url}
            print(item)
            return render_template("viewdetails.html", item=item)        
    except Exception as e:
            print("Database connection failed due to {}".format(e))
            return redirect("/")

@app.route('/initialize')
def initialize():
    try:
        print("INITIALIZING DATABASE")
        conn =  pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
        cur = conn.cursor()
        try:
            cur.execute("DROP TABLE userdetails;")
            print("table deleted")
        except Exception as e:
            print("cannot delete table")
        cur.execute("CREATE TABLE userdetails(email VARCHAR(20), password VARCHAR(20), description VARCHAR(50), imagelocation VARCHAR(50));")
        print("table created")
        cur.execute("INSERT INTO userdetails(email,password,description,imagelocation) VALUES('test1@gmail.com','password','this is a desc', 'Default.png');")
        print("Insert Success")
        cur.execute("INSERT INTO userdetails(email,password,description,imagelocation) VALUES('test2@gmail.com','password','this is a desc', 'Default.png');")
        print("Insert Success")
        cur.execute("INSERT INTO userdetails(email,password,description,imagelocation) VALUES('test3@gmail.com','password','this is a desc', 'Default.png');")
        print("Insert Success")
        cur.execute("INSERT INTO userdetails(email,password,description,imagelocation) VALUES('test4@gmail.com','password','this is a desc', 'Default.png');")
        print("Insert Success")
        conn.commit()

        cur.execute("SELECT * FROM userdetails;")
        query_results = cur.fetchall()
        print(query_results)
        return redirect("/")
    except Exception as e:
        print("Database connection failed due to {}".format(e))
        return redirect("/")


if __name__=="__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", debug=True, port=5000)