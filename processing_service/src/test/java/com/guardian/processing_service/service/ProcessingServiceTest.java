
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

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.json.JSONObject;


public class ProcessingServiceTest {

    @Mock
    private RustLexer lexer;

    @Mock
    private RustParser parser;

    @InjectMocks
    private ProcessingService processingService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }


    @Test
    public void testProcessCodeWithValidCodeSample() {
        ProcessingService service = new ProcessingService();
        CodeSample codeSample = new RustCodeSample("fn main() { println!(\"Hello World\"); }", 1, "repo", "rust", "path", "license");
        
        // Assuming the method is expected to return a non-empty string for valid Rust code
        JSONObject result = service.processCode(codeSample);
        assertNotNull(result);
        assertFalse(result.isEmpty());
    }

    @Test
    public void testProcessCodeWithInvalidLanguage() {
        ProcessingService service = new ProcessingService();
        CodeSample codeSample = new RustCodeSample("fn main() {}", 1, "repo", "not_rust", "path", "license");
        
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            service.processCode(codeSample);
        });

        assertEquals("Invalid code sample or language not supported", exception.getMessage());
    }

    @Test
public void testProcessCodeWithNullCodeSample() {
    ProcessingService service = new ProcessingService();
    Exception exception = assertThrows(IllegalArgumentException.class, () -> {
        service.processCode(null);
    });

    assertEquals("Invalid code sample or language not supported", exception.getMessage());
}

@Test
public void testProcessCodeWithEmptyCode() {
    ProcessingService service = new ProcessingService();
    CodeSample codeSample = new RustCodeSample("", 1, "repo", "rust", "path", "license");

    Exception exception = assertThrows(IllegalArgumentException.class, () -> {
        service.processCode(codeSample);
    });

    assertEquals("Invalid code sample or language not supported", exception.getMessage());
}

@Test
public void testBuildTreeWithNullTree() {
    ProcessingService service = new ProcessingService();
    RustParser parser = new RustParser(new CommonTokenStream(new RustLexer(CharStreams.fromString(""))));

    Exception exception = assertThrows(IllegalArgumentException.class, () -> {
        service.buildTree(null, parser);
    });

    assertEquals("Tree cannot be null", exception.getMessage());
}

@Test
public void testBuildTreeWithNullParser() {
    ProcessingService service = new ProcessingService();
    RustParser parser = new RustParser(new CommonTokenStream(new RustLexer(CharStreams.fromString(""))));
    ParseTree tree = parser.crate();

    Exception exception = assertThrows(IllegalArgumentException.class, () -> {
        service.buildTree(tree, null);
    });

    assertEquals("Parser cannot be null", exception.getMessage());
}


}