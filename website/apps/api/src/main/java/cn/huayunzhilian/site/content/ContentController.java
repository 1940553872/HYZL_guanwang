package cn.huayunzhilian.site.content;

import cn.huayunzhilian.site.common.ApiException;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import java.util.List;
import java.util.Map;
import org.springframework.http.CacheControl;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** 公开内容接口（K-05 §2.1）。 */
@RestController
@Validated
@RequestMapping("/api/v1/content")
public class ContentController {
    private static final CacheControl CACHE = CacheControl.maxAge(java.time.Duration.ofMinutes(5)).cachePublic();

    private final ContentService service;

    public ContentController(ContentService service) {
        this.service = service;
    }

    @GetMapping("/{type}")
    public ResponseEntity<Map<String, Object>> list(
            @PathVariable String type,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) Boolean featured,
            @RequestParam(required = false) Boolean archived,
            @RequestParam(required = false) @Min(1) @Max(3650) Integer within,
            @RequestParam(required = false) @Min(1) @Max(500) Integer limit) {
        checkType(type);
        List<ContentItem> items = service.list(new ContentQuery(type, category, featured, archived, within, limit));
        return ResponseEntity.ok().cacheControl(CACHE).body(Map.of("total", items.size(), "items", items));
    }

    @GetMapping("/{type}/**")
    public ResponseEntity<ContentItem> get(@PathVariable String type, jakarta.servlet.http.HttpServletRequest request) {
        checkType(type);
        String prefix = "/api/v1/content/" + type + "/";
        String slug = request.getRequestURI().substring(request.getRequestURI().indexOf(prefix) + prefix.length());
        slug = java.net.URLDecoder.decode(slug, java.nio.charset.StandardCharsets.UTF_8);
        if (!slug.matches("[a-z0-9][a-z0-9\\-/]{0,158}")) {
            throw ApiException.notFound("CONTENT_NOT_FOUND", "内容不存在");
        }
        return ResponseEntity.ok().cacheControl(CACHE).body(service.get(type, slug));
    }

    private static void checkType(String type) {
        if (!ContentService.TYPES.contains(type)) {
            throw ApiException.notFound("TYPE_NOT_FOUND", "内容类型不存在");
        }
    }
}
