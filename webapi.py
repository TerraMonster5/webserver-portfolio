from flask import Flask, render_template, session, redirect, request, send_file

serverCookies = dict()

app = Flask(__name__, template_folder="templateFiles", static_folder="staticFiles")

app.templates_auto_reload = True
app.secret_key = "a"

def isLoggedIn(request, cookie) -> tuple:
    cookieArgs = str(cookie).split("|")
    addr = request.remote_addr
    if cookie == None:
        return False, -1
    elif addr in serverCookies.keys():
        if serverCookies[addr] == cookieArgs[2]:
            if cookieArgs[1] == "inf":
                return True, int(cookieArgs[3])
            timediff = float(time.time()) - float(cookieArgs[0])
            if timediff >= float(cookieArgs[1]):
                return False, -1
            else:
                return True, int(cookieArgs[3])
    return False, -1

def genRandString(n) -> str:
    randString = ""
    for x in range(n):
        randString += choice(string.ascii_letters+string.digits)
    return randString

@app.route("/auth", methods=["POST"])
def auth():
    addr = request.remote_addr
    args = request.get_json()
    password = args["pass"]
    save = args["save"]

    hashedPass = sha512(password.encode()).hexdigest()

    if hashedPass in PASSES:
        randString = genRandString(64)
        if save:
            session["user"] = f"{time.time()}|inf|{randString}|{PASSES.index(hashedPass)}"
            serverCookies[addr] = randString
        else:
            session["user"] = f"{time.time()}|3600|{randString}|{PASSES.index(hashedPass)}"
            serverCookies[addr] = randString

        return "Authorised", 200
    
    return "Unauthorised", 401

@app.route("/logout", methods=["GET"])
def logout():
    session["user"] = None
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host="0.0.0.0")