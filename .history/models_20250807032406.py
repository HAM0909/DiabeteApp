from sqlalchemy import  Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pregnancies = Column(Integer)
    glucose = Column(Integer)
    bmi = Column(Float)
    age = Column(Integer)
    diabete_pedigree = Column(Float)
    result = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    prediction = relationship("")