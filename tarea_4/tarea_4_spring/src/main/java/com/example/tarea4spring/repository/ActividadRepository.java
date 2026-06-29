package com.example.tarea4spring.repository;

import com.example.tarea4spring.dto.ActivitySearchResult;
import com.example.tarea4spring.domain.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ActividadRepository extends JpaRepository<Actividad, Long> {

    @Query("SELECT new com.example.tarea4spring.dto.ActivitySearchResult(a.id, m.nombre, a.dia, a.tipo, c.nombre, a.nombre, a.descripcion) " +
           "FROM Actividad a " +
           "JOIN a.miembro m " +
           "JOIN m.comuna c " +
           "WHERE LOWER(a.nombre) LIKE :term " +
           "OR LOWER(COALESCE(a.descripcion, '')) LIKE :term " +
           "OR LOWER(c.nombre) LIKE :term " +
           "ORDER BY a.nombre")
    List<ActivitySearchResult> searchByNameDescriptionOrMunicipality(@Param("term") String term);
}
