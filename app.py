from flask import Flask, render_template, request, jsonify
from models import db, Thought, Alternative
import openai

# Initial API Key: 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
# Second API Key: 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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
db.init_app(app)

# Set up the GPT-3 API connection
openai.api_key = "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"

def generate_gpt3_response(prompt, model='text-davinci-002', n=1):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        n=n,
        max_tokens=100,
        temperature=0.8
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    thoughts = Thought.query.all()
    return render_template('index.html', thoughts=thoughts)

@app.route('/thoughts', methods=['GET', 'POST'])
def thoughts():
    if request.method == 'POST':
        content = request.json.get('content')
        if content:
            thought = Thought(content=content)
            db.session.add(thought)
            db.session.commit()
            return jsonify(id=thought.id, content=thought.content)
        return jsonify(error='Content is empty'), 400
    else:
        thoughts = Thought.query.all()
        return jsonify([{'id': t.id, 'content': t.content} for t in thoughts])

@app.route('/alternatives', methods=['POST'])
def generate_alternative():
    thought_id = request.json.get('thought_id')
    thought = Thought.query.get(thought_id)
    if not thought:
        return jsonify(error='Thought not found'), 404

    prompt = f"Alternative thought to: {thought.content}"
    alternative_text = generate_gpt3_response(prompt)
    alternative = Alternative(content=alternative_text, thought_id=thought_id)
    db.session.add(alternative)
    db.session.commit()
    return jsonify(id=alternative.id, content=alternative.content)

@app.route('/alternatives/<int:alt_id>/select', methods=['POST'])
def select_alternative(alt_id):
    alternative = Alternative.query.get(alt_id)
    if not alternative:
        return jsonify(error='Alternative not found'), 404

    alternative.selected = True
    db.session.commit()
    return jsonify(success=True)

@app.route('/alternatives/<int:alt_id>', methods=['PUT'])
def update_alternative(alt_id):
    alternative = Alternative.query.get(alt_id)
    if not alternative:
        return jsonify(error='Alternative not found'), 404

    new_content = request.json.get('content')
    if new_content:
        alternative.content = new_content
        alternative.selected = True
        db.session.commit()
        return jsonify(success=True)
    return jsonify(error='Content is empty'), 400

if __name__ == '__main__':
    app.run(debug=True)
