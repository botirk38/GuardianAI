
package com.guardian.processing_service.service;

import com.guardian.processing_service.antlr.rust.RustLexer;
import com.guardian.processing_service.antlr.rust.RustParser;
import com.guardian.processing_service.models.CodeSample;
import com.guardian.processing_service.models.RustCodeSample;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;


public class RustProcessingServiceTest {

    @Mock
    private RustLexer lexer;

    @Mock
    private RustParser parser;

    @InjectMocks
    private RustProcessingService processingService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }


    @Test
    public void testProcessCodeWithValidCodeSample() {
        RustProcessingService service = new RustProcessingService();
        CodeSample codeSample = new RustCodeSample("fn main() { println!(\"Hello World\"); }", 1, "repo", "rust", "path", "license");
        
        // Assuming the method is expected to return a non-empty string for valid Rust code
        String result = service.processCode(codeSample);
        assertNotNull(result);
        assertFalse(result.isEmpty());
    }

    @Test
    public void testProcessCodeWithInvalidLanguage() {
        RustProcessingService service = new RustProcessingService();
        CodeSample codeSample = new RustCodeSample("fn main() {}", 1, "repo", "not_rust", "path", "license");
        
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            service.processCode(codeSample);
        });

        assertEquals("Invalid code sample or language not supported", exception.getMessage());
    }


}