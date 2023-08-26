from flask import Flask, render_template,request,session
import ibm_db

app = Flask(__name__)
app.secret_key="_abcde5"
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT= 30756; UID=sjg34727; PWD=YSrjWWkzJpeYJXgG;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(ibm_db.active(conn))
@app.route("/")
def index():
  return render_template("index.html")
@app.route("/contact")
def contact():
  return render_template("contact.html")
@app.route("/login",methods=["GET","POST"])
def login():
  if request.method=="POST":
    username=request.form["username"]
    password=request.form["password"]
    print(username,password)
    sql="SELECT * FROM REGISTER WHERE USERNAME = ? AND PASSWORD = ?"
    stmt = ibm_db.prepare (conn,sql)
    ibm_db.bind_param (stmt, 1, username)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    out= ibm_db.fetch_assoc(stmt)
    print(out)
    if out != False:
      session['username']=username
      session['emaild']= out ['EMAIL']
      global uname
      if out['ROLE'] == 0:
         return render_template ("adminprofile.html", username=username, emailid =out['EMAIL'])
      elif out['ROLE']==1:
         return render_template ("studentprofile.html" ,username=username, emailid =out['EMAIL'])
      else:
        return render_template ("facultyprofile.html",username=username, emailid =out['EMAIL'])
    else:
      msg = "Invaid Credential"
      return render_template("login.html",message1=msg)
    
  return render_template("login.html")
@app.route("/register", methods = ['GET','POST'])
def register():
  if request.method=='POST':
      username = request.form['sname']
      email=request.form['semail']
      pword = request.form ['spassword']
      role = request.form ['role']
      print(username,email,pword,role)
      sql ="SELECT * FROM REGISTER WHERE USERNAME = ?"
      stmt = ibm_db.prepare(conn,sql)
      ibm_db.bind_param(stmt, 1, username)
      ibm_db.execute(stmt)
      out=ibm_db.fetch_assoc(stmt)
      print(out)
      if out != False:
         msg = "already registered"
         return render_template('register.html',msg =msg)
      else:
        sql = "INSERT INTO REGISTER VALUES(?,?,?,?)"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1,username)
        ibm_db.bind_param(stmt, 2,email)
        ibm_db.bind_param(stmt, 3, pword)
        ibm_db.bind_param(stmt, 4, role)
        ibm_db.execute(stmt)
        msg ="registered"
        return render_template("register.html", msg=msg)

  return render_template("register.html")
if __name__== "__main__":
  app.run(debug=True)

