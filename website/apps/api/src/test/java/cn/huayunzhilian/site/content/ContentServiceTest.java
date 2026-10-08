package cn.huayunzhilian.site.content;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import tools.jackson.databind.json.JsonMapper;

class ContentServiceTest {
    private static final LocalDate TODAY = LocalDate.of(2026, 10, 8);

    private static ContentItem item(String type, boolean authorized, LocalDate expiresAt) {
        return new ContentItem(type, "x", "标题", "", null, 1, false, null, expiresAt, authorized, false, null,
                JsonMapper.builder().build().createObjectNode());
    }

    @Test
    void hidesUnauthorizedCases() {
        assertThat(ContentService.visible(item("case", false, null), TODAY)).isFalse();
        assertThat(ContentService.visible(item("case", true, null), TODAY)).isTrue();
        assertThat(ContentService.visible(item("news", false, null), TODAY)).isTrue();
    }

    @Test
    void hidesExpiredCertificates() {
        assertThat(ContentService.visible(item("certificate", true, TODAY.minusDays(1)), TODAY)).isFalse();
        assertThat(ContentService.visible(item("certificate", true, TODAY), TODAY)).isTrue();
    }

    @Test
    void marksCertificatesExpiringWithin60Days() {
        assertThat(ContentService.decorate(item("certificate", true, TODAY.plusDays(60)), TODAY).status()).isEqualTo("expiring");
        assertThat(ContentService.decorate(item("certificate", true, TODAY.plusDays(61)), TODAY).status()).isEqualTo("valid");
        assertThat(ContentService.decorate(item("certificate", true, null), TODAY).status()).isEqualTo("valid");
        assertThat(ContentService.decorate(item("news", true, null), TODAY).status()).isNull();
    }
}
