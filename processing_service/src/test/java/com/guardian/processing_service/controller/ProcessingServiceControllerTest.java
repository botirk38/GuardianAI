package com.guardian.processing_service.controller;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.guardian.processing_service.models.CodeSample;
import com.guardian.processing_service.models.RustCodeSample;
import com.guardian.processing_service.service.ProcessingService;

@WebMvcTest(ProcessingServiceController.class)
public class ProcessingServiceControllerTest {

    private MockMvc mockMvc;

    @MockBean
    private RestTemplate restTemplate;

    @MockBean
    private ProcessingService processingService;

    @InjectMocks
    private ProcessingServiceController controller;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    

    @Test
    public void testProcessCodeWithUnsupportedLanguage() throws Exception {
        mockMvc.perform(get("/processing-service/process-code/java")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest());
    }

    @Test
    public void testProcessCodeWithInvalidCodeSample() throws Exception {
        when(restTemplate.getForObject(anyString(), eq(RustCodeSample.class))).thenReturn(null);

        mockMvc.perform(get("/processing-service/process-code/rust")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest());
    }

   

    @Test
    public void testAnalyzeCodeWithInvalidCodeSample() throws Exception {
        CodeSample codeSample = new RustCodeSample("", 0, "", "", "", "");

        mockMvc.perform(post("/processing-service/analyze-code")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(codeSample)))
                .andExpect(status().isBadRequest());
    }

    @Test
    public void testProcessCodeWithEmptyCodeSample() throws Exception {
        CodeSample codeSample = new RustCodeSample("", 0, "", "rust", "", "");

        mockMvc.perform(get("/processing-service/process-code/rust")
                .contentType(MediaType.APPLICATION_JSON).content(new ObjectMapper().writeValueAsString(codeSample)))

                .andExpect(status().isBadRequest());
    }

    @Test
    public void testProcessCodeWithNullLanguage() throws Exception {
        mockMvc.perform(get("/processing-service/process-code/null")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest());
    }
}
