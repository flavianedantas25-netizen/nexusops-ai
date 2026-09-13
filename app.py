import os

import uvicorn


if __name__ == "__main__":
    port = int(
        os.getenv(
            "SERVER_PORT",
            os.getenv("PORT", "8000"),
        )
    )

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=port,
    )
