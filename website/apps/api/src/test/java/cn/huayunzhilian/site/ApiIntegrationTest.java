package cn.huayunzhilian.site;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import cn.huayunzhilian.site.common.RateLimiter;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

/** 接口集成测试：真实 Flyway 迁移 + 种子内容 + H2 内存库（K-06 §3 接口用例）。 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class ApiIntegrationTest {
    @Autowired
    MockMvc mvc;

    @Autowired
    RateLimiter limiter;

    @BeforeEach
    void resetLimiter() {
        limiter.reset();
    }

    private static String lead(String phone, String email, boolean consent) {
        return """
                {"type":"demo","name":"测试","company":"测试公司","phone":%s,"email":%s,"consent":%s,"website":""}
                """.formatted(phone == null ? "null" : "\"" + phone + "\"", email == null ? "null" : "\"" + email + "\"", consent);
    }

    @Test
    void listsAndFiltersContent() throws Exception {
        mvc.perform(get("/api/v1/content/product").param("category", "sub_product"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.total", is(4)));
        mvc.perform(get("/api/v1/content/news/2020/company-01"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.category", is("company")));
        mvc.perform(get("/api/v1/content/news/2099/none")).andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code", is("CONTENT_NOT_FOUND")));
        mvc.perform(get("/api/v1/content/unknown-type")).andExpect(status().isNotFound());
    }

    @Test
    void certificatesCarryStatus() throws Exception {
        mvc.perform(get("/api/v1/content/certificate"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items[0].status").exists());
    }

    @Test
    void searchRanksExactCodeFirst() throws Exception {
        mvc.perform(get("/api/v1/search").param("q", "iMES"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.hits[0].slug", is("imes")))
                .andExpect(jsonPath("$.hits[0].url", is("/products/software/imes")));
        mvc.perform(get("/api/v1/search").param("q", "")).andExpect(status().isBadRequest());
    }

    @Test
    void leadValidationAndDedupe() throws Exception {
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead(null, null, true)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message", containsString("至少填写一项")));
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("13800138000", null, false)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code", is("VALIDATION_FAILED")));
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("12345", null, true)))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("13900139000", null, true)))
                .andExpect(status().isCreated());
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("+86 139 0013 9000", null, true)))
                .andExpect(status().isOk());
    }

    @Test
    void leadRateLimitedPerIp() throws Exception {
        for (int i = 0; i < 5; i++) {
            mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead(null, "rl" + i + "@example.com", true)));
        }
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead(null, "rl9@example.com", true)))
                .andExpect(status().isTooManyRequests())
                .andExpect(jsonPath("$.code", is("RATE_LIMITED")));
    }

    @Test
    void adminRequiresTokenAndMasksPii() throws Exception {
        mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("13700137000", null, true)))
                .andExpect(status().isCreated());
        mvc.perform(get("/admin/v1/leads")).andExpect(status().isUnauthorized());
        mvc.perform(get("/admin/v1/leads").header("Authorization", "Bearer wrong")).andExpect(status().isUnauthorized());
        mvc.perform(get("/admin/v1/leads").header("Authorization", "Bearer test-admin-token"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.total", greaterThan(0)))
                .andExpect(jsonPath("$.items[*].phone", hasItem(containsString("****"))));
    }

    @Test
    void adminRejectsInvalidStateTransition() throws Exception {
        String body = mvc.perform(post("/api/v1/leads").contentType(MediaType.APPLICATION_JSON).content(lead("13600136000", null, true)))
                .andReturn().getResponse().getContentAsString();
        String id = body.replaceAll(".*\"id\":\"([^\"]+)\".*", "$1");
        mvc.perform(patch("/admin/v1/leads/" + id).header("Authorization", "Bearer test-admin-token")
                        .contentType(MediaType.APPLICATION_JSON).content("{\"status\":\"qualified\"}"))
                .andExpect(status().isConflict());
        mvc.perform(patch("/admin/v1/leads/" + id).header("Authorization", "Bearer test-admin-token")
                        .contentType(MediaType.APPLICATION_JSON).content("{\"status\":\"assigned\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void healthIsUp() throws Exception {
        mvc.perform(get("/actuator/health")).andExpect(status().isOk()).andExpect(jsonPath("$.status", is("UP")));
    }
}
