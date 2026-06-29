package com.example.tarea4spring.domain;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "miembro_id", nullable = false)
    private Miembro miembro;

    @Enumerated(EnumType.STRING)
    @Column(name = "dia", nullable = false, length = 20)
    private DiaEnum dia;

    @Column(name = "hora_inicio", nullable = false, length = 5)
    private String horaInicio;

    @Column(name = "duracion", nullable = false, length = 5)
    private String duracion;

    @Enumerated(EnumType.STRING)
    @Column(name = "tipo", nullable = false, length = 20)
    private TipoActividadEnum tipo;

    @Column(name = "nombre", nullable = false, length = 45)
    private String nombre;

    @Column(name = "descripcion", columnDefinition = "TEXT")
    private String descripcion;

    public Long getId() {
        return id;
    }

    public Miembro getMiembro() {
        return miembro;
    }

    public DiaEnum getDia() {
        return dia;
    }

    public String getHoraInicio() {
        return horaInicio;
    }

    public String getDuracion() {
        return duracion;
    }

    public TipoActividadEnum getTipo() {
        return tipo;
    }

    public String getNombre() {
        return nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public enum DiaEnum {
        lunes,
        martes,
        miércoles,
        jueves,
        viernes,
        sábado,
        domingo
    }

    public enum TipoActividadEnum {
        arte,
        deporte,
        tecnología,
        social,
        recreación,
        otra
    }
}
