package com.example.tarea4spring.dto;

public class ActivitySearchResult {

    private final Long id;
    private final String memberName;
    private final String day;
    private final String type;
    private final String municipality;
    private final String name;
    private final String description;

    public ActivitySearchResult(Long id, String memberName, String day, String type, String municipality, String name, String description) {
        this.id = id;
        this.memberName = memberName;
        this.day = day;
        this.type = type;
        this.municipality = municipality;
        this.name = name;
        this.description = description;
    }

    public Long getId() {
        return id;
    }

    public String getMemberName() {
        return memberName;
    }

    public String getDay() {
        return day;
    }

    public String getType() {
        return type;
    }

    public String getMunicipality() {
        return municipality;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }
}
