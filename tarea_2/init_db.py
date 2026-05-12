from app import engine, Base, Session, Region, Comuna, Miembro, Actividad, Foto
from datetime import datetime

# Create tables
Base.metadata.create_all(engine)

# Load region and comuna data
session = Session()

# Assuming region-comuna.sql is executed separately, or load manually
# For now, insert some sample data

# Regions (from region-comuna.sql summary)
regions_data = [
    (1, 'Región de Tarapacá'),
    (2, 'Región de Antofagasta'),
    (13, 'Región Metropolitana de Santiago'),
    # Add more as needed
]

for id_, nombre in regions_data:
    existing = session.query(Region).filter_by(id=id_).first()
    if not existing:
        region = Region(id=id_, nombre=nombre)
        session.add(region)

# Comunas
comunas_data = [
    (10301, 'Iquique', 1),
    (20101, 'Tocopilla', 2),
    (13101, 'Santiago', 13),
    # Add more
]

for id_, nombre, region_id in comunas_data:
    existing = session.query(Comuna).filter_by(id=id_).first()
    if not existing:
        comuna = Comuna(id=id_, nombre=nombre, region_id=region_id)
        session.add(comuna)

# Load static members from script.js
members_data = [
    {
        'name': 'Ana',
        'type': 'student_undergrad',
        'email': 'x@mail.com',
        'comuna_id': 10301,  # Example
        'activities': [
            {'dia': 'lunes', 'hora_inicio': '10:00', 'duracion': '60', 'tipo': 'tecnologia', 'nombre': 'Programar perros', 'descripcion': ''},
            {'dia': 'martes', 'hora_inicio': '14:00', 'duracion': '30', 'tipo': 'social', 'nombre': 'Pasear perros', 'descripcion': ''}
        ]
    },
    {
        'name': 'Luis',
        'type': 'faculty',
        'email': 'y@mail.com',
        'comuna_id': 20101,
        'activities': []
    },
    # Add the rest
]

for m_data in members_data:
    existing_member = session.query(Miembro).filter_by(email=m_data['email']).first()
    if existing_member:
        miembro = existing_member
    else:
        miembro = Miembro(
            nombre=m_data['name'],
            email=m_data['email'],
            telefono='123456789',  # Placeholder
            tipo=m_data['type'],
            comuna_id=m_data['comuna_id'],
            fecha_registro=datetime.utcnow()
        )
        session.add(miembro)
        session.flush()  # To get id

    for a_data in m_data['activities']:
        existing_activity = session.query(Actividad).filter_by(
            miembro_id=miembro.id,
            nombre=a_data['nombre'],
            hora_inicio=a_data['hora_inicio']
        ).first()
        if not existing_activity:
            actividad = Actividad(
                miembro_id=miembro.id,
                dia=a_data['dia'],
                hora_inicio=a_data['hora_inicio'],
                duracion=a_data['duracion'],
                tipo=a_data['tipo'],
                nombre=a_data['nombre'],
                descripcion=a_data['descripcion']
            )
            session.add(actividad)

session.commit()
session.close()

print("Database initialized.")