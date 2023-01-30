from api.api import app
from db.models import metadata, engine

if __name__ == '__main__':
    metadata.create_all(engine)
    app.run(debug=True)
