package cn.huayunzhilian.site.lead;

import static org.assertj.core.api.Assertions.assertThat;

import cn.huayunzhilian.site.common.HyzlProperties;
import org.junit.jupiter.api.Test;

class CryptoServiceTest {
    private final CryptoService crypto = new CryptoService(new HyzlProperties("./data", null, null, null,
            new HyzlProperties.Crypto("aHl6bC1sb2NhbC1zbTQhIQ==", "test-hmac"), "2026-10", null));

    @Test
    void sm4GcmRoundTripUsesRandomIv() {
        String a = crypto.encrypt("13800138000");
        String b = crypto.encrypt("13800138000");
        assertThat(a).isNotEqualTo(b).doesNotContain("13800138000");
        assertThat(crypto.decrypt(a)).isEqualTo("13800138000");
    }

    @Test
    void hashIsDeterministic() {
        assertThat(crypto.hash("a@b.cn")).isEqualTo(crypto.hash("a@b.cn")).isNotEqualTo(crypto.hash("c@d.cn"));
    }
}
