# Anteater Open Classroom

## Background

UCI has a multitude of study rooms, scattered all across campus. 
As an off-campus student, I spend most of my week (and some weekends!)
studying on the beautiful campus. However, with so many students,
I can almost never find any open study spaces. Thus begins my trek to
find an empty space.

The goal of this project is to save students' valuable time in
finding a study space. Rather than individual tables, this looks for
lecture halls and classrooms that have no scheduled classes.

### Components
   * Frontend UI for easy-to-read calendars and accessibility
   * Backend crawler for set-time, frequent updates
   * Deployment for access to the UCI community

#### Future Ideas/Updates?
  * Location: A recommended page for nearby open areas.
  * Integration with clubs: allow for clubs to add their schedules 
to the page

### Bug Notes
  * Will only be able to see the current schedule (i.e. TODAY's date and time)

#### Implementation
  * Backend
    * Python
      * FastAPI
      * MySQL

  * Frontend
    * Vanilla JS
    * HTML/CSS
   
  * Other Software
    * Docker

  #### Installations
  `pip install fastapi[all]`
  `pip install mysql-connector-python`
  `pip install requests`
