import os
import oracledb as ora
from sqlalchemy import create_engine, MetaData, text, Column

metadata = MetaData()

engine = create_engine(
    "oracle+oracledb://",
    thick_mode=True,
    connect_args={
        "user": os.getenv("ORACLE_USER"),
        "password": os.getenv("ORACLE_PASSWORD"),
        "dsn": f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
    }
)

with engine.connect() as conn:

    sql = text("""
        WITH ATEND AS (
            SELECT CD_ATENDIMENTO, CD_PACIENTE, CD_CONVENIO, CD_PRESTADOR, DT_ATENDIMENTO
            FROM DBAMV.ATENDIME
            ORDER BY DT_ATENDIMENTO DESC
        )
        SELECT * FROM ATEND WHERE ROWNUM < 10
    """)

    # tb_atendimento = conn.execute(sql)      # ResultProxy
    # print(tb_atendimento)

    # registros = tb_atendimento.fetchall()   # ResultSet
    # print(registros)

    registros = conn.execute(sql).fetchmany(size=2) # Obter ResultSet com tamanho 2 de ResultProxy

    primeiro_registro = registros[0]          # Obter um registro
    primeira_coluna = primeiro_registro[0]    # Obter dado da primeira coluna

    print(conn.execute(sql).keys())           # Nome dos campos
    print(primeiro_registro)                  # Primeiro registro
    print(primeiro_registro.cd_atendimento)   # Obtendo codigo de atendimento
    print(primeira_coluna)
