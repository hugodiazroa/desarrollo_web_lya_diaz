from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from datetime import datetime
import enum
import re
import os
import json
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE_URI = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

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
    message = request.args.get('message')
    return render_template("index.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    form_data = {
        'name': '',
        'email': '',
        'phone': '',
        'type': '',
        'region_id': '',
        'comuna_id': ''
    }

    if request.method == "POST":
        region_id = request.form.get('region', type=int)
        comuna_id = request.form.get('comuna', type=int)
        form_data.update({
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'type': request.form.get('type', '').strip(),
            'region_id': region_id if region_id is not None else '',
            'comuna_id': comuna_id if comuna_id is not None else ''
        })

        if not form_data['name']:
            errors.append('Name is required.')
        if not form_data['email']:
            errors.append('Email is required.')
        elif not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', form_data['email']):
            errors.append('Email must be valid.')
        if not form_data['phone']:
            errors.append('Phone is required.')
        elif not re.match(r'^\+?\d{1,15}$', form_data['phone']):
            errors.append('Phone must be up to 15 digits and may start with +.')
        if not form_data['type']:
            errors.append('Type is required.')
        if region_id is None:
            errors.append('Region is required.')
        if comuna_id is None:
            errors.append('Comuna is required.')

        session = Session()
        try:
            comuna = None
            if comuna_id is not None:
                comuna = session.query(Comuna).filter(Comuna.id == comuna_id).first()
                if not comuna:
                    errors.append('Selected comuna is invalid.')
                elif region_id is not None and comuna.region_id != region_id:
                    errors.append('Selected comuna does not match the selected region.')

            if not errors:
                miembro = Miembro(
                    nombre=form_data['name'],
                    email=form_data['email'],
                    telefono=form_data['phone'],
                    tipo=form_data['type'],
                    comuna_id=comuna_id
                )
                session.add(miembro)
                session.commit()
                return redirect(url_for('index', message='Member registered successfully'))
        except Exception:
            session.rollback()
            errors.append('Unable to save registration. Please try again.')
        finally:
            session.close()

    return render_template("register.html", errors=errors, form_data=form_data)

@app.route("/activity", methods=["GET", "POST"])
def activity():
    errors = []
    form_data = {
        'activity_name': '',
        'category': '',
        'link': '',
        'schedule_items': []
    }

    if request.method == "POST":
        member_name = request.form.get('member_name', '').strip()
        form_data.update({
            'activity_name': request.form.get('activity_name', '').strip(),
            'category': request.form.get('category', '').strip(),
            'link': request.form.get('link', '').strip()
        })

        schedule_json = request.form.get('schedules', '[]')
        try:
            schedule_items = json.loads(schedule_json)
            if not isinstance(schedule_items, list):
                schedule_items = []
        except json.JSONDecodeError:
            schedule_items = []
        form_data['schedule_items'] = schedule_items

        if not member_name:
            errors.append('Member must be registered to report an activity.')
        if not form_data['activity_name']:
            errors.append('Activity name is required.')
        if not form_data['category']:
            errors.append('Activity category is required.')
        if not schedule_items:
            errors.append('At least one schedule is required.')

        category_map = {
            'Artistic': 'arte',
            'Athletic': 'deporte',
            'Tech': 'tecnología',
            'Social': 'social',
            'Recreational': 'recreación'
        }
        day_map = {
            'Monday': 'lunes',
            'Tuesday': 'martes',
            'Wednesday': 'miércoles',
            'Thursday': 'jueves',
            'Friday': 'viernes',
            'Saturday': 'sábado',
            'Sunday': 'domingo'
        }

        if form_data['category'] not in category_map:
            errors.append('Invalid activity category.')

        valid_schedules = []
        for idx, item in enumerate(schedule_items, start=1):
            if not isinstance(item, dict):
                errors.append(f'Schedule entry {idx} is invalid.')
                continue
            day = item.get('day', '')
            hour = item.get('hour', '')
            minute = item.get('minute', '')
            duration = item.get('duration', '')

            if not day or not hour or not minute or not duration:
                errors.append(f'Schedule entry {idx} must include day, hour, minute, and duration.')
                continue
            if day not in day_map:
                errors.append(f'Schedule entry {idx} includes invalid day.')
            if not hour.isdigit() or not (0 <= int(hour) <= 23):
                errors.append(f'Schedule entry {idx} includes invalid hour.')
            if not minute.isdigit() or not (0 <= int(minute) <= 59):
                errors.append(f'Schedule entry {idx} includes invalid minute.')
            if not str(duration).isdigit() or not (1 <= int(duration) <= 240):
                errors.append(f'Schedule entry {idx} duration must be between 1 and 240 minutes.')

            if not errors:
                valid_schedules.append({
                    'day': day_map[day],
                    'hour': f"{int(hour):02d}:{int(minute):02d}",
                    'duration': str(duration)
                })

        if form_data['link']:
            if not re.match(r'^(https?:\/\/)?[\w-]+(\.[\w-]+)+([\/\w\- .?%&=]*)?$', form_data['link']):
                errors.append('Activity link must be a valid URL.')

        files = [f for f in request.files.getlist('photos') if f and f.filename]
        if not files:
            errors.append('At least one image or video file is required.')
        elif len(files) > 8:
            errors.append('You can upload at most 8 files.')

        session = Session()
        try:
            miembro = None
            if member_name and not errors:
                miembro = session.query(Miembro).filter(Miembro.nombre == member_name).first()
                if not miembro:
                    errors.append('Registered member was not found.')

            if not errors:
                saved_files = []
                for upload in files:
                    filename = secure_filename(upload.filename)
                    if not filename:
                        continue
                    unique_name = f"{uuid.uuid4().hex}_{filename}"
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                    upload.save(upload_path)
                    saved_files.append({
                        'ruta_archivo': '/static/uploads/',
                        'nombre_archivo': unique_name
                    })

                for schedule in valid_schedules:
                    actividad = Actividad(
                        miembro_id=miembro.id,
                        dia=schedule['day'],
                        hora_inicio=schedule['hour'],
                        duracion=schedule['duration'],
                        tipo=category_map[form_data['category']],
                        nombre=form_data['activity_name'],
                        descripcion=None
                    )
                    session.add(actividad)
                    session.flush()

                    for saved in saved_files:
                        foto = Foto(
                            ruta_archivo=saved['ruta_archivo'],
                            nombre_archivo=saved['nombre_archivo'],
                            actividad_id=actividad.id
                        )
                        session.add(foto)

                session.commit()
                return redirect(url_for('index', message='Activity registered successfully'))
        except Exception:
            session.rollback()
            errors.append('Unable to save activity registration. Please try again.')
        finally:
            session.close()

    return render_template("activity.html", errors=errors, form_data=form_data, schedule_items=form_data['schedule_items'])

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
                'description': a.descripcion,
                'image': (a.fotos[0].ruta_archivo + a.fotos[0].nombre_archivo) if a.fotos else None
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
