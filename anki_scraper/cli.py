"""
Idea:

Basic CLI interaction (using typer)
Should have some command allowing to generate cards

Arguments:
    topic : str (required)
    num_of_cards : int (optional)
"""
import typer

app = typer.Typer()

@app.command()
def generate(topic : str, num_of_cards : int):
    print(f"Generated {num_of_cards} cards about {topic}")

@app.command()
def null():
    pass

if __name__ == "__main__":
    app()