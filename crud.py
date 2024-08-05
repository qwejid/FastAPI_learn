import asyncio

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import (
    db_helper,
    User,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAsociationTable,
)


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
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
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
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )

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


async def get_profiles_with_users_and_users_with_post(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == "John")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print("**" * 10)
        print("profile", profile.first_name)
        print("users", profile.user)
        print("users_with_posts", profile.user.posts)


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)

    session.add(order)
    await session.commit()

    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()

    return product


async def create_orderd_and_products(session: AsyncSession):
    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")

    mouse = await create_product(
        session=session,
        name="Mouse",
        description="Great gaming mouse",
        price=123,
    )

    keyboard = await create_product(
        session=session,
        name="Keyboard",
        description="Great gaming keyboard",
        price=149,
    )

    display = await create_product(
        session=session,
        name="Display",
        description="Office display",
        price=299,
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(selectinload(Order.products)),
    )

    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products)),
    )

    order_one.products.append(mouse)
    order_one.products.append(keyboard)

    order_promo.products.append(keyboard)
    order_promo.products.append(display)

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAsociationTable.product
            )
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session=session)
    for order in orders:
        print(f"Order {order.id} has products:")
        for product in order.products:
            print(f"- {product.name}")


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(f"Order {order.id} has products:")
        for order_product_details in order.products_details:
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty: ",
                order_product_details.count,
            )

async def create_gift_product_for_existing_orderd(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session=session,
        name="Gift",
        description="A gift for you",
        price=0,
    )

    for order in orders:
        order.products_details.append(
            OrderProductAsociationTable(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )

    await session.commit()


async def main_relations(session: AssertionError):
    await create_user(session=session, username="John", email="john@example.com")
    await create_user(session=session, username="Sam", email="sam@example.com")
    await create_user(session=session, username="Alice", email="alice@example.com")
    await get_user_by_username(session=session, username="sam")
    user_john = await get_user_by_username(session=session, username="John")
    user_alice = await get_user_by_username(session=session, username="Alice")
    await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name="John",
        last_name="Doe",
    )
    await create_user_profile(
        session=session,
        user_id=user_alice.id,
        first_name="Alice",
        last_name="Smith",
    )
    await show_users_with_profile(session=session)
    await create_posts(
        session,
        user_john.id,
        "SQLA 2.0",
        "SQLA Joins",
    )
    await create_posts(
        session,
        user_alice.id,
        "FastAPI Advanced",
        "FastAPI more",
    )
    await get_users_with_posts(session=session)
    await get_posts_with_autors(session=session)
    await get_users_with_posts_and_profiles(session=session)
    await get_profiles_with_users_and_users_with_post(session=session)


async def demo_m2m(session: AsyncSession):
    # await create_orderd_and_products
    # await demo_get_orders_with_products_through_secondary(session)
    
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orderd(session=session)
    


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
