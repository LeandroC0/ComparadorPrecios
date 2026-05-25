import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Numeric, Boolean, DateTime,
    ForeignKey, BigInteger, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Supermercado(Base):
    __tablename__ = "supermercados"

    id          = Column(String(30), primary_key=True)
    nombre      = Column(String(100), nullable=False)
    lat         = Column(Numeric(9, 6))
    lon         = Column(Numeric(9, 6))
    costo_viaje = Column(Numeric(8, 2), default=0)

    precios = relationship("Precio", back_populates="supermercado_rel")


class Categoria(Base):
    __tablename__ = "categorias"

    id        = Column(String(60), primary_key=True)
    nombre    = Column(String(100), nullable=False)

    productos = relationship("Producto", back_populates="categoria_rel")


class Producto(Base):
    __tablename__ = "productos"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre           = Column(String(255), nullable=False)
    categoria_id     = Column(String(60), ForeignKey("categorias.id"), nullable=True)
    url_walmart      = Column(Text)
    url_maxi_pali    = Column(Text)
    url_auto_mercado = Column(Text)
    url_pricesmart   = Column(Text)
    url_megasuper    = Column(Text)
    url_mayca        = Column(Text)
    activo           = Column(Boolean, default=True)
    creado_en        = Column(DateTime, default=datetime.utcnow)

    categoria_rel = relationship("Categoria", back_populates="productos")
    precios       = relationship("Precio", back_populates="producto")
    alertas       = relationship("Alerta", back_populates="producto")


class Precio(Base):
    __tablename__ = "precios"

    id                = Column(BigInteger, primary_key=True, autoincrement=True)
    producto_id       = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    supermercado      = Column(String(30), ForeignKey("supermercados.id"), nullable=False)
    precio            = Column(Numeric(10, 2), nullable=False)
    precio_por_unidad = Column(Numeric(10, 4))
    unidad            = Column(String(20))
    es_promo          = Column(Boolean, default=False)
    precio_minimo_30d = Column(Boolean, default=False)
    fecha_hora        = Column(DateTime, default=datetime.utcnow, index=True)

    producto         = relationship("Producto", back_populates="precios")
    supermercado_rel = relationship("Supermercado", back_populates="precios")


class Alerta(Base):
    __tablename__ = "alertas"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    tipo        = Column(String(30))
    umbral      = Column(Numeric(5, 2))
    canal       = Column(String(20))
    activa      = Column(Boolean, default=True)
    creado_en   = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="alertas")


class NotificacionEnviada(Base):
    __tablename__ = "notificaciones_enviadas"

    id                = Column(BigInteger, primary_key=True, autoincrement=True)
    alerta_id         = Column(UUID(as_uuid=True), ForeignKey("alertas.id"), nullable=False)
    precio_disparador = Column(Numeric(10, 2))
    canal             = Column(String(20))
    enviado_en        = Column(DateTime, default=datetime.utcnow)