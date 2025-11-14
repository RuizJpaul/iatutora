import os
from src import create_app

app = create_app()

if __name__ == "__main__":
    # Puerto dinámico para servicios en la nube (Render, Railway, etc.)
    port = int(os.getenv("PORT", 5000))
    # Host 0.0.0.0 permite conexiones externas
    app.run(host="0.0.0.0", port=port, debug=False)