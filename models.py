from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

# Usually we would do SQLAlchemy(app) here, but we do that later to avoid circular reference.
db = SQLAlchemy()

# In order to generate our models via create_all() in the cli, we need to execute the ff:
# Together with the create_app defined in bugtracker.py
# from bugtracker import create_app, db
# app = create_app()
# app.app_context().push()
# db.create_all()

# For relationship declaration see https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

# Declare User before Project because we will be declaring a One-To-Many relationship
# One User manages -> Many Projects
# backref uses the table name, it is lowercase by default!
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    user_hash = db.Column(db.String(300))
    user_email = db.Column(db.String(120), unique=True)
    user_first_name = db.Column(db.String(50))
    user_last_name = db.Column(db.String(50))
    user_role = db.Column(db.String(100))
    user_projects_managed = db.relationship('Project', backref='manager', lazy=True)
    # !! When referencing User ID multipli times from a class
    # In this case a Ticket needs two different ID's, one for the submitter and one for the developer
    # you MUST define the foreign_keys paramater for the column, or SQLAlchemy fails with an ambiguous foreignkey error
    user_ticket_submitted = db.relationship('Ticket', backref='submitter', foreign_keys="Ticket.tck_submitter", lazy=True)
    user_ticket_assigned = db.relationship('Ticket', backref='developer', foreign_keys="Ticket.tck_developer", lazy=True)
    user_messages_sent = db.relationship('Ticket_Message', backref='sender', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.user_name


# Projet Model, it will be linked to a single manager [User]
# with many tickets
class Project(db.Model):
    proj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # A project MUST have a Project Manager! nullable=True, we update it to null for when a user is deleted
    proj_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    proj_name = db.Column(db.String(100))
    proj_desc = db.Column(db.String(555))
    proj_deadline = db.Column(db.DateTime)
    proj_tickets = db.relationship('Ticket', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.proj_name}, {self.proj_desc}, {self.proj_deadline}, {self.proj_user_id}>'

# TODO Add a "Sprint" Class, which an inbuilt "To Do Task List" tracker
# much like Google Tasks but with a deadline 
# We can safely add new classes(tables with create_all), the previous data is untouched
# https://docs.sqlalchemy.org/en/13/core/metadata.html

# TODO Add an attachment class for file uploading...
# See Flask_Uploads
# https://pythonhosted.org/Flask-Uploads/


# Tickets, Belongs to one project
# Linked to many Ticket_History_Entry, and Ticket_Message
class Ticket(db.Model):
    tck_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tck_proj_id = db.Column(db.Integer, db.ForeignKey('project.proj_id'), nullable=False)
    tck_title = db.Column(db.String(50), nullable=False)
    tck_desc = db.Column(db.String(555), nullable=False)
    tck_type = db.Column(db.String(30))
    tck_prio = db.Column(db.String(20))
    tck_status = db.Column(db.String(20))
    tck_submitter = db.Column(db.Integer, db.ForeignKey('user.user_id'), foreign_keys="Ticket_user_id", nullable=False)
    tck_developer = db.Column(db.Integer, db.ForeignKey('user.user_id'), foreign_keys="Ticket_user_id", nullable=False)
    tck_created = db.Column(db.DateTime, nullable=False)
    tck_history_entries = db.relationship('Ticket_History_Entry', backref='ticket', lazy=True)
    tck_messages = db.relationship('Ticket_Message', backref='ticket', lazy=True)

    def __repr__(self):
        return f'<Ticket {self.tck_id}: {self.tck_title}>'


# History Entries for tracking changes to an issue
# Using this class name results in "ticket__history__entry" as the table name
class Ticket_History_Entry(db.Model):
    tckhisten_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tckhisten_tck_id = db.Column(db.Integer, db.ForeignKey('ticket.tck_id'), nullable=False)
    tckhisten_prop = db.Column(db.String(30), nullable=False)
    tckhisten_oldval = db.Column(db.String(30), nullable=False)
    tckhisten_newval = db.Column(db.String(30), nullable=False)
    tckhisten_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Ticket History Entry %r>' % self.tckhisten_id


# Messages for tracking Developer Comments
# Using this class name results in "ticket__message" as the table name
class Ticket_Message(db.Model):
    tckmsg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tckmsg_tck_id = db.Column(db.Integer, db.ForeignKey('ticket.tck_id'), nullable=False)
    tckmsg_msg = db.Column(db.String(555), nullable=False)
    tckmsg_sender = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    tckmsg_timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Ticket %r Message %r>' % self.tckmsg_tck_id, self.tckmsg_id