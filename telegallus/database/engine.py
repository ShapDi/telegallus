from telegallus.settings import parameters_col


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def get_session_factory():
    test_engine = create_async_engine(
        url=f"postgresql+asyncpg://{parameters_col.USER_DATABASE}:{parameters_col.PASSWORD_DATABASE}@{parameters_col.HOST_DATABASE}:{parameters_col.PORT_DATABASE}/{parameters_col.NAME_DATABASE}", echo=False
    )
    session_factory = async_sessionmaker(test_engine)
    return session_factory()
