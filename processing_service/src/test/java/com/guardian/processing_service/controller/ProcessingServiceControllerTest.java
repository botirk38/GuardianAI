package com.guardian.processing_service.controller;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.client.RestTemplate;

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
    public void testProcessCodeWithValidLanguage() throws Exception {
        CodeSample codeSample = new RustCodeSample("fn main() { println!(\"Hello World\"); }", 1, "repo", "rust", "path", "license");
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("result", "Processed");

        when(restTemplate.getForObject(anyString(), eq(CodeSample.class))).thenReturn(codeSample);
        when(processingService.processCode(codeSample)).thenReturn(jsonObject);

        mockMvc.perform(get("/processing-service/process-code/rust")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk());
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
}
