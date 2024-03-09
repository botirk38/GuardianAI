package com.guardian.processing_service.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import com.guardian.processing_service.antlr.RustLexer;
import com.guardian.processing_service.antlr.RustParser;
import com.guardian.processing_service.models.CodeSample;

@Service
public class ProcessingService {

    private final RestTemplate restTemplate;
    private final RustLexer lexer;
    private final RustParser parser;

    public ProcessingService(RestTemplate restTemplate, RustLexer lexer, RustParser parser) {
        this.restTemplate = restTemplate;
        this.lexer = lexer;
        this.parser = parser;
    }

    public void processCode(CodeSample codeSample) {
        String code = codeSample.getCode();
        CharStream input = CharStreams.fromString(code);

        lexer.setInputStream(input);

        CommonTokenStream tokens = new CommonTokenStream(lexer);

        parser.setTokenStream(tokens);

        ParseTree tree = parser.crate();

        System.out.println(tree.toStringTree(parser));

        
    }
    
}
