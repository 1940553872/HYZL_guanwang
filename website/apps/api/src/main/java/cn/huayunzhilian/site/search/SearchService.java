package cn.huayunzhilian.site.search;

import cn.huayunzhilian.site.content.ContentItem;
import cn.huayunzhilian.site.content.ContentRepository;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import org.springframework.stereotype.Service;
import tools.jackson.databind.JsonNode;

/**
 * 站内搜索：编码（i 系列、标准号、软著登记号）精确匹配优先，其次标题、摘要、正文包含匹配。
 * 内容量约 250 条，在内存中完成；数据量增长后切换到 PostgreSQL 中文全文检索（K-05 §1.1）。
 */
@Service
public class SearchService {
    static final Set<String> TYPES = Set.of("product", "solution", "case", "news", "standard", "patent", "copyright",
            "project", "award", "lab");

    private final ContentRepository repository;

    public SearchService(ContentRepository repository) {
        this.repository = repository;
    }

    /** 非正文字段（结构标记、图片、关联键），不参与正文匹配与摘要。 */
    private static final Set<String> NON_TEXT_KEYS = Set.of("t", "kind", "group", "src", "thumb", "w", "h", "parent", "icon",
            "related", "products", "status", "codeSource", "level", "state", "image", "images", "logo", "id");

    /** 同分时的类型权重：产品 > 方案 > 案例 > 其他（用户多为找产品与方案）。 */
    private static final Map<String, Integer> TYPE_WEIGHT = Map.of("product", 5, "solution", 4, "case", 3, "lab", 2,
            "news", 1);

    public record Hit(String type, String slug, String title, String code, String snippet, String url, int score) {}

    public Map<String, Object> search(String q, String type, int page, int size) {
        String needle = q.trim().toLowerCase(Locale.ROOT);
        String compact = needle.replace(" ", "");
        List<Hit> hits = new ArrayList<>();
        for (ContentItem i : repository.findAllPublished()) {
            if (!TYPES.contains(i.type()) || (type != null && !type.equals(i.type())) || ("case".equals(i.type()) && !i.authorized())) {
                continue;
            }
            String code = codeOf(i).toLowerCase(Locale.ROOT);
            String title = i.title().toLowerCase(Locale.ROOT);
            String summary = i.summary() == null ? "" : i.summary();
            String body = plain(i.data());
            int score = 0;
            if (!code.isEmpty() && (code.equals(needle) || code.replace(" ", "").equals(compact))) {
                score = 100;
            } else if (!code.isEmpty() && code.replace(" ", "").contains(compact)) {
                score = 80;
            } else if (title.contains(needle)) {
                score = 60;
            } else if (summary.toLowerCase(Locale.ROOT).contains(needle)) {
                score = 40;
            } else if (body.toLowerCase(Locale.ROOT).contains(needle)) {
                score = 20;
            }
            if (score > 0) {
                String source = summary.toLowerCase(Locale.ROOT).contains(needle) || body.isEmpty() ? summary : body;
                hits.add(new Hit(i.type(), i.slug(), i.title(), code.isEmpty() ? null : codeOf(i),
                        snippet(source.isEmpty() ? summary : source, needle), urlOf(i),
                        score + TYPE_WEIGHT.getOrDefault(i.type(), 0)));
            }
        }
        hits.sort(Comparator.comparingInt(Hit::score).reversed().thenComparing(Hit::title));
        int from = Math.min((page - 1) * size, hits.size());
        int to = Math.min(from + size, hits.size());
        return Map.of("total", hits.size(), "page", page, "hits", hits.subList(from, to));
    }

    static String codeOf(ContentItem i) {
        JsonNode d = i.data();
        for (String f : List.of("code", "regNo", "number")) {
            JsonNode v = d.get(f);
            if (v != null && v.isString()) {
                return v.asString();
            }
        }
        return "";
    }

    static String plain(JsonNode node) {
        StringBuilder sb = new StringBuilder();
        collect(node, sb);
        return sb.toString();
    }

    private static void collect(JsonNode n, StringBuilder sb) {
        if (n == null) {
            return;
        }
        if (n.isString()) {
            String s = n.asString();
            if (!s.startsWith("/media/")) {
                sb.append(s).append(' ');
            }
        } else if (n.isObject()) {
            for (Map.Entry<String, JsonNode> e : n.properties()) {
                if (!NON_TEXT_KEYS.contains(e.getKey())) {
                    collect(e.getValue(), sb);
                }
            }
        } else if (n.isArray()) {
            for (JsonNode c : n) {
                collect(c, sb);
            }
        }
    }

    static String snippet(String text, String needle) {
        if (text == null || text.isEmpty()) {
            return "";
        }
        int idx = text.toLowerCase(Locale.ROOT).indexOf(needle);
        int start = Math.max(0, idx < 0 ? 0 : idx - 30);
        int end = Math.min(text.length(), start + 120);
        return (start > 0 ? "…" : "") + text.substring(start, end).trim() + (end < text.length() ? "…" : "");
    }

    /** 与前端路由保持一致（design_document/K-02 §2.1）。 */
    static String urlOf(ContentItem i) {
        return switch (i.type()) {
            case "product" -> productUrl(i);
            case "solution" -> "/solutions/" + i.slug();
            case "case" -> "/cases/" + i.slug();
            case "news" -> "/news/" + i.slug();
            case "lab" -> "/research/labs";
            case "standard", "patent", "copyright", "project" -> "/research?tab=" + i.type() + "s";
            case "award" -> "/about/honors";
            default -> "/";
        };
    }

    private static String productUrl(ContentItem i) {
        String c = i.category() == null ? "" : i.category();
        return switch (c) {
            case "platform" -> "/products";
            case "flagship" -> "/products/spatigo";
            case "sub_product" -> "/products/spatigo/" + i.slug().replace("spatigo-", "");
            case "model" -> "/products/imllm";
            case "agent" -> "/products/agents/" + i.slug();
            case "engine_group" -> "/products/engines";
            case "engine" -> "/products/engines#" + i.slug();
            case "software" -> "/products/software/" + i.slug();
            case "software_group" -> "/products/software";
            case "security" -> "/products/security-integration";
            default -> "/products";
        };
    }
}
