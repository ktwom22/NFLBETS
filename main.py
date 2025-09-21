from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQzkiku2N0QWoW05DP189iwYhYmIqHUPGyrjvCJVqlAEq5hglWg0CBGhpefSZziNXKiQHs_-9g2PKro/pub?gid=1306441773&single=true&output=csv"

def load_data():
    df = pd.read_csv(CSV_URL)
    df = df.fillna("")  # Replace NaN
    df = df[(df["Home Team"] != "") & (df["Away Team"] != "")]
    return df

@app.route("/")
def index():
    df = load_data()
    games = df.to_dict(orient="records")

    template = """
    <!doctype html>
    <html lang="en">
    <head>
        <title>NFL Matchups & My Picks</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .flip-card { background-color: transparent; perspective: 1000px; margin: 20px; cursor: pointer; }
            .flip-card-inner {
                position: relative;
                width: 100%;
                height: 250px;
                text-align: center;
                transition: transform 0.6s;
                transform-style: preserve-3d;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                border-radius: 15px;
            }
            .flip-card.flip .flip-card-inner {
                transform: rotateY(180deg);
            }
            .flip-card-front, .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                -webkit-backface-visibility: hidden;
                backface-visibility: hidden;
                border-radius: 15px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 10px;
            }
            .flip-card-front { background-color: #ffffff; color: black; }
            .flip-card-back { background-color: #007bff; color: white; transform: rotateY(180deg); }
            .team-logo { max-height: 50px; margin-bottom: 5px; }
            .my-pick-text { font-weight: bold; color: white; background-color: green; padding: 5px 10px; border-radius: 5px; margin-top: 10px; display: inline-block;}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const cards = document.querySelectorAll('.flip-card');
                cards.forEach(card => {
                    card.addEventListener('click', function() {
                        card.classList.toggle('flip');
                    });
                });
            });
        </script>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center my-4">NFL Matchups & My Picks</h1>
            <div class="row">
                {% for game in games %}
                <div class="col-md-6">
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <!-- Front -->
                            <div class="flip-card-front">
                                <div class="row align-items-center w-100">
                                    <div class="col text-center">
                                        {% if game['Away Logo'] %}
                                        <img src="{{ game['Away Logo'] }}" class="team-logo"><br>
                                        {% endif %}
                                        <strong>{{ game['Away Team'] }}</strong><br>
                                        {% if game['Away Final Points'] %}<span>{{ game['Away Final Points'] }}</span>{% endif %}
                                        {% if game['My Pick'] == game['Away Team'] %}
                                        <div class="my-pick-text">My Pick</div>
                                        {% endif %}
                                    </div>
                                    <div class="col text-center">
                                        <h4>at</h4>
                                    </div>
                                    <div class="col text-center">
                                        {% if game['Home Logo'] %}
                                        <img src="{{ game['Home Logo'] }}" class="team-logo"><br>
                                        {% endif %}
                                        <strong>{{ game['Home Team'] }}</strong><br>
                                        {% if game['Home Final Points'] %}<span>{{ game['Home Final Points'] }}</span>{% endif %}
                                        {% if game['My Pick'] == game['Home Team'] %}
                                        <div class="my-pick-text">My Pick</div>
                                        {% endif %}
                                    </div>
                                </div>
                                {% if game['My Pick'] %}
                                <hr>
                                <p>Predicted Winner: <strong>{{ game['My Pick'] }}</strong></p>
                                {% endif %}
                            </div>
                            <!-- Back -->
                            <div class="flip-card-back">
                                {% if game['Rationale'] %}
                                <p>{{ game['Rationale'] }}</p>
                                {% else %}
                                <p>No rationale provided.</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, games=games)

if __name__ == "__main__":
    app.run(debug=True)
