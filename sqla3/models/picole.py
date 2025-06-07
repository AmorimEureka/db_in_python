import sqlalchemy as sa
import sqlalchemy.orm as orm

from datetime import datetime
from typing import List, Optional

from models.model_base import ModelBase

from models.sabor import Sabor
from models.tipo_embalage import TipoEmbalage
from models.tipo_picole import TipoPicole

from models.aditivo_nutritivo import AditivoNutritivo
from models.conservante import Conservante
from models.ingrediente import Ingrediente


aditivivos_nutritivos_picole = sa.Table(
    'aditivivos_nutritivos_picole',
    ModelBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('id_aditivo_nutritivo', sa.Integer, sa.ForeignKey('aditivos_nutritivos.id')),
    sa.Column('id_picole', sa.Integer, sa.ForeignKey('picoles.id'))
)


conservantes_picoles = sa.Table(
    'conservantes_picoles',
    ModelBase.metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('id_conservante', sa.Integer, sa.ForeignKey('conservantes.id')),
    sa.Column('id_picole', sa.Integer, sa.ForeignKey('picoles.id'))
)


ingredientes_picole = sa.Table(
    'ingredientes_picole',
    ModelBase.metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('id_ingrediente', sa.Integer, sa.ForeignKey('ingredientes.id')),
    sa.Column('id_picole', sa.Integer, sa.ForeignKey('picoles.id'))
)


class Picole(ModelBase):
    __tablename__: str = 'picoles'

    id: int = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    preco: float = sa.Column(sa.DECIMAL(8,2), nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)


    id_sabor: int = sa.Column(sa.Integer, sa.ForeignKey('sabores.id'))
    sabor: Sabor = orm.relationship('Sabor', lazy='joined')

    id_tipo_embalagem: int = sa.Column(sa.Integer, sa.ForeignKey('tipos_embalagem.id'))
    tipo_embalagem: TipoEmbalage = orm.relationship('TipoEmbalage', lazy='joined')

    id_tipo_picole: int = sa.Column(sa.Integer, sa.ForeignKey('tipos_picole.id'))
    tipo_picole: TipoPicole = orm.relationship('TipoPicole', lazy='joined')


    picoles_aditivos_nutritivos: Optional[AditivoNutritivo] = orm.relationship(
        'aditivos_nutritivos',
        secondary=aditivivos_nutritivos_picole,
        backref='aditivos_nutrivos',
        lazy='dynamic')

    picoles_conservantes: Optional[Conservante] = orm.relationship(
        'conservantes',
        secondary=conservantes_picoles,
        backref='conservantes',
        lazy='dynamic')

    picoles_ingredientes: List[Ingrediente] = orm.relationship(
        'ingredientes',
        secondary=ingredientes_picole,
        backref='ingredientes',
        lazy='dynamic')

    def __repr__(self) -> str:
        return f"<>Picole: {self.tipo_picole.nome} com sabor de: {self.sabor.nome}, valor: {self.preco}"
