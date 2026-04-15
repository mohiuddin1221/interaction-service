import asyncio
import os
from database import get_async_db, redis_client
from sqlalchemy import insert
from src.like.models import PostLike



async def sync_likes_to_db():
    """Background task to fetch data from Redis, convert to list, and insert to DB."""
    while True:
        try:
            await asyncio.sleep(30)
            print("⏱️ [Sync Worker] Starting simple database sync...")

            async for db in get_async_db():
                likes_to_insert = []
                keys_to_delete = []

                async for key in redis_client.scan_iter("post:*:likes"):
                    post_uid = key.split(":")[1]
                    liked_users = await redis_client.smembers(key)

                    for user_data in liked_users:
                        user_uid, username = user_data.split(":")

                        likes_to_insert.append(
                            {
                                "post_uid": post_uid,
                                "user_uid": user_uid,
                                "username": username,
                            }
                        )

                    keys_to_delete.append(key)

                if likes_to_insert:
                    await db.execute(insert(PostLike), likes_to_insert)

                    await db.commit()
                    print(
                        f"➕ [DB Sync] Successfully inserted {len(likes_to_insert)} likes to DB."
                    )

                    for k in keys_to_delete:
                        await redis_client.delete(k)

                    print("🧹 [Redis] Processed keys cleared from Redis.")

        except Exception as e:
            print(f"❌ Error during sync: {e}")