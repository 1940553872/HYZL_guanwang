package cn.huayunzhilian.site.search;

import cn.huayunzhilian.site.common.ApiException;
import cn.huayunzhilian.site.common.ClientIp;
import cn.huayunzhilian.site.common.RateLimiter;
import jakarta.servlet.http.HttpServletRequest;
import java.time.Duration;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/search")
public class SearchController {
    private final SearchService service;
    private final RateLimiter limiter;

    public SearchController(SearchService service, RateLimiter limiter) {
        this.service = service;
        this.limiter = limiter;
    }

    @GetMapping
    public Map<String, Object> search(@RequestParam("q") String q,
                                      @RequestParam(required = false) String type,
                                      @RequestParam(defaultValue = "1") int page,
                                      @RequestParam(defaultValue = "10") int size,
                                      HttpServletRequest http) {
        limiter.check("search", ClientIp.of(http), 30, Duration.ofMinutes(1));
        String query = q == null ? "" : q.trim();
        if (query.isEmpty() || query.length() > 50) {
            throw ApiException.badRequest("q", "length", "搜索词长度应为 1—50 个字符");
        }
        if (type != null && !SearchService.TYPES.contains(type)) {
            throw ApiException.badRequest("type", "enum", "搜索类型不正确");
        }
        return service.search(query, type, Math.max(page, 1), Math.min(Math.max(size, 1), 50));
    }
}
