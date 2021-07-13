import os
from football_memories import create_app

if os.path.exists("env.py"):
    import env

app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
