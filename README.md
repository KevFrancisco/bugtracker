<!-- Hello! Title -->
# Bug Tracker
### _[Live Demo](http://kevfrancisco.pythonanywhere.com/)_
---
<!-- Summary -->

Manage all your projects in one place. Track bugs and feature requests, and **never** forget an issue again.

One of the problems I faced in previous projects was I forgot issues quite often. It was troublesome trying to track different projects, and all the bugs that would come up. I made this tracker to help me focus on improving my skills while building projects, and not have to think about remembering individual issues.

I also tracked bugs and feature requests to Bug Tracker _using itself_, which I think is really, really cool!

## Features
* Demo user login - Want to try out Bug Tracker quickly? Use one of the demo accounts provided.
* Charts by Google Visualization API - to easily see which projects have the most tickets.
    * Clicking a section in the charts takes you to the relevant ticket list.
* Critical priority tickets in the front page - know which issues to work on first
* Resolved tickets in the front page - see the most recent issues resolved
* Masonry layout in the projects page - because it's beautiful, and why not :D
    * Complete with an identifying image.
    * _For best results, use a transparent png file without whitspace borders._
* Search box in ticket list - search for the issue you want, fast!

## Structure

The main object in Bug Tracker are tickets, which lists all the details regarding an issue. Contrary to it's name, a ticket can be of other types aside from a Bug Report. It also has other relevant properties like status, and priority.

####Ticket Type:
* Bug Report
* Feature Request
* Other Comment
* Documentation Request

Tickets belong to a project, and without a project a ticket cannot be made. A project also has a deadline to help the Users remember a deadline to finish debugging. As an added feature, an image may be uploaded to a project to help Users visualize the project in the project list.

---

## Permissions

#### Admin
* Submit Tickets
* Be assigned to tickets
* Resolve Tickets
* Delete Users
* Basically, the Admin role can do anything

#### Project Manager
* Create and Delete Projects
* Upload project images

#### Developer
* Delete tickets
* Mark tickets as resolved

#### Submitter
* Create new tickets

---
# Plans for the future of Bug Tracker
I have plans to make a messaging system to enable developers to share ideas debugging. Another feature is a sprint system to track project goals with deadlines. Also, I am planning to tweak some views, the ticket list in particular can be improved to be more concise and intuitive. Lastly, I will be adding an archive system where resolved tickets and finished projects can be checked for future reference.