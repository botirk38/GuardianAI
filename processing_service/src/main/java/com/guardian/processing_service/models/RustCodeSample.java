package com.guardian.processing_service.models;


public class RustCodeSample implements CodeSample{

    private String code;
    private int size;
    
    private String repo;
    private String language;
    private String path;
    private String license;


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




}
