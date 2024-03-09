package com.guardian.processing_service.controller;

import java.util.Map;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.guardian.processing_service.models.CodeSample;
import com.guardian.processing_service.models.RustCodeSample;
import com.guardian.processing_service.service.RustProcessingService;

@RestController
@RequestMapping("/processing-service")
public class ProcessingServiceController {

    private final RestTemplate restTemplate;
    private final RustProcessingService processingService;

    public ProcessingServiceController(RestTemplate restTemplate, RustProcessingService processingService) {
        this.restTemplate = restTemplate;
        this.processingService = processingService;

    }

    @GetMapping("/process-code/{language}")
    public JSONObject processCode(PathVariable language) {

        if (!language.equals("rust")) {
            throw new IllegalArgumentException("Language not supported");
        }

        CodeSample codeSample =  restTemplate.getForObject("http://localhost:5000/fetch-code-sample", RustCodeSample.class);

        return processingService.processCode(codeSample);

    }
}
