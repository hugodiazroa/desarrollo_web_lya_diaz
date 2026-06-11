# desarrollo_web_lya_diaz
Repositorio para el curso CC5002-2: Desarrollo de Aplicaciones 

# Tarea 1: Scheduler Web App
A simple front-end web app aimed at members of the DCC that permits member registration, activity scheduling, viewing of registered users and their activities and some statistics using vanilla HTML, CSS, and JavaScript. This project has no backend yet, so the users an the activities they create are not trasspassed into a database.


---

## Features

### 1. Home
- Main page where that links to other pages in the app
- Shows:
  - Register 
  - Activity
  - Members
  - Metrics

### 2. Member Registration
- Permit users to register with name, email, and their role inside the university
- Input validation (required fields + valid email format)
- Stores active user in `localStorage` inside `script.js`

### 3. Activity Reporting
- Add activities with:
  - Category of activity
  - Schedule (day, time, duration)
  - At least one image or video
  - Link of activity
- Activities only can be added if:
  - There is a logged-in user
  - There is at least one schedule for the activity
  - All fields are filled

### 4. Member Listing (Static)
- Filter and sort members
- Demo dataset (hardcoded in `script.js`)
- Shows activities of members when a member is selected 

### 5. Statistics
- Shows how many members each branch of the school has
- Shows how many activities are in each category
- This will be done with the static data in `script.js`,but then it will be done with the dinamic database that the webpage handles

### 6. Session Handling
- Active user is selected after a user is registered correctly
- Uses `localStorage` for `active user`
- Login state reflected across pages
- Logout support
- It will be added a password for users after the project starts being full-stack

---

## Project Structure

```
.
├── .gitignore
├── README.md
├── LICENSE
├── Tarea_1/
│   ├── index.html        # Home page
│   ├── register.html     # User registration
│   ├── activity.html     # Activity submission
│   ├── members.html      # Registered members and activities listing
│   ├── metrics.html      # Statistics
│   ├── script.js         # App logic
│   ├── styles.css        # Styling
```

---

## License

MIT License

---
