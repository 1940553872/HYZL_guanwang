package cn.huayunzhilian.site.lead;

import cn.huayunzhilian.site.common.ClientIp;
import cn.huayunzhilian.site.common.RateLimiter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import java.time.Duration;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/leads")
public class LeadController {
    private final LeadService service;
    private final RateLimiter limiter;

    public LeadController(LeadService service, RateLimiter limiter) {
        this.service = service;
        this.limiter = limiter;
    }

    @PostMapping
    public ResponseEntity<Map<String, String>> create(@Valid @RequestBody LeadRequest req, HttpServletRequest http) {
        String ip = ClientIp.of(http);
        // 每 IP 5 次 / 10 分钟（K-05 §2.2）；验证码服务接入前，超限直接返回 429
        limiter.check("lead", ip, 5, Duration.ofMinutes(10));
        LeadService.Result r = service.create(req, ip);
        return ResponseEntity.status(r.duplicate() ? HttpStatus.OK : HttpStatus.CREATED)
                .body(Map.of("id", r.id(), "status", "received"));
    }
}
