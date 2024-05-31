package com.smartGuardian.api_gateway_vuln_detection.config;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        http
                .authorizeExchange(exchanges -> exchanges
                        .pathMatchers("/feature-extractor/**").hasAuthority("SCOPE_write:detect_vulnerabilities_free")
                        .anyExchange().authenticated()
                    

                )
                .oauth2ResourceServer(oauth2 -> oauth2.jwt(withDefaults()));
                
                
        return http.build();
    }

    

}
