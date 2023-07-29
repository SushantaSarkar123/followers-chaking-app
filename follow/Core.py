from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok  # Correct the function name here
from bs4 import BeautifulSoup

app = Flask(__name__)
run_with_ngrok(app)

def extract_profiles_from_html(file_content):
    soup = BeautifulSoup(file_content, 'html.parser')
    profiles = [a['href'] for a in soup.find_all('a', href=True)]
    return profiles

def find_profiles_not_in_followers(followers_file_content, followings_file_content):
    followers = extract_profiles_from_html(followers_file_content)
    followings = extract_profiles_from_html(followings_file_content)

    not_in_followers = [profile for profile in followings if profile not in followers]
    return not_in_followers

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    not_in_followers_list = []
    if request.method == 'POST':
        followers_file = request.files['followers_file']
        followings_file = request.files['followings_file']

        followers_content = followers_file.read().decode('utf-8')
        followings_content = followings_file.read().decode('utf-8')

        not_in_followers_list = find_profiles_not_in_followers(followers_content, followings_content)

    return render_template('index.html', not_in_followers=not_in_followers_list)

if __name__ == "__main__":
    app.run()


# if __name__ == "__main__":
#     app.run(debug=True)