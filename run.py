from app import create_app, db
from app.models import User, Asset

app = create_app()

if __name__ == "__main__":
    app.run()
