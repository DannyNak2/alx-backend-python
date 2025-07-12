import asyncio
import aiosqlite

# ✅ Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

# ✅ Run both functions concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, older_users = results
    print("All Users:", all_users)
    print("Older Users:", older_users)

# ✅ Run the async operation
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
