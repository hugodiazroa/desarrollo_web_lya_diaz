package com.example.tarea4spring.domain;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "region")
public class Region {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    @OneToMany(mappedBy = "region", fetch = FetchType.LAZY)
    private List<Comuna> comunas;

    public Long getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public List<Comuna> getComunas() {
        return comunas;
    }
}
