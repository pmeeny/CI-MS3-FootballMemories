import os
from football_memories import create_app

# Create an app
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
