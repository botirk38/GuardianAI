package com.guardian.processing_service.service;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import com.guardian.processing_service.antlr.rust.RustLexer;
import com.guardian.processing_service.antlr.rust.RustParser;
import com.guardian.processing_service.models.CodeSample;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class ProcessingService {

    private final Logger logger = LoggerFactory.getLogger(ProcessingService.class);

    public ProcessingService() {
    }

    public Map<String, Object> processCode(CodeSample codeSample) {

        if (codeSample == null || !codeSample.getLanguage().equals("rust") || codeSample.getCode().isEmpty()) {
            throw new IllegalArgumentException("Invalid code sample or language not supported");
        }

        CharStream input = CharStreams.fromString(codeSample.getCode());

        RustLexer lexer = new RustLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        RustParser parser = new RustParser(tokens);

        ParseTree tree = parser.crate();

        Map<String, Object> json = buildTree(tree, parser);

        logger.debug("JSON: " + json.toString());

        return json;
    }

    Map<String, Object> buildTree(ParseTree tree, RustParser parser) {

        if (tree == null) {
            throw new IllegalArgumentException("Tree cannot be null");
        }

        if (parser == null) {
            throw new IllegalArgumentException("Parser cannot be null");
        }

        // Create a new map for the current node
        Map<String, Object> json = new HashMap<>();
        json.put("name", parser.getRuleNames()[((RuleContext) tree).getRuleIndex()]);

        // Check if the tree has children
        if (tree.getChildCount() > 0) {
            List<Map<String, Object>> children = new ArrayList<>();
            for (int i = 0; i < tree.getChildCount(); i++) {
                ParseTree child = tree.getChild(i);
                if (child instanceof RuleContext) {
                    // Recursive call for non-terminal nodes
                    children.add(buildTree(child, parser));
                } else {
                    // Create a new map for the leaf node
                    Map<String, Object> leaf = new HashMap<>();
                    leaf.put("name", child.toString());
                    children.add(leaf);
                }
            }
            json.put("children", children);
        }
        return json;
    }

}
