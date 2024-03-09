package com.guardian.processing_service.models;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class RustCodeSampleTest {

    @Test
    public void testGetCode() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals("code", sample.getCode());
    }

    @Test
    public void testGetCodeNull() {
        RustCodeSample sample = new RustCodeSample(null, 1, "repo", "language", "path", "license");
        assertEquals(null, sample.getCode());
    }

    @Test
    public void testGetSize() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals(1, sample.getSize());
    }

    @Test
    public void testGetSizeZero() {
        RustCodeSample sample = new RustCodeSample("code", 0, "repo", "language", "path", "license");
        assertEquals(0, sample.getSize());
    }

    @Test
    public void testGetRepo() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals("repo", sample.getRepo());
    }

    @Test
    public void testGetLanguage() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals("language", sample.getLanguage());
    }

    @Test
    public void testGetPath() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals("path", sample.getPath());
    }

    @Test
    public void testGetLicense() {
        RustCodeSample sample = new RustCodeSample("code", 1, "repo", "language", "path", "license");
        assertEquals("license", sample.getLicense());
    }
}