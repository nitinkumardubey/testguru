from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:Dubey%40421999@localhost:5432/postgres"
# DATABASE_URL = "postgresql://postgres_dhoc_user:owS0lTuGWkEAb9cfya2ijm7DuOasH0TY@dpg-d53ck875r7bs73do87u0-a.oregon-postgres.render.com/postgres_dhoc"
DATABASE_URL = "postgresql://postgres_dhoc_user:owS0lTuGWkEAb9cfya2ijm7DuOasH0TY@dpg-d53ck875r7bs73do87u0-a/postgres_dhoc"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
