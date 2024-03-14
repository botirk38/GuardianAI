package com.guardian.processing_service.controller;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.guardian.processing_service.models.CodeSample;
import com.guardian.processing_service.models.RustCodeSample;
import com.guardian.processing_service.service.ProcessingService;

@RestController
@RequestMapping("/processing-service")
public class ProcessingServiceController {

    private final RestTemplate restTemplate;
    private final ProcessingService processingService;
    private final Logger logger = LoggerFactory.getLogger(ProcessingServiceController.class);

    public ProcessingServiceController(RestTemplate restTemplate, ProcessingService processingService) {
        this.restTemplate = restTemplate;
        this.processingService = processingService;

    }

    @GetMapping("/process-code/{language}")
    public ResponseEntity<Map<String, ?>> processCode(@PathVariable("language") String language) {

        if (!language.equals("rust")) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid code sample or language not supported"));
        }

        CodeSample codeSample = restTemplate.getForObject("http://localhost:5000/fetch-code-sample",
                RustCodeSample.class);

        logger.debug("Code Sample: " + codeSample.toString());

        if (codeSample == null || !codeSample.getLanguage().equals("rust") || codeSample.getCode().isEmpty()
                || codeSample.getSize() < 1 || codeSample.getRepo().isEmpty() || codeSample.getPath().isEmpty()
                || codeSample.getLicense().isEmpty() || codeSample.getLanguage().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid code sample or language not supported"));
        }

        Map<String, Object> tree = processingService.processCode(codeSample);
        Map<String, Object> result = new HashMap<>();

        result.put("Code:", codeSample.getCode());
        result.put("Tree:", tree);
        logger.debug("Result: " + result.toString());

        return ResponseEntity.ok().body(result);

    }

    @PostMapping("/analyze-code")
    public ResponseEntity<Map<String, ?>> analyzeCode(@RequestBody RustCodeSample codeSample) {
        if (codeSample == null || !codeSample.getLanguage().equals("rust") || codeSample.getCode().isEmpty()
                || codeSample.getSize() < 1 || codeSample.getRepo().isEmpty() || codeSample.getPath().isEmpty()
                || codeSample.getLicense().isEmpty() || codeSample.getLanguage().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid code sample or language not supported"));
        }

        Map<String, Object> result = processingService.processCode(codeSample);

        return ResponseEntity.ok().body(Map.of("Tree:", result));
    }
}
