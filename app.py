from flask import Flask, render_template, request, jsonify
import wikipedia
import re  # For regex to identify simple formulas

app = Flask(__name__)

# Function to replace the formula from Wikipedia with LaTeX
def format_formula(summary):
    # Define common formulas and their LaTeX equivalents
    formulas = {
        "a^2 + b^2 = c^2": "$$a^2 + b^2 = c^2$$"  # LaTeX formatted
    }
    
    # Replace formulas found in the text
    for formula, latex_formula in formulas.items():
        summary = re.sub(re.escape(formula), latex_formula, summary)
    
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question')

        # Fetch Wikipedia summary
        summary = wikipedia.summary(question, sentences=5)  # Fetch 5 sentences from Wikipedia

        # Format summary to replace any formulas with LaTeX
        formatted_summary = format_formula(summary)

        response = f"{formatted_summary}\n\nRead more: https://en.wikipedia.org/wiki/{question.replace(' ', '_')}"
        
        return jsonify({'response': response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'An error occurred. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)
