package cn.huayunzhilian.site.admin;

import cn.huayunzhilian.site.common.ApiException;
import cn.huayunzhilian.site.lead.CryptoService;
import jakarta.servlet.http.HttpServletRequest;
import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** 线索管理接口（K-05 §2.3 的最小实现）：列表默认脱敏，查看明文写审计日志，状态按状态机流转。 */
@RestController
@RequestMapping("/admin/v1/leads")
public class AdminLeadController {
    private static final Map<String, Set<String>> TRANSITIONS = Map.of(
            "new", Set.of("assigned", "invalid"),
            "assigned", Set.of("contacted", "invalid"),
            "contacted", Set.of("qualified", "invalid"),
            "invalid", Set.of("assigned"),
            "qualified", Set.of());

    private final JdbcClient jdbc;
    private final CryptoService crypto;

    public AdminLeadController(JdbcClient jdbc, CryptoService crypto) {
        this.jdbc = jdbc;
        this.crypto = crypto;
    }

    @GetMapping
    public Map<String, Object> list(@RequestParam(required = false) String status,
                                    @RequestParam(defaultValue = "false") boolean reveal,
                                    @RequestParam(defaultValue = "1") int page,
                                    @RequestParam(defaultValue = "20") int size,
                                    HttpServletRequest http) {
        int limit = Math.min(Math.max(size, 1), 100);
        int offset = (Math.max(page, 1) - 1) * limit;
        List<Map<String, Object>> rows = jdbc.sql("""
                SELECT id, lead_type, name, company, job_title, phone_enc, email_enc, product_interest, scenario,
                       source_page, status, created_at FROM leads
                WHERE (CAST(:status AS VARCHAR) IS NULL OR status = :status) ORDER BY created_at DESC LIMIT :limit OFFSET :offset
                """)
                .param("status", status).param("limit", limit).param("offset", offset)
                .query((rs, n) -> {
                    Map<String, Object> m = new LinkedHashMap<>();
                    m.put("id", rs.getString("id"));
                    m.put("type", rs.getString("lead_type"));
                    m.put("name", rs.getString("name"));
                    m.put("company", rs.getString("company"));
                    m.put("title", rs.getString("job_title"));
                    String phone = crypto.decrypt(rs.getString("phone_enc"));
                    String email = crypto.decrypt(rs.getString("email_enc"));
                    m.put("phone", reveal ? phone : maskPhone(phone));
                    m.put("email", reveal ? email : maskEmail(email));
                    m.put("productInterest", rs.getString("product_interest"));
                    m.put("scenario", rs.getString("scenario"));
                    m.put("sourcePage", rs.getString("source_page"));
                    m.put("status", rs.getString("status"));
                    m.put("createdAt", rs.getTimestamp("created_at").toLocalDateTime().toString());
                    return m;
                })
                .list();
        if (reveal) {
            for (Map<String, Object> r : rows) {
                audit(http, "view_pii", (String) r.get("id"), null);
            }
        }
        long total = jdbc.sql("SELECT COUNT(*) FROM leads WHERE (CAST(:status AS VARCHAR) IS NULL OR status = :status)")
                .param("status", status).query(Long.class).single();
        return Map.of("total", total, "items", rows);
    }

    public record StatusChange(String status, String notes) {}

    @PatchMapping("/{id}")
    public Map<String, String> update(@PathVariable String id, @RequestBody StatusChange change, HttpServletRequest http) {
        String current = jdbc.sql("SELECT status FROM leads WHERE id = :id").param("id", id).query(String.class)
                .optional().orElseThrow(() -> ApiException.notFound("LEAD_NOT_FOUND", "线索不存在"));
        if (change.status() == null || !TRANSITIONS.getOrDefault(current, Set.of()).contains(change.status())) {
            throw new ApiException(HttpStatus.CONFLICT, "INVALID_TRANSITION",
                    "不允许从 " + current + " 变更为 " + change.status());
        }
        jdbc.sql("UPDATE leads SET status = :s, notes = COALESCE(:n, notes), updated_at = :t WHERE id = :id")
                .param("s", change.status()).param("n", change.notes()).param("t", LocalDateTime.now()).param("id", id)
                .update();
        audit(http, "update_status", id, current + "->" + change.status());
        return Map.of("id", id, "status", change.status());
    }

    private void audit(HttpServletRequest http, String action, String id, String detail) {
        jdbc.sql("INSERT INTO audit_logs (actor, action, target_type, target_id, detail) VALUES (:a, :ac, 'lead', :id, :d)")
                .param("a", String.valueOf(http.getAttribute("actor"))).param("ac", action).param("id", id)
                .param("d", detail).update();
    }

    static String maskPhone(String p) {
        if (p == null) {
            return null;
        }
        return p.length() >= 7 ? p.substring(0, 3) + "****" + p.substring(p.length() - 4) : "****";
    }

    static String maskEmail(String e) {
        if (e == null) {
            return null;
        }
        int at = e.indexOf('@');
        return at <= 1 ? "***" + e.substring(Math.max(at, 0)) : e.charAt(0) + "***" + e.substring(at);
    }
}
