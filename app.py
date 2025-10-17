import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

load_dotenv()

app = Flask(__name__)


try:
    genai.configure(api_key=os.getenv("AIzaSyCRNZayG9h0hePNNKNSwcETIA4c67yA3iA"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    
    model = None

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/review-code', methods=['POST'])
def review_code_handler():
    """Handles the file upload and code review request."""
    if not model:
        return jsonify({"error": "Generative AI model is not configured. Check API key."}), 500

    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        
        try:
            code_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return jsonify({"error": "Could not decode the file. Please ensure it is a plain text file."}), 400
        
        prompt = f"""
        Review the following code for readability, modularity, and potential bugs.
        Provide clear, actionable improvement suggestions formatted in Markdown.

        Code:
        ```
        {code_content}
        ```
        """
        
        try:
            response = model.generate_content(prompt)
            review_report = response.text
            
            return jsonify({"review_report": review_report})
            
        except Exception as e:
            return jsonify({"error": f"Error generating review from the AI model: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)