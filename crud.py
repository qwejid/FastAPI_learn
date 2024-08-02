import asyncio

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Product, Post


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
) -> User:
    user = User(username=username, email=email)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("Found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars().all()
    users = await session.scalars(stmt)
    for user in users:
        print("User:", user)
        print("Profile:", user.profile.first_name)
    # return list(users)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print("Posts created:", posts)
    return posts

async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        # joinedload(User.posts),
        selectinload(User.posts),
        ).order_by(User.id)
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    # users = result.scalars()

    users = await session.scalars(stmt)
    
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)

async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):    
    stmt = select(User).options(
        joinedload(User.profile),
        selectinload(User.posts),
        ).order_by(User.id)
    
    users = await session.scalars(stmt)
    
    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)
    
async def get_posts_with_autors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    
    for post in posts:
        print("**" * 10)
        print("post", post)
        print("author", post.user)

async def get_profiles_with_users_and_users_with_post(session:AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts)
        )
        .where(User.username == 'John')
        .order_by(Profile.id)
    )
    
    profiles = await session.scalars(stmt)
    
    for profile in profiles:
        print("**" * 10)
        print("profile", profile.first_name)
        print("users", profile.user)
        print("users_with_posts", profile.user.posts)

async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="John", email="john@example.com")
        # await create_user(session=session, username="Sam", email="sam@example.com")
        # await create_user(session=session, username="Alice", email="alice@example.com")
        # await get_user_by_username(session=session, username="sam")
        # user_john = await get_user_by_username(session=session, username="John")
        # user_alice = await get_user_by_username(session=session, username="Alice")

        # await create_user_profile(
        #     session=session,
        #     user_id=user_john.id,
        #     first_name="John",
        #     last_name="Doe",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_alice.id,
        #     first_name="Alice",
        #     last_name="Smith",
        # )
        # await show_users_with_profile(session=session)
        # await create_posts(
        #     session,
        #     user_john.id,
        #     "SQLA 2.0",
        #     "SQLA Joins",
        # )
        # await create_posts(
        #     session,
        #     user_alice.id,
        #     "FastAPI Advanced",
        #     "FastAPI more",
        # )
        # await get_users_with_posts(session=session)
        # await get_posts_with_autors(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_post(session=session)


if __name__ == "__main__":
    asyncio.run(main())
