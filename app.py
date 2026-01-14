from flask import Flask, request, render_template, Response
import requests

app = Flask(__name__)

# =========================
# Coding Ninjas Details
# =========================
def coding_ninjas(uuid):
    url = f"https://www.naukri.com/code360/api/v3/public_section/profile/user_details?uuid={uuid}&app_context=publicsection&naukri_request=true"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://www.naukri.com/code360/profile/{uuid}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data['data']
            
            # Extract basic info
            name = data['profile']['name']
            badge_count = data['college_badges_data']['badge_count']
            dsa_stats = data['dsa_domain_data']['problem_count_data']
            
            # Create difficulty lookup
            diffs = {item['level']: item['count'] for item in dsa_stats['difficulty_data']}

            badges_hash = response_data.get('data', {}).get('dsa_domain_data', {}).get('badges_hash', {})

            extracted_badges = []
            for level, contents in badges_hash.items():
                topics = contents.get('ptm', [])
                for topic in topics:
                    extracted_badges.append({
                        'name': topic,
                        'level': level.capitalize()
                    })
            
            return {
                "name": name,
                "cnt": len(extracted_badges),
                "badge_count": badge_count,
                "total": dsa_stats['total_count'],
                "easy": diffs.get('Easy', 0),
                "moderate": diffs.get('Moderate', 0),
                "hard": diffs.get('Hard', 0)
            }

    except Exception as e:
        print(f"API Call Failed: {e}")
        return []

# =========================
# LeetCode Data Fetch
# =========================
def get_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userBadges($username: String!) {
      matchedUser(username: $username) {
        badges {
          name
          icon 
          hoverText
        }
      }
    }
    """
    payload = {"query": query, "variables": {"username": username}}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        badges = data['data']['matchedUser']['badges']

        # Fix relative icon URLs
        for badge in badges:
            if badge['icon'].startswith('/'):
                badge['icon'] = "https://leetcode.com" + badge['icon']
        return badges

    except Exception as e:
        print(f"Error: {e}")
        return []

# =========================
# Coding Ninjas Badges
# =========================
def get_live_coding_ninjas_badges(uuid):
    url = f"https://www.naukri.com/code360/api/v3/public_section/profile/user_details?uuid={uuid}&app_context=publicsection&naukri_request=true"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://www.naukri.com/code360/profile/{uuid}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            badges_hash = json_data.get('data', {}).get('dsa_domain_data', {}).get('badges_hash', {})
            
            extracted_badges = []
            for level, contents in badges_hash.items():
                topics = contents.get('ptm', [])
                for topic in topics:
                    extracted_badges.append({
                        'name': topic,
                        'level': level.capitalize()
                    })
            return extracted_badges
        return []
    except Exception as e:
        print(f"API Call Failed: {e}")
        return []

# =========================
# Routes
# =========================
@app.route("/")
def home():
    url = "https://api.github.com/users/parshotam94"
    try:
        res = requests.get(url)
        res.raise_for_status()
        git_data = res.json()
    except Exception as e:
        print("GitHub API Error:", e)
        git_data = {
            "name": "GitHub API Error",
            "html_url": "#",
            "avatar_url": "https://via.placeholder.com/150",
            "bio": "Could not fetch data",
            "public_repos": 0,
            "followers": 0
        }

    coding_ninjas_data = coding_ninjas("parshotam")
    leetcode_badges = get_leetcode_data("Prshotm")
    leetcode_badges_cnt = len(leetcode_badges)

    return render_template(
        "home.html",
        git_data=git_data,
        user=coding_ninjas_data,
        leetcode_badges_cnt=leetcode_badges_cnt
    )

@app.route("/projects")
def projects():
    url = "https://api.github.com/users/parshotam94/repos"
    try:
        res = requests.get(url)
        res.raise_for_status()
        git = res.json()
    except Exception as e:
        print("GitHub Error:", e)
        git = []
    return render_template("projects.html", git=git)

@app.route("/achievements")
def achievements():
    my_badges = get_leetcode_data("Prshotm")
    my_coding_ninjas_badges = get_live_coding_ninjas_badges("parshotam")
    return render_template(
        "achievements.html",
        badges=my_badges,
        cn_badges=my_coding_ninjas_badges
    )

# =========================
# Resume PDF Dynamic Serving
# =========================
GITHUB_REPO_API = "https://api.github.com/repos/parshotam94/resume/contents/"

@app.route("/resume.pdf")
def serve_resume():
    # Get list of files in the repo
    r = requests.get(GITHUB_REPO_API)
    if r.status_code != 200:
        return "Could not fetch repo contents", 500

    files = r.json()

    # Find the first PDF dynamically
    pdf_file = None
    for f in files:
        if f["name"].lower().endswith(".pdf"):
            pdf_file = f
            break

    if not pdf_file:
        return "No PDF found in repo", 404

    # Fetch PDF content
    pdf_url = pdf_file["download_url"]
    pdf_content = requests.get(pdf_url).content

    # Serve PDF inline
    return Response(
        pdf_content,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename={pdf_file['name']}"}
    )

@app.route("/resume")
def resume():
    return render_template("resume.html")

# =========================
# Main
# =========================
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
