package com.guardian.processing_service.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class WebConfig {

    RestTemplate restTemplate() {
        return new RestTemplate();
    }
    

    
}
