package com.guardian.processing_service.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import com.guardian.processing_service.antlr.rust.RustLexer;
import com.guardian.processing_service.antlr.rust.RustParser;

@Configuration
public class WebConfig {

    @Bean
    RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    RustParser rustParser() {
        return new RustParser(null);
    }

    @Bean
    RustLexer rustLexer() {
        return new RustLexer(null);
    }


    
}
