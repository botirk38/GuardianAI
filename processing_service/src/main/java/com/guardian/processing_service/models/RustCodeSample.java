package com.guardian.processing_service.models;

import java.io.Serializable;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RustCodeSample implements CodeSample, Serializable{

    private String code;
    private int size;
    @JsonProperty("repo_name")
    private String repo;
    private String language;
    private String path;
    private String license;

    public RustCodeSample() {
    }

    public RustCodeSample(String code, int size, String repo, String language, String path, String license) {

        this.code = code;
        this.size = size;
        this.repo = repo;
        this.language = language;
        this.path = path;
        this.license = license;

    }

    @Override
    public String getCode() {

        return code;
    }

    @Override
    public int getSize() {

        return size;

    }

    @Override
    public String getRepo() {

        return repo;
    }

    @Override
    public String getLanguage() {

        return language;
    }

    @Override
    public String getPath() {

        return path;
    }

    @Override
    public String getLicense() {

        return license;

    }

    @Override
    public String toString() {
        return "RustCodeSample{" +
                "language='" + language + '\'' +
                ", code='" + code + '\'' +
                ", size=" + size +
                ", repo='" + repo + '\'' +
                ", path='" + path + '\'' +
                ", license='" + license + '\'' +
                '}';
    }

}
