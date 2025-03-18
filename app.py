from flask import Flask, request, redirect, render_template, jsonify # type: ignore
import hashlib

app = Flask(__name__)

# Store the URLs (using a dictionary for simplicity)
url_database = {}

# Function to generate a short URL
def generate_short_url(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]  # Generate a 6-character short URL

@app.route('/')
def home():
    return render_template('index.html')  # Renders the HTML form

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']  # Get URL from form input
    custom_alias = request.form.get('alias')  # Get custom alias from the form (optional)
    
    # If no custom alias provided, generate one
    if not custom_alias:
        short_url = generate_short_url(long_url)
    else:
        # If alias already exists, use it; otherwise, store it as a new alias
        if custom_alias in url_database:
            return jsonify({'error': 'Custom alias already taken. Please choose another one.'}), 400
        short_url = custom_alias
    
    # Store the mapping (custom alias or generated short URL)
    url_database[short_url] = long_url

    return jsonify({'short_url': f'http://127.0.0.1:5000/{short_url}'})  # Return shortened URL

@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = url_database.get(short_url)
    
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found!", 404

if __name__ == "__main__":
    app.run(debug=True)
