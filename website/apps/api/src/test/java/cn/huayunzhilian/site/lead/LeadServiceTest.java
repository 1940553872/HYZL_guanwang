package cn.huayunzhilian.site.lead;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class LeadServiceTest {
    @Test
    void normalizesPhoneNumbers() {
        assertThat(LeadService.normalizePhone("138 0013 8000")).isEqualTo("13800138000");
        assertThat(LeadService.normalizePhone("+86-138-0013-8000")).isEqualTo("13800138000");
        assertThat(LeadService.normalizePhone("0086 13800138000")).isEqualTo("13800138000");
        assertThat(LeadService.normalizePhone("＋８６１３８００１３８０００")).isEqualTo("13800138000");
        assertThat(LeadService.normalizePhone("029-88810623")).isEqualTo("02988810623");
        assertThat(LeadService.normalizePhone("  ")).isNull();
        assertThat(LeadService.normalizePhone(null)).isNull();
    }
}
