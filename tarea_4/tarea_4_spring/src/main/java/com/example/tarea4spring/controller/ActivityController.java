package com.example.tarea4spring.controller;

import com.example.tarea4spring.dto.ActivitySearchResult;
import com.example.tarea4spring.repository.ActividadRepository;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Collections;
import java.util.List;

@Controller
public class ActivityController {

    private final ActividadRepository actividadRepository;

    public ActivityController(ActividadRepository actividadRepository) {
        this.actividadRepository = actividadRepository;
    }

    @GetMapping("/activities")
    public String activitiesPage() {
        return "activities";
    }

    @GetMapping("/api/activities/search")
    @ResponseBody
    public List<ActivitySearchResult> searchActivities(@RequestParam(name = "q", required = false) String query) {
        if (query == null) {
            return Collections.emptyList();
        }

        String trimmed = query.trim();
        if (trimmed.length() < 3) {
            return Collections.emptyList();
        }

        String searchTerm = "%" + trimmed.toLowerCase() + "%";
        return actividadRepository.searchByNameDescriptionOrMunicipality(searchTerm);
    }
}
