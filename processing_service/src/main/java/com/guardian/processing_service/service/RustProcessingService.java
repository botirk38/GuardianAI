package com.guardian.processing_service.service;

import org.springframework.stereotype.Service;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import com.guardian.processing_service.antlr.rust.RustLexer;
import com.guardian.processing_service.antlr.rust.RustParser;
import com.guardian.processing_service.models.CodeSample;

@Service
public class RustProcessingService {

    public RustProcessingService() {
    }

    public String processCode(CodeSample codeSample) {

        if (codeSample == null || !codeSample.getLanguage().equals("rust")) {
            throw new IllegalArgumentException("Invalid code sample or language not supported");
        }

        CharStream input = CharStreams.fromString(codeSample.getCode());

        RustLexer lexer = new RustLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        RustParser parser = new RustParser(tokens);

        ParseTree tree = parser.crate();

        return tree.toStringTree(parser);
    }

}
