package cn.huayunzhilian.site.rum;

import cn.huayunzhilian.site.common.ClientIp;
import cn.huayunzhilian.site.common.HyzlProperties;
import cn.huayunzhilian.site.common.RateLimiter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** 前端 Web Vitals 上报（K-05 §2.2），按采样率写入 rum_metrics。 */
@RestController
@RequestMapping("/api/v1/rum")
public class RumController {
    public record Metric(@Pattern(regexp = "LCP|INP|CLS|TTFB|FCP") String name,
                         @NotNull Double value,
                         @Size(max = 20) String rating,
                         @Size(max = 255) String path,
                         @Size(max = 16) String device) {}

    public record Batch(@NotNull @Size(max = 20) List<@Valid Metric> items) {}

    private final JdbcClient jdbc;
    private final RateLimiter limiter;
    private final HyzlProperties props;

    public RumController(JdbcClient jdbc, RateLimiter limiter, HyzlProperties props) {
        this.jdbc = jdbc;
        this.limiter = limiter;
        this.props = props;
    }

    @PostMapping
    public ResponseEntity<Void> collect(@Valid @RequestBody Batch batch, HttpServletRequest http) {
        limiter.check("rum", ClientIp.of(http), 60, Duration.ofMinutes(1));
        if (ThreadLocalRandom.current().nextDouble() < props.rum().sampleRate()) {
            for (Metric m : batch.items()) {
                jdbc.sql("INSERT INTO rum_metrics (metric, metric_value, rating, page_path, device) VALUES (:n, :v, :r, :p, :d)")
                        .param("n", m.name()).param("v", m.value()).param("r", m.rating())
                        .param("p", m.path()).param("d", m.device())
                        .update();
            }
        }
        return ResponseEntity.noContent().build();
    }
}
