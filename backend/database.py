from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------
# Database setup
# -------------------------
DATABASE_URL = "sqlite:///./finance.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# -------------------------
# Models
# -------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, date={self.date}, description={self.description}, amount={self.amount}, category={self.category})>"


# -------------------------
# Create tables
# -------------------------
Base.metadata.create_all(bind=engine)
