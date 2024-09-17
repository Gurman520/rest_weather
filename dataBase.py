from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base
from support import get_weather_description, degrees_to_direction

Base = declarative_base()


# Класс, что описывает структуру таблицы в БД
class CurrentWeather(Base):
    __tablename__ = "current_weather"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String, nullable=False)
    apparent_temperature = Column(Float)
    precipitation_value = Column(Float)
    precipitation = Column(String)
    surface_pressure = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)


DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    '''
    Функция инициализации БД
    :return:
    '''
    Base.metadata.create_all(bind=engine)


def save_to_db(session, data):
    '''
    Функция записи новых значений в БД
    :param session:
    :param data: Данные для записи в БД
    :return:
    '''
    db = session()
    try:
        new_record = CurrentWeather(
            time=data['time'],
            apparent_temperature=data.get('apparent_temperature'),
            precipitation_value=data.get('precipitation'),
            precipitation=get_weather_description(data.get('weather_code')),
            surface_pressure=data.get('surface_pressure'),
            wind_speed=data.get('wind_speed_10m'),
            wind_direction=degrees_to_direction(data.get('wind_direction_10m')),
        )
        db.add(new_record)
        db.commit()
    finally:
        db.close()


def get_last_10_records(session):
    '''
    Функция получения данных из БД
    :param session:
    :return:
    '''
    with session() as db:
        records = db.query(CurrentWeather).order_by(CurrentWeather.id.desc()).limit(10).all()
        return records
