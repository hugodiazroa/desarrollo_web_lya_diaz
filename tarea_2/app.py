from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from datetime import datetime
import enum

app = Flask(__name__, template_folder="templates", static_folder="static")

# Database configuration
DATABASE_URI = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Enums for actividad
class DiaEnum(enum.Enum):
    lunes = 'lunes'
    martes = 'martes'
    miercoles = 'miércoles'
    jueves = 'jueves'
    viernes = 'viernes'
    sabado = 'sábado'
    domingo = 'domingo'

class TipoActividadEnum(enum.Enum):
    arte = 'arte'
    deporte = 'deporte'
    tecnologia = 'tecnología'
    social = 'social'
    recreacion = 'recreación'
    otra = 'otra'

# Models
class Region(Base):
    __tablename__ = 'region'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    comunas: Mapped[list["Comuna"]] = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey('region.id'), nullable=False)
    region: Mapped["Region"] = relationship("Region", back_populates="comunas")
    miembros: Mapped[list["Miembro"]] = relationship("Miembro", back_populates="comuna")

class Miembro(Base):
    __tablename__ = 'miembro'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    telefono: Mapped[str] = mapped_column(String(15), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    comuna_id: Mapped[int] = mapped_column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna: Mapped["Comuna"] = relationship("Comuna", back_populates="miembros")
    actividades: Mapped[list["Actividad"]] = relationship("Actividad", back_populates="miembro")

class Actividad(Base):
    __tablename__ = 'actividad'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    miembro_id: Mapped[int] = mapped_column(Integer, ForeignKey('miembro.id'), nullable=False)
    dia: Mapped[DiaEnum] = mapped_column(
        SAEnum(
            DiaEnum,
            values_callable=lambda enum: [e.value for e in enum],
            name='diaenum'
        ),
        nullable=False
    )
    hora_inicio: Mapped[str] = mapped_column(String(5), nullable=False)
    duracion: Mapped[str] = mapped_column(String(5), nullable=False)
    tipo: Mapped[TipoActividadEnum] = mapped_column(
        SAEnum(
            TipoActividadEnum,
            values_callable=lambda enum: [e.value for e in enum],
            name='tipoactividadenum'
        ),
        nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text(500), nullable=True)
    miembro: Mapped["Miembro"] = relationship("Miembro", back_populates="actividades")
    fotos: Mapped[list["Foto"]] = relationship("Foto", back_populates="actividad")

class Foto(Base):
    __tablename__ = 'foto'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    actividad_id: Mapped[int] = mapped_column(Integer, ForeignKey('actividad.id'), nullable=False)
    actividad: Mapped["Actividad"] = relationship("Actividad", back_populates="fotos")

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/metrics")
def metrics():
    return render_template("metrics.html")

@app.route("/members/<int:member_id>")
def member_detail(member_id):
    return render_template("member_detail.html", member_id=member_id)

# API endpoints
@app.route("/api/members")
def api_members():
    session = Session()
    try:
        miembros = session.query(Miembro).all()
        data = []
        for m in miembros:
            actividades = []
            for a in m.actividades:
                category_map = {
                    'arte': 'Artistic',
                    'deporte': 'Athletic',
                    'tecnologia': 'Tech',
                    'social': 'Social',
                    'recreacion': 'Recreational',
                    'otra': 'Other'
                }
                category = category_map.get(a.tipo.value, a.tipo.value)
                actividades.append({
                    'name': a.nombre,
                    'category': category,
                    'link': f'/activity/{a.id}'  # Todo: change this to random links
                })
            data.append({
                'id': m.id,
                'name': m.nombre,
                'type': m.tipo,
                'email': m.email,
                'activities': actividades
            })
        return jsonify(data)
    finally:
        session.close()

@app.route("/api/regions")
def api_regions():
    session = Session()
    try:
        regions = session.query(Region).order_by(Region.nombre).all()
        return jsonify([{'id': r.id, 'nombre': r.nombre} for r in regions])
    finally:
        session.close()

@app.route("/api/comunas")
def api_comunas():
    region_id = request.args.get('region_id', type=int)
    session = Session()
    try:
        query = session.query(Comuna)
        if region_id is not None:
            query = query.filter(Comuna.region_id == region_id)
        comunas = query.order_by(Comuna.nombre).all()
        return jsonify([{'id': c.id, 'nombre': c.nombre, 'region_id': c.region_id} for c in comunas])
    finally:
        session.close()

@app.route("/api/member/<int:member_id>")
def api_member(member_id):
    session = Session()
    try:
        miembro = session.query(Miembro).filter(Miembro.id == member_id).first()
        if not miembro:
            return jsonify({'error': 'Member not found'}), 404

        actividades = []
        for a in miembro.actividades:
            category_map = {
                'arte': 'Artistic',
                'deporte': 'Athletic',
                'tecnologia': 'Tech',
                'social': 'Social',
                'recreacion': 'Recreational',
                'otra': 'Other'
            }
            category = category_map.get(a.tipo.value, a.tipo.value)
            actividades.append({
                'id': a.id,
                'name': a.nombre,
                'category': category,
                'day': a.dia.value,
                'start_time': a.hora_inicio,
                'duration': a.duracion,
                'description': a.descripcion
            })

        return jsonify({
            'id': miembro.id,
            'name': miembro.nombre,
            'email': miembro.email,
            'phone': miembro.telefono,
            'type': miembro.tipo,
            'registration_date': miembro.fecha_registro.isoformat(),
            'comuna': miembro.comuna.nombre,
            'activities': actividades
        })
    finally:
        session.close()

@app.route("/api/metrics")
def api_metrics():
    session = Session()
    try:
        # Role counts
        from sqlalchemy import func
        role_query = session.query(Miembro.tipo, func.count(Miembro.id)).group_by(Miembro.tipo).all()
        roles = {tipo: count for tipo, count in role_query}

        # Activity counts
        activity_query = session.query(Actividad.tipo, func.count(Actividad.id)).group_by(Actividad.tipo).all()
        category_map = {
            'arte': 'Artistic',
            'deporte': 'Athletic',
            'tecnologia': 'Tech',
            'social': 'Social',
            'recreacion': 'Recreational',
            'otra': 'Other'
        }
        activities = {}
        for tipo, count in activity_query:
            category = category_map.get(tipo.value, tipo.value)
            activities[category] = count

        return jsonify({
            'roles': roles,
            'activities': activities
        })
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
