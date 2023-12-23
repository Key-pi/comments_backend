import os
from pathlib import Path
from server.protocol_router import asgi_app
import uvicorn

import settings

if __name__ == "__main__":
    reload_dir = Path(__file__).resolve().parent.parent  # backend
    """Django 3 does not support lifespan protocol. If you need to use lifespan signals use django signals natively"""
    print(f'https://{settings.SERVER_URL}')

    uvicorn.run(
        'server.protocol_router:asgi_app',
        host="0.0.0.0", port=8000,
        reload=True,
        # reload_dirs=[reload_dir],
        workers=5
    )
