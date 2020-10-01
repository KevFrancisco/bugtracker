<!-- Hello! Title -->
# Bug Tracker
#### [Live Demo](http://kevfrancisco.pythonanywhere.com/) | [Slides](https://docs.google.com/presentation/d/e/2PACX-1vTsSQdbKXSyJ2t89nx7W3PFbwsUERJZbSpfmCLu1KBPbK_0SqeaI3X9x5lyGqWxypBrKtpw_zXXj8EW/pub?start=false&loop=false&delayms=5000) | [Repository](https://github.com/KevFrancisco/bugtracker)
<!-- Youtube: https://youtu.be/VE7nLzftF_0 -->
___
<!-- Summary -->

Manage all your projects in one place. Track bugs and feature requests, and **never** forget an issue again.

One of the problems I faced in previous projects was I forgot issues quite often. It was troublesome trying to track different projects, and all the bugs that would come up. I made this tracker to help me focus on improving my skills while building projects, and not have to think about remembering individual issues.

I also tracked bugs and feature requests to Bug Tracker _using itself_, which I think is really, really cool!
___

## Features
* __Demo user login__ - Want to try out Bug Tracker quickly? Use one of the demo accounts provided.
* __Charts by Google Visualization API__ - to easily see which projects have the most tickets.
    * Clicking a section in the charts takes you to the relevant ticket list.
* __Critical priority tickets in the front page__ - know which issues to work on first
* __Resolved tickets in the front page__ - see the most recent issues resolved
* __Masonry layout in the projects page__ - because it's beautiful, and why not :D
    * Complete with an identifying image.
    * _For best results, use a transparent png file without whitspace borders._
* __Search box in ticket list__ - search for the issue you want, fast!

## Structure

The main object in Bug Tracker are tickets, which lists all the details regarding an issue. Contrary to it's name, a ticket can be of other types aside from a Bug Report. It also has other relevant properties like status to indicate whether a bug is open, resolved, or if the developer needs additional information. Tickets also have priority as low, medium, high or critical.

**Ticket Types:**
* Bug Report
* Feature Request
* Other Comment
* Documentation Request

Tickets belong to a project, and without a project a ticket cannot be made. A project also has a deadline to help the Users remember a deadline to finish debugging. As an added feature, an image may be uploaded to a project to help Users visualize the project in the project list.

---

## Permissions

**Admin**
* Submit Tickets
* Be assigned to tickets
* Resolve Tickets
* Delete Users
* Basically, the Admin role can do anything

**Project Manager**
* Create and Delete Projects
* Upload project images

**Developer**
* Delete tickets
* Mark tickets as resolved

**Submitter**
* Create new tickets

---
## Tools Used
* Flask - https://getbootstrap.com
* Bootstrap - https://getbootstrap.com
* Google Visualization API - https://developers.google.com/chart/interactive/docs
* Font Awesome - https://font-awesome.com
* Bootstrap-Table - https://bootstrap-table.com
* Bootstrap-Validate - https://bootstrap-validate.js.org
* Slim-Scroll - https://github.com/rochal/jQuery-slimScroll
* Undraw - https://undraw.co/illustrations
* Transparent Textures - https://www.transparenttextures.com
* Subtle Patterns - https://www.toptal.com/designers/subtlepatterns/
* Stack Overflow (●'◡'●) - https://stackoverflow.com
* Undraw - https://undraw.co/illustrations
* Tabler-Icons - https://tablericons.com
* Freepik - https://www.freepik.com
* SlidesGo - https://slidesgo.com 


---
# Plans for the future of Bug Tracker
#### Long Term
* Bug Tracker will continue to recieve updates and reworks as long as I write code, it's my personal tool after all.
* Long term, I'd like to build it with Rust-lang and Electron, see how performant and aesthetic I can make it.
* I'd also like to make a Desktop App alternative, it would be cool to have functionality like Slack, Discord, and Spotify, applications that run on browsers and outside it.

#### Medium Term
* As for improvements, I will be migrating the authenticating and authorization features to Flask-Admin and Flask-Login respectively, to further leverage the Flask ecosystem.

#### Short Term
* I have plans to make a messaging system to enable developers to share ideas debugging.
* Another feature is a sprint system to track project goals with deadlines.
* Also, I am planning to tweak some views, the ticket list in particular can be improved to be more concise and intuitive.
* A ticket history will also be added where all changes to a ticket are logged with the following: User who updated the ticket, value changed, and a datetime stamp.
* Lastly, I will be adding an archive system where resolved tickets and finished projects can be checked for future reference.
