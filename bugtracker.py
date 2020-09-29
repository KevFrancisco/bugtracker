import os

from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
### Moved to models.py -> from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
### See Reference Guide for Flask File Uploads -> https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/ ###
from werkzeug.utils import secure_filename

from helpers import apology, login_required, allowed_file
from models import Project, Ticket, Ticket_History_Entry, Ticket_Message, db, User

# We use a helper function to push a context to Flask when using CLI -> db.create_all()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bugtracker.db"
    db.init_app(app)
    return app

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True # Verbose output to stderr
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bugtracker.db"

# File Upload Configuration
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# 2 MB Max
UPLOAD_FOLDER = 'uploads\img\project-cards'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize db, see reference about separating models.py
# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
db.init_app(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

##############################################
##########   File Upload Handling   ##########
##############################################

# Upload Test
@app.route('/upload-test', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Guard Clauses
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # If there is both a file and is one of the allowed filetypes
        if file and allowed_file(file.filename):
            filename = "demo" + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("/sandbox/uploadtest.html")

@app.route('/uploads/img/project-cards/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


########################################
##########   Routes Section   ##########
########################################

@app.route("/")
def index():
    """Show All """
    # Redirect if a user is logged in
    if session.get('user_id', None) != None:
        return redirect(url_for('overview_main'))
    
    # Default welcome page with Jumbotron
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register a new user """
    if request.method == "POST":
        f_user_name = request.form.get("f_user_name")
        f_user_password = request.form.get("f_user_password")
        f_user_email = request.form.get("f_user_email")
        f_user_first_name = request.form.get("f_user_first_name")
        f_user_last_name = request.form.get("f_user_last_name")
        f_user_role = request.form.get("f_user_role")


        # We cannot do this client side without exposing all the user names :(
        # Check if username already exists in Users database
        userlist = User.query.with_entities(User.user_name).all()
        # Clean the list (Unpack), get only the first item (the username)
        # user[0] because it's a list of tuples
        userlist = [user[0] for user in userlist]
        if f_user_name in userlist:
            return render_template("register.html", msg_error="Username is taken, please choose another username")

        newuser = User(
                        user_name=f_user_name,
                        user_hash=generate_password_hash(f_user_password),
                        user_email=f_user_email,
                        user_first_name=f_user_first_name,
                        user_last_name=f_user_last_name,
                        user_role=f_user_role
                        )
        db.session.add(newuser)
        db.session.commit()

        message="Registration Succesful. You may now log in."
        return render_template("login.html", msg_success=message)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Alias the login username and password
        l_username = request.form.get("f_user_name")
        l_password = request.form.get("f_user_password")

        # Ensure username was submitted
        if not request.form.get("f_user_name"):
            return render_template("login.html",
                                    msg_error="Please enter a username.")

        # Ensure password was submitted
        elif not request.form.get("f_user_password"):
            return render_template("login.html",
                                    msg_error="Please enter a password.")

        # Alias the user row, then check if the user is registered, and the password hash matches
        userrow = User.query.filter_by(user_name=l_username).first()
        if not userrow or not check_password_hash(userrow.user_hash, l_password):
            return render_template('login.html', error="Invald username and/or password. Please check your credentials.")

        # Remember which user has logged in
        session["user_id"] = userrow.user_id
        session["user_role"] = userrow.user_role
        session["user_first_name"] = userrow.user_first_name
        session["user_last_name"] = userrow.user_last_name

        msg_success = f"Login succesful! Welcome back, {session['user_first_name']}."
        # Redirect user to home page
        # return render_template("overview.html", 
        #                         user_id=session["user_id"], 
        #                         user_first_name=session["user_first_name"], 
        #                         user_last_name=session["user_last_name"],
        #                         user_role=session["user_role"], 
        #                         msg_success=msg_success)
        # Pass message success as a get argument
        # https://stackoverflow.com/questions/24451019/redirect-with-data-parameter-in-flask
        return redirect(url_for('overview_main',
                                msg_success=msg_success))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


##################################################
#                    OVERVIEW                    #
##################################################

@app.route("/overview")
@login_required
def overview_main():
    """ Show Overview of all tickets made with graphs """
    projectslist = Project.query.all()
    ticketslist = Ticket.query.all()

    # Retrieve url argument
    msg_success=request.args.get('msg_success')

    return render_template("overview.html",
                            user_id=session["user_id"],
                            user_first_name=session["user_first_name"], 
                            user_last_name=session["user_last_name"],
                            user_role=session["user_role"],
                            msg_success=msg_success,
                            projectslist=projectslist,
                            ticketslist=ticketslist)

##################################################
#                    PROJECTS                    #
##################################################

@app.route("/projects")
@login_required
def projects_main():
    """ Show Overview of all projects """
    projectslist = Project.query.all()
    msg_error=request.args.get('msg_error')
    msg_success=request.args.get('msg_success')

    return render_template("/projects/manage_projects.html", 
                            projectslist=projectslist,
                            msg_success=msg_success,
                            msg_error=msg_error)


@app.route("/projects/new", methods=["GET", "POST"])
@login_required
def projects_new():
    """ Create a New Project """
    if request.method == "POST":
        # Add the project to the database
        # Get New Project details. No need to put guard clauses
        # Forms are verified client side via bootstrap-validate library

        if session["user_role"] not in ["Admin", "Project Manager"]:
            msg_error = "Project not logged. Only User\'s with the Admin or Project Manager Role may create new Projects"
            return redirect(url_for('projects_main', msg_error=msg_error))

        # Alias the data the user submitted
        new_proj_name = request.form.get("f_proj_name")
        new_proj_user_id = request.form.get("f_proj_user_id")
        raw_proj_deadline = request.form.get("f_proj_deadline")
        new_proj_deadline = datetime.strptime(raw_proj_deadline, '%Y-%m-%d')
        new_proj_desc = request.form.get("f_proj_desc")

        # Create a new Project instance
        new_project = Project(proj_name=new_proj_name,
                              proj_user_id=new_proj_user_id,
                              proj_deadline=new_proj_deadline,
                              proj_desc=new_proj_desc)

        # Add it to the session, then
        # Always db.session.commit()
        # aka save changes -> required by SQLAlchemy after every session touch
        db.session.add(new_project)
        db.session.commit()

        # Handle the File Image Card
        if 'f_proj_img' not in request.files:
            flash("No File Picked")
            #flash('No file part')
            return redirect(request.url)
        file = request.files['f_proj_img']

        # if user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash("File Submitted was empty")
            #flash('No selected file')
            return redirect(request.url)
        
        # If there is both a file and is one of the allowed filetypes
        if file and allowed_file(file.filename):
            filename = str(new_project.proj_id) + ".png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        msg_success = "Project Created!" + str(new_project.proj_id)
        userlist = User.query.filter_by(user_role="Project Manager").all()
        projectslist = Project.query.all()

        return redirect(url_for('projects_main'))

    else:
        # Create new project page
        userlist = User.query.filter((User.user_role=="Project Manager") | (User.user_role=="Admin")).all()
        
        msg_error = str()
        if session["user_role"] not in ["Admin", "Project Manager"]:
            msg_error = "Only User\'s with the Admin or Project Manager Role may create new Projects"

        return render_template("/projects/project_new.html",
                                msg_error=msg_error,
                                userlist=userlist)

@app.route("/manage_project/<int:url_proj_id>", methods=["GET", "POST"])
@login_required
def manage_project(url_proj_id):

    """ Edit a Single Project """

    project = Project.query.get(url_proj_id)
    projectlist = Project.query.all()
    userlist = User.query.filter((User.user_role=="Project Manager") | (User.user_role=="Admin")).all()

    if request.method == "POST":

        # Edit the project
        new_proj_name = request.form.get("f_proj_name")
        new_proj_user_id = request.form.get("f_proj_user_id")
        raw_proj_deadline = request.form.get("f_proj_deadline")
        new_proj_deadline = datetime.strptime(raw_proj_deadline, '%Y-%m-%d')
        new_proj_desc = request.form.get("f_proj_desc")

        project.proj_name = new_proj_name
        project.proj_user_id = new_proj_user_id
        project.proj_deadline = new_proj_deadline
        project.proj_desc = new_proj_desc

        db.session.commit()
        
        if 'f_proj_img' in request.files:
            file = request.files['f_proj_img']
            # if user does not select file, browser also submits an empty part without filename
            if file.filename != '':
                # If there is both a file and is one of the allowed filetypes
                if file and allowed_file(file.filename):
                    filename = str(url_proj_id) + ".png"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        msg_success = "Project updated."

        return redirect(url_for('projects_main'))
    else:
        return render_template("/projects/manage_project.html",
                         project=project,
                         projectlist=projectlist,
                         userlist=userlist)

@app.route("/manage_project/delete/<int:url_proj_id>", methods=["GET", "POST"])
@login_required
def delete_project(url_proj_id):

    """ DELETE Project """
    if session["user_role"] in ["Admin", "Project Manager"]:

        # No need to set relationships (orphaned projects and messages) to null, the ORM handles relationships
        # The relationships were set to Nullable=True in models to be safe
        delete_project = Project.query.get(url_proj_id)

        db.session.delete(delete_project)
        db.session.commit()

        msg_success = "Project was succesfully deleted!"
        projectslist = Project.query.all()

        return redirect(url_for('projects_main'))
    else:
        msg_error = "You do not have authorization to delete a project."
        project = Project.query.get(url_proj_id)
        userlist = User.query.filter_by(user_role="Project Manager").all()
        projectslist = Project.query.all()

        return render_template("/projects/manage_project.html",
                                project=project,
                                projectlist=projectslist,
                                userlist=userlist,
                                msg_error=msg_error)


#################################################
#                    Tickets                    #
#################################################

@app.route("/tickets")
@login_required
def tickets_main():
    """ Show Overview of all Tickets """
    ticketslist = Ticket.query.order_by(Ticket.tck_created.desc()).all()
    msg_error=request.args.get('msg_error')
    msg_success=request.args.get('msg_success')
    return render_template("/tickets/manage_tickets.html",
                            msg_error=msg_error,
                            msg_success=msg_success,
                            ticketslist=ticketslist)

@app.route("/tickets/search/<string:tck_column>/<string:str_q>")
@login_required
def tickets_search(tck_column, str_q):
    """ Show Overview of Tickets, by Type, Prio, or Status """
    if tck_column == 'type':
        ticketslist = Ticket.query.filter_by(tck_type=str_q).order_by(Ticket.tck_created.desc())
    elif tck_column == 'priority':
        ticketslist = Ticket.query.filter_by(tck_prio=str_q).order_by(Ticket.tck_created.desc())
    elif tck_column == 'status':
        ticketslist = Ticket.query.filter_by(tck_status=str_q).order_by(Ticket.tck_created.desc())
    else:
        return apology("Internal Server Error", 500)

    return render_template("/tickets/manage_tickets.html", 
                            ticketslist=ticketslist)

@app.route("/tickets/search/<int:url_proj_id>/<string:tck_column>/<string:str_q>")
@login_required
def tickets_search_with_project(url_proj_id, tck_column, str_q):
    """ Show Overview of Tickets, by Type, Prio, or Status """
    # Using logical operators for SQL Alchemy ORM: https://stackoverflow.com/a/14185275/14000441
    # Otherwise you can call .filter_by multiple times, but it's harder to read than | and &
    if tck_column == 'type':
        ticketslist = Ticket.query.filter((Ticket.tck_type==str_q) & (Ticket.tck_proj_id==url_proj_id)).order_by(Ticket.tck_created.desc())
    elif tck_column == 'priority':
        ticketslist = Ticket.query.filter((Ticket.tck_prio==str_q) & (Ticket.tck_proj_id==url_proj_id)).order_by(Ticket.tck_created.desc())
    elif tck_column == 'status':
        ticketslist = Ticket.query.filter((Ticket.tck_status==str_q) & (Ticket.tck_proj_id==url_proj_id)).order_by(Ticket.tck_created.desc())
    else:
        return apology("Internal Server Error", 500)

    return render_template("/tickets/manage_tickets.html", 
                            ticketslist=ticketslist)


@app.route("/tickets/new", methods=["GET", "POST"])
@login_required
def ticktets_new():
    """ Create a New Ticket """
    if request.method == "POST":
        # Add the ticket to the database
        # Get New Ticket details. No need to put guard clauses
        # Forms are verified client side via bootstrap-validate library 
        if session["user_role"] not in ["Admin", "Submitter"] :
            msg_error = "Ticket NOT logged. Only User\'s with the Admin or Submitter Role may log new Tickets"
            return redirect(url_for('tickets_main', msg_error=msg_error))

        projectslist = Project.query.all()
        ticketslist = Ticket.query.order_by(Ticket.tck_created.desc()).all()

        # Alias the data the user submitted
        new_tck_proj_id = request.form.get("f_tck_proj_id")
        new_tck_title = request.form.get("f_tck_title")
        new_tck_desc = request.form.get("f_tck_desc")
        new_tck_type = request.form.get("f_tck_type")
        new_tck_prio = request.form.get("f_tck_prio")
        new_tck_status = request.form.get("f_tck_status")
        new_tck_submitter = request.form.get("f_tck_submitter")
        new_tck_developer = request.form.get("f_tck_developer")
        new_tck_created = datetime.now()
        
        # Create a new Ticket instance
        new_ticket = Ticket(tck_proj_id=new_tck_proj_id,
                            tck_title=new_tck_title,
                            tck_desc=new_tck_desc,
                            tck_type=new_tck_type,
                            tck_prio=new_tck_prio,
                            tck_status=new_tck_status,
                            tck_submitter=new_tck_submitter,
                            tck_developer=new_tck_developer,
                            tck_created=new_tck_created)

        # Add it to the session, then
        # Always db.session.commit()
        # aka save changes -> required by SQLAlchemy after every session touch
        db.session.add(new_ticket)
        db.session.commit()

        msg_success = "Ticket Created!"

        ticketslist = Ticket.query.order_by(Ticket.tck_created.desc()).all()
        return render_template("/tickets/manage_tickets.html",
                                ticketslist=ticketslist)

    else:
        # Create new ticket page
        subuserlist = User.query.filter((User.user_role=="Submitter") | (User.user_role=="Admin")).all()
        devuserlist = User.query.filter((User.user_role=="Developer") | (User.user_role=="Admin")).all()
        projectslist = Project.query.all()

        msg_error = str()
        if session["user_role"] not in ["Admin", "Submitter"]:
            msg_error = "Only User\'s with the Admin or Submitter Role may log new Tickets"

        return render_template("/tickets/ticket_new.html",
                                thisuserid=session["user_id"],
                                projectslist=projectslist,
                                subuserlist=subuserlist,
                                msg_error=msg_error,
                                devuserlist=devuserlist)


@app.route("/manage_ticket/<int:url_tck_id>", methods=["GET", "POST"])
@login_required
def manage_ticket(url_tck_id):

    """ Edit a Single Ticket """

    userlist = User.query.filter((User.user_role=="Submitter") | (User.user_role=="Admin")).all()
    thisticket = Ticket.query.get(url_tck_id)

    if request.method == "POST":
        #Get Lists
        projectslist = Project.query.all()
        ticketslist = Ticket.query.order_by(Ticket.tck_created.desc()).all()

        # Alias the data the user submitted
        thisticket.tck_proj_id = request.form.get("f_tck_proj_id")
        thisticket.tck_title = request.form.get("f_tck_title")
        thisticket.tck_desc = request.form.get("f_tck_desc")
        thisticket.tck_type = request.form.get("f_tck_type")
        thisticket.tck_prio = request.form.get("f_tck_prio")
        thisticket.tck_submitter = request.form.get("f_tck_submitter")
        thisticket.tck_developer = request.form.get("f_tck_developer")
        # Authorization, only Admin and Developer can Resolve tickets
        msg_error = str()
        if request.form.get("f_tck_status") == "Resolved":
            if session["user_role"] in ["Admin", "Developer"]:
                thisticket.tck_status = request.form.get("f_tck_status")
            else:
                msg_error= "Only User\'s with Admin or Developer Roles can update tickets as \'Resolved\'"
        # Always do db.session.commit() to save changes
        db.session.commit()

        msg_success = "Ticket updated."

        subuserlist = User.query.filter((User.user_role=="Submitter") | (User.user_role=="Admin")).all()
        return redirect(url_for('tickets_main', msg_success=msg_success, msg_error=msg_error))

    else:
        # Create new ticket page
        subuserlist = User.query.filter((User.user_role=="Submitter") | (User.user_role=="Admin")).all()
        devuserlist = User.query.filter((User.user_role=="Developer") | (User.user_role=="Admin")).all()
        projectslist = Project.query.all()
        
        return render_template("/tickets/manage_ticket.html",
                                thisuserid = session["user_id"],
                                thisticket=thisticket,
                                projectslist=projectslist,
                                subuserlist=subuserlist,
                                devuserlist=devuserlist)

@app.route("/manage_ticket/delete/<int:url_tck_id>", methods=["GET", "POST"])
@login_required
def delete_ticket(url_tck_id):

    """ DELETE Ticket """
    if session["user_role"] in ["Admin", "Developer"]:

        # No need to set relationships (orphaned tickets and messages) to null, the ORM handles relationships
        # The relationships were set to Nullable=True in models to be safe
        delete_ticket = Ticket.query.get(url_tck_id)

        db.session.delete(delete_ticket)
        db.session.commit()

        msg_success = "Ticket was succesfully deleted!"
        ticketslist = Ticket.query.all()

        return render_template("/tickets/manage_tickets.html",
                                ticketslist=ticketslist,
                                msg_success=msg_success)
    else:
        msg_error = "You do not have authorization to delete a ticket."
        ticket = Ticket.query.get(url_tck_id)
        userlist = User.query.filter_by(user_role="Ticket Manager").all()
        ticketlist = Ticket.query.all()


        return render_template("/tickets/manage_ticket.html",
                                ticket=ticket,
                                ticketlist=ticketlist,
                                userlist=userlist,
                                msg_error=msg_error)



###############################################
#                    USERS                    #
###############################################

@app.route("/users")
@login_required
def manage_users():
    """ Show Overview of all Users """
    # Get a list of users
    userlist = User.query.all()
    msg_error=request.args.get('msg_error')
    msg_success=request.args.get('msg_success')

    return render_template("/users/manage_users.html", 
                            user_id=session["user_id"],
                            userlist=userlist,
                            msg_error=msg_error,
                            msg_success=msg_success)


@app.route("/manage_user/<int:url_user_id>", methods=["GET", "POST"])
@login_required
def manage_user(url_user_id):
    """ Edit a Single User """

    if request.method == "POST":

        # Get User table list for the sidebar
        userlist = User.query.with_entities(User.user_id, User.user_name, User.user_first_name, User.user_last_name).all()
        user = User.query.get(url_user_id)

        new_user_name = request.form.get("f_user_name")
        # Check if the username already exists
        usernamelist = User.query.with_entities(User.user_name).all()
        # Clean the list (Unpack), get only the first item (the username)
        # user[0] because it's a list of tuples
        usernamelist = [user[0] for user in usernamelist]

        # The second condition is to make sure the username was changed, otherwise it stays the same
        if new_user_name in usernamelist and new_user_name != user.user_name:
            return render_template("/users/manage_user.html", 
                                    msg_error="Username is taken, please choose another username.",
                                    userlist=userlist, 
                                    user=user)

        new_user_email = request.form.get("f_user_email")
        new_user_first_name = request.form.get("f_user_first_name")
        new_user_last_name = request.form.get("f_user_last_name")
        new_user_role = request.form.get("f_user_role")

        user.user_name = new_user_name
        user.user_email = new_user_email
        user.user_first_name = new_user_first_name
        user.user_last_name = new_user_last_name
        user.user_role = new_user_role

        db.session.commit()
        # Safe to use f-string here bec we validated via javascript
        msg_success = f"User {user.user_name} updated!"
        return redirect(url_for('manage_users', msg_success=msg_success))

    else:
        # Get User table list for the sidebar
        userlist = User.query.with_entities(User.user_id, User.user_name, User.user_first_name, User.user_last_name).all()
        user = User.query.get(url_user_id)

        return render_template("/users/manage_user.html",
                                userlist=userlist,
                                user=user)

@app.route("/manage_user/delete/<int:url_user_id>", methods=["GET", "POST"])
@login_required
def delete_user(url_user_id):
    """ DELETE USER """
    if session["user_role"] == "Admin":
        # If the user is trying to delete himself
        if session["user_id"] == url_user_id:
            userlist = User.query.with_entities(User.user_id, User.user_name, User.user_first_name, User.user_last_name).all()
            user = User.query.get(url_user_id)

            return render_template("/users/manage_user.html", 
                                    msg_error="Your account cannot be deleted while logged in.",
                                    userlist=userlist, 
                                    user=user)

        # No need to set relationships (orphaned tickets and messages) to null, the ORM handles relationships
        # The relationships were set to Nullable=True in models to be safe
        delete_user = User.query.get(url_user_id)

        db.session.delete(delete_user)
        db.session.commit()

        msg_success = "User was succesfully deleted!"
        userlist = User.query.all()

        return render_template('/users/manage_users.html', 
                                msg_success=msg_success, 
                                userlist=userlist)
    else:
        msg_error = "You do not have authorization to delete a user."
        userlist = User.query.all()
        
        return render_template('/users/manage_users.html', 
                                msg_error=msg_error, 
                                userlist=userlist)


#####################################################
########## Built-in error handlers by CS50 ##########
#####################################################

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
