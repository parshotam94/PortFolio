This project is a **dynamic coding portfolio website** built with Flask and integrated with multiple API's.

# **Portfolio Website (Flask)**

A dynamic portfolio website built with **Flask** that showcases my coding journey, integrating APIs from **CodeForces, GitHub, LeetCode, GeeksforGeeks (GFG), Coding Ninjas**, and more. It also allows for **dynamic resume preview** directly from GitHub.


## **Table of Contents**

1. [Features](#features)
2. [Demo](#demo)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Usage](#usage)
7. [APIs Integrated](#apis-integrated)
8. [Dynamic Resume](#dynamic-resume)
9. [Future Enhancements](#future-enhancements)

## **Features**

* Display **GitHub profile** and repositories dynamically
* Show **LeetCode badges and solved problems**
* Fetch **Coding Ninjas DSA badges and statistics**
* Integrate other platforms like **GFG**
* Dynamic **resume PDF preview**
* Responsive **Flask-based web application**
* Auto-updates whenever APIs or resume are updated
* Modular and extendable design


## **Demo**

* Home Page: `/` → Shows GitHub, Coding Ninjas, and LeetCode stats
* Projects Page: `/projects` → Displays all GitHub repositories
* Achievements Page: `/achievements` → Shows coding badges
* Resume Page: `/resume` → Dynamic preview of your latest PDF
* Direct PDF: `/resume.pdf` → Inline PDF fetch

## **Tech Stack**

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, Jinja2 templates
* **APIs:** CodeForces, GitHub, LeetCode, Coding Ninjas, GFG
* **Other Tools:** `requests`, `gunicorn`

## **Project Structure**

```
my-flask-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile               # Render/Gunicorn start command
├── runtime.txt            # Python version for deployment
├── templates/             # HTML templates
│   ├── home.html
│   ├── projects.html
│   ├── achievements.html
│   └── resume.html
├── static/                #  CSS, images
```

---

## **Installation**

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run locally**

```bash
python app.py
```

* Open browser: `http://127.0.0.1:5000/` but first convert execution line to -> ```app.run(debug=True)```


## **Usage**

* **Home Page:** Displays GitHub profile info, LeetCode stats, CodeForces and Coding Ninjas statistics
* **Projects Page:** Shows all GitHub repositories
* **Achievements Page:** Shows coding badges from LeetCode and Coding Ninjas
* **Resume Page:** Embed my latest PDF dynamically using GitHub


## **APIs Integrated**

1. **GitHub API**

   * Fetch user profile: `https://api.github.com/users/<username>`
   * Fetch repositories: `https://api.github.com/users/<username>/repos`

2. **LeetCode GraphQL API**

   * Fetch badges and solved problems

3. **Coding Ninjas API**

   * Fetch DSA badges and problem statistics

4. **GFG:**
 
   * Fetch problem statistics

## **Dynamic Resume**

* Resume stored in GitHub repo
* Flask route `/resume.pdf` fetches the **latest PDF dynamically**
* Can rename the PDF; route will automatically detect it
* `/resume` page embeds PDF inline for browser preview

## **Future Enhancements**

* Add caching for API calls to reduce response time
* Add **analytics graphs** for solved problems over time
* Add **authentication** to personalize stats
* Improve mobile responsiveness and UI/UX
* Integrate more coding platforms (HackerRank, Codeforces, etc.)
