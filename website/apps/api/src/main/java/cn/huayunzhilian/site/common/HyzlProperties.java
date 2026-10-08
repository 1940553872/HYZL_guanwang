package cn.huayunzhilian.site.common;

import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;

/** 业务配置（application.yml 中 hyzl.*）。 */
@ConfigurationProperties(prefix = "hyzl")
public record HyzlProperties(
        String dataDir,
        Seed seed,
        Cors cors,
        Admin admin,
        Crypto crypto,
        String consentVersion,
        Rum rum) {

    public record Seed(String mode) {}

    public record Cors(List<String> allowedOrigins) {}

    public record Admin(String token) {}

    public record Crypto(String sm4Key, String hmacKey) {}

    public record Rum(double sampleRate) {}
}
