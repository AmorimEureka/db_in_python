import os
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase

__engine: Optional[Engine] = None


def create_engine(sqlite: bool = False) -> Engine:

    """
        Engine padrão para configurar a interface do mecansmo
         de conexão com o PostreSQL, sendo possível utilizar sqlite
    """
    global __engine

    if __engine:
        return

    if sqlite:
        arquivo_db = 'db/picoles.sqlite'
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)

        conn_str = f'sqlite:///{arquivo_db}'
        __engine = sa.create_engine(
            url=conn_str,
            echo=False,
            connect_args={
                "check_same_thread": False
            }
        )
    else:
        conn_str = os.getenv("POSTGRES_STRING")
        __engine = sa.create_engine(
            url=conn_str,
            echo=True
        )

    return __engine


def create_session() -> Session:
    """
        Função para criar a sessao de conexao com banco de dados
    """

    global __engine

    if not __engine:
        create_engine(sqlite=True) # sem postgres, então create_engine(sqlite=True)

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session


def create_tables() -> None:
    """
        Funcao para criar, dropar ou recriar tabelas do banco de dados
    """

    global __engine

    if not __engine:
        create_engine(sqlite=True)  # sem postgres, então create_engine(sqlite=True)

    import models.__all__models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
