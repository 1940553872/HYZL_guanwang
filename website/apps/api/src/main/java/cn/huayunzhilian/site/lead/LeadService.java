package cn.huayunzhilian.site.lead;

import cn.huayunzhilian.site.common.ApiException;
import cn.huayunzhilian.site.common.HyzlProperties;
import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;

@Service
public class LeadService {
    private static final Logger log = LoggerFactory.getLogger(LeadService.class);
    private static final Pattern MOBILE = Pattern.compile("^1[3-9]\\d{9}$");
    private static final Pattern LANDLINE = Pattern.compile("^0\\d{2,3}\\d{7,8}$");

    private final JdbcClient jdbc;
    private final CryptoService crypto;
    private final HyzlProperties props;

    public LeadService(JdbcClient jdbc, CryptoService crypto, HyzlProperties props) {
        this.jdbc = jdbc;
        this.crypto = crypto;
        this.props = props;
    }

    public record Result(String id, boolean duplicate) {}

    /** 规范化手机号：全角转半角，去空格与连字符，去 +86 前缀。 */
    static String normalizePhone(String raw) {
        if (raw == null || raw.isBlank()) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        for (char ch : raw.trim().toCharArray()) {
            if (ch >= '０' && ch <= '９') {
                ch = (char) (ch - '０' + '0');
            } else if (ch == '＋') {
                ch = '+';
            }
            if (Character.isDigit(ch) || ch == '+') {
                sb.append(ch);
            }
        }
        String p = sb.toString();
        if (p.startsWith("+86")) {
            p = p.substring(3);
        } else if (p.startsWith("0086")) {
            p = p.substring(4);
        }
        return p;
    }

    public Result create(LeadRequest req, String ip) {
        String phone = normalizePhone(req.phone());
        String email = req.email() == null || req.email().isBlank() ? null : req.email().trim().toLowerCase();
        if (phone == null && email == null) {
            throw ApiException.badRequest("phone", "required", "手机号或邮箱至少填写一项");
        }
        if (phone != null && !MOBILE.matcher(phone).matches() && !LANDLINE.matcher(phone).matches()) {
            throw ApiException.badRequest("phone", "pattern", "手机号格式不正确");
        }
        String phoneHash = crypto.hash(phone);
        String emailHash = crypto.hash(email);
        LocalDateTime since = LocalDateTime.now().minusHours(24);
        // 参数为 NULL 时“= NULL”恒不成立，因此未填写的字段不参与去重（H2 / PostgreSQL 通用写法）
        Optional<String> existing = jdbc.sql("""
                SELECT id FROM leads WHERE created_at >= :since
                  AND (phone_hash = :ph OR email_hash = :eh)
                ORDER BY created_at DESC
                """)
                .param("since", since).param("ph", phoneHash).param("eh", emailHash)
                .query(String.class).list().stream().findFirst();
        if (existing.isPresent()) {
            return new Result(existing.get(), true);
        }
        String id = UUID.randomUUID().toString();
        jdbc.sql("""
                INSERT INTO leads (id, lead_type, name, company, job_title, phone_enc, phone_hash, email_enc, email_hash,
                    product_interest, scenario, locale, source_page, utm_source, utm_medium, utm_campaign, ip_hash,
                    consent_version, consent_at)
                VALUES (:id, :type, :name, :company, :title, :pe, :ph, :ee, :eh, :pi, :sc, :locale, :src, :us, :um, :uc,
                    :ip, :cv, :ca)
                """)
                .param("id", id)
                .param("type", req.type() == null ? "demo" : req.type())
                .param("name", req.name().trim())
                .param("company", req.company().trim())
                .param("title", trim(req.title()))
                .param("pe", crypto.encrypt(phone)).param("ph", phoneHash)
                .param("ee", crypto.encrypt(email)).param("eh", emailHash)
                .param("pi", trim(req.productInterest()))
                .param("sc", trim(req.scenario()))
                .param("locale", req.locale() == null ? "zh" : req.locale())
                .param("src", trim(req.sourcePage()))
                .param("us", trim(req.utmSource())).param("um", trim(req.utmMedium())).param("uc", trim(req.utmCampaign()))
                .param("ip", crypto.hash(ip))
                .param("cv", req.consentVersion() == null ? props.consentVersion() : req.consentVersion())
                .param("ca", LocalDateTime.now())
                .update();
        // 通知：当前版本写入日志（不含个人信息）；生产按 K-05 §1.1 接入企业微信 / 邮件
        log.info("new lead id={} type={} product={}", id, req.type(), req.productInterest());
        return new Result(id, false);
    }

    private static String trim(String s) {
        return s == null || s.isBlank() ? null : s.trim();
    }
}
