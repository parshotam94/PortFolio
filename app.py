from flask import Flask, render_template, Response
import requests
import os

app = Flask(__name__)

# =========================
# GitHub API Helper
# =========================
def github_get(url):
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"token {token}"

    return requests.get(url, headers=headers, timeout=10)

# =========================
# Coding Ninjas Details
# =========================
def coding_ninjas(uuid):
    url = f"https://www.naukri.com/code360/api/v3/public_section/profile/user_details?uuid={uuid}&app_context=publicsection&naukri_request=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://www.naukri.com/code360/profile/{uuid}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get("data", {})

            name = data.get("profile", {}).get("name", "")
            badge_count = data.get("college_badges_data", {}).get("badge_count", 0)
            dsa_stats = data.get("dsa_domain_data", {}).get("problem_count_data", {})

            diffs = {
                item["level"]: item["count"]
                for item in dsa_stats.get("difficulty_data", [])
            }

            badges_hash = data.get("dsa_domain_data", {}).get("badges_hash", {})

            extracted_badges = []
            for level, contents in badges_hash.items():
                for topic in contents.get("ptm", []):
                    extracted_badges.append({
                        "name": topic,
                        "level": level.capitalize()
                    })

            return {
                "name": name,
                "cnt": len(extracted_badges),
                "badge_count": badge_count,
                "total": dsa_stats.get("total_count", 0),
                "easy": diffs.get("Easy", 0),
                "moderate": diffs.get("Moderate", 0),
                "hard": diffs.get("Hard", 0)
            }

    except Exception as e:
        print("Coding Ninjas API Error:", e)

    return {}

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
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        badges = (
            data.get("data", {})
                .get("matchedUser", {})
                .get("badges", [])
        )

        for badge in badges:
            if badge.get("icon", "").startswith("/"):
                badge["icon"] = "https://leetcode.com" + badge["icon"]

        return badges

    except Exception as e:
        print("LeetCode API Error:", e)
        return []

# =========================
# Coding Ninjas Badges
# =========================
def get_live_coding_ninjas_badges(uuid):
    url = f"https://www.naukri.com/code360/api/v3/public_section/profile/user_details?uuid={uuid}&app_context=publicsection&naukri_request=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://www.naukri.com/code360/profile/{uuid}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            badges_hash = data.get("dsa_domain_data", {}).get("badges_hash", {})

            extracted_badges = []
            for level, contents in badges_hash.items():
                for topic in contents.get("ptm", []):
                    extracted_badges.append({
                        "name": topic,
                        "level": level.capitalize()
                    })

            return extracted_badges

    except Exception as e:
        print("Coding Ninjas Badge Error:", e)

    return []

# =========================
# Routes
# =========================
@app.route("/")
def home():
    try:
        res = github_get("https://api.github.com/users/parshotam94")
        res.raise_for_status()
        git_data = res.json()
    except Exception as e:
        print("GitHub Profile Error:", e)
        git_data = {
            "name": "GitHub API Error",
            "html_url": "#",
            "avatar_url": "https://via.placeholder.com/150",
            "bio": "Could not fetch data",
            "public_repos": 0,
            "followers": 0
        }

    return render_template(
        "home.html",
        git_data=git_data,
        user=coding_ninjas("parshotam"),
        leetcode_badges_cnt=len(get_leetcode_data("Prshotm"))
    )

@app.route("/projects")
def projects():
    try:
        res = github_get("https://api.github.com/users/parshotam94/repos")
        res.raise_for_status()
        git = sorted(res.json(), key=lambda x: x["updated_at"], reverse=True)
    except Exception as e:
        print("GitHub Repos Error:", e)
        git = []

    return render_template("projects.html", git=git)

@app.route("/achievements")
def achievements():
    return render_template(
        "achievements.html",
        badges=get_leetcode_data("Prshotm"),
        cn_badges=get_live_coding_ninjas_badges("parshotam")
    )

# =========================
# Resume PDF Dynamic Serving
# =========================
GITHUB_REPO_API = "https://api.github.com/repos/parshotam94/resume/contents/"

@app.route("/resume.pdf")
def serve_resume():
    try:
        r = github_get(GITHUB_REPO_API)
        r.raise_for_status()

        files = r.json()
        pdf_file = next(
            (f for f in files if f["name"].lower().endswith(".pdf")),
            None
        )

        if not pdf_file:
            return "No PDF found", 404

        pdf_content = requests.get(pdf_file["download_url"], timeout=10).content

        return Response(
            pdf_content,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={pdf_file['name']}"
            }
        )

    except Exception as e:
        print("Resume API Error:", e)
        return "Could not load resume", 500

@app.route("/resume")
def resume():
    return render_template("resume.html")

# =========================
# Main
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
