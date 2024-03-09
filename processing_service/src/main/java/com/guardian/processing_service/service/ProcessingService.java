package com.guardian.processing_service.service;

import org.springframework.stereotype.Service;


import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import com.guardian.processing_service.antlr.rust.RustLexer;
import com.guardian.processing_service.antlr.rust.RustParser;
import com.guardian.processing_service.models.CodeSample;

import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class ProcessingService {

    private final Logger logger = LoggerFactory.getLogger(ProcessingService.class);

    public ProcessingService() {
    }

    public JSONObject processCode(CodeSample codeSample) {

        if (codeSample == null || !codeSample.getLanguage().equals("rust") || codeSample.getCode().isEmpty()) {
            throw new IllegalArgumentException("Invalid code sample or language not supported");
        }

        CharStream input = CharStreams.fromString(codeSample.getCode());

        RustLexer lexer = new RustLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        RustParser parser = new RustParser(tokens);

        ParseTree tree = parser.crate();

        JSONObject json = buildTree(tree, parser);
        logger.debug("Tree: " + json.toString());

        return json;
    }

     JSONObject buildTree(ParseTree tree, RustParser parser) {

        if( tree == null ) {
            throw new IllegalArgumentException("Tree cannot be null");
        }

        if( parser == null ) {
            throw new IllegalArgumentException("Parser cannot be null");
        }

        JSONObject json = new JSONObject();
        json.put("name", parser.getRuleNames()[((RuleContext) tree).getRuleIndex()]);
        JSONArray children = new JSONArray();
        for (int i = 0; i < tree.getChildCount(); i++) {
            ParseTree child = tree.getChild(i);
            if (child instanceof RuleContext) {
                children.put(buildTree(child, parser));
            } else {
                JSONObject leaf = new JSONObject();
                leaf.put("name", child.toString());
                children.put(leaf);
            }
        }
        json.put("children", children);
        return json;
    }


}
