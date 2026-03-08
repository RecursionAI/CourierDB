import uvicorn
import argparse


WS_CHOICES = ("auto", "none", "websockets", "websockets-sansio", "wsproto")


def main():
    parser = argparse.ArgumentParser(description="CourierDB CLI")
    parser.add_argument("command", choices=["start"], help="Command to run")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument(
        "--ws",
        default="websockets-sansio",
        choices=WS_CHOICES,
        help="WebSocket protocol backend (default: websockets-sansio)",
    )

    args = parser.parse_args()

    if args.command == "start":
        print(f"🚀 Starting CourierDB Server on http://{args.host}:{args.port}...")
        uvicorn.run(
            "courierdb.server.app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            ws=args.ws,
        )
        print(f"🚀 CourierDB Server started on http://{args.host}:{args.port}")

if __name__ == "__main__":
    main()
