import os`r`nfrom flask import Flask, render_template, request, redirect, url_for, session, flash
from services.api import ApiService

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "aman-local-secret")

@app.route("/")
def home():
    return render_template("home.html")




@app.route("/dashboard")
def dashboard():
    if "token" not in session:
        flash("Enterprise session required. Please authenticate.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/tours")
def tours():
    return render_template("tours.html")

@app.route("/destinations")
def destinations():
    return render_template("destinations.html")

@app.route("/bookings")
def bookings():
    if "token" not in session:
        flash("Authentication required to access booking ledger.", "warning")
        return redirect(url_for("login"))
    return render_template("bookings.html")

@app.route("/customers")
def customers():
    if "token" not in session:
        flash("Authentication required for customer CRM.", "warning")
        return redirect(url_for("login"))
    
    token = session.get("token")
    data, status_code = ApiService.get_users(token)
    
    users_list = []
    if status_code == 200:
        users_list = data
    else:
        flash("Could not fetch customer records from ledger.", "error")
        
    return render_template("customers.html", users=users_list)

@app.route("/analytics")
def analytics():
    if "token" not in session:
        flash("Authentication required for analytics telemetry.", "warning")
        return redirect(url_for("login"))
    return render_template("analytics.html")

@app.route("/profile")
def profile():
    if "token" not in session:
        flash("Authentication required.", "warning")
        return redirect(url_for("login"))
    user_info = {"name": "Aman Director", "email": session.get("user_email", "admin@amantour.io")}
    return render_template("profile.html", user=user_info)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        payload = {"email": email, "password": password}
        
        data, status_code = ApiService.login_user(payload)
        if status_code == 200:
            session["token"] = data.get("access_token") or "mock-jwt-dark-token"
            session["user_email"] = email
            flash("Successfully authenticated into Aman Enterprise Cloud.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(data.get("detail", "Invalid enterprise credentials."), "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        payload = {"name": name, "email": email, "phone": phone, "password": password}
        
        data, status_code = ApiService.register_user(payload)
        if status_code in [200, 201]:
            flash("Enterprise account provisioned successfully. Please sign in.", "success")
            return redirect(url_for("login"))
        else:
            flash(data.get("detail", "Registration failed. Verify parameters."), "error")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully signed out of enterprise cloud.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
