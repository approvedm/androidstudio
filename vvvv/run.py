import asyncio
try:
    import usdt
    print("Checking function availability...")
    asyncio.run(usdt.track_and_send())
except AttributeError:
    print("Error: track_and_send function not found in module.")
except Exception as e:
    print(f"Error: {e}")
