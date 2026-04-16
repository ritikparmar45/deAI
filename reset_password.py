import sys
import asyncio
from automate import run_automate

async def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python reset_password.py <email>")
        print("Example: python reset_password.py john@company.com")
        sys.exit(1)
    
    email = sys.argv[1]
    task = f"Reset password for {email}"
    
    print(f"🚀 Initializing reset password task for: {email}")
    await run_automate(task)

if __name__ == "__main__":
    asyncio.run(main())
