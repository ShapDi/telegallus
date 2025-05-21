from telegallus import settings


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def get_session_factory():
    if settings.TEST:
        test_engine = create_async_engine(
            url=settings.TEST_SQLALCHEMY_DATABASE_URL, echo=False
        )
        test_session_factory = async_sessionmaker(test_engine)
        return test_session_factory()
    else:
        engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URL, echo=False)
        session_factory = async_sessionmaker(engine)
        return session_factory()