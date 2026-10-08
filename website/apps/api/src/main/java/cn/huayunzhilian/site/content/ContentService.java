package cn.huayunzhilian.site.content;

import java.time.Clock;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;
import org.springframework.stereotype.Service;

/**
 * 内容读取与对外过滤规则（K-05 §2.1、§5“内容合规”）：
 * - 案例 / 客户：未授权或授权过期不返回；
 * - 证书：过期不返回，60 天内到期标记 expiring；
 * - 新闻：按发布日期倒序，可按近 N 天过滤。
 */
@Service
public class ContentService {
    public static final Set<String> TYPES = Set.of("page", "product", "solution", "case", "news", "job", "standard",
            "patent", "copyright", "project", "award", "certificate", "partner", "lab");
    static final int EXPIRING_DAYS = 60;

    private final ContentRepository repository;
    private final Clock clock;

    public ContentService(ContentRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    public List<ContentItem> list(ContentQuery q) {
        LocalDate today = LocalDate.now(clock);
        Stream<ContentItem> s = repository.findPublished(q.type()).stream()
                .filter(i -> visible(i, today))
                .map(i -> decorate(i, today));
        if (q.category() != null) {
            Set<String> cats = Set.of(q.category().split(","));
            s = s.filter(i -> i.category() != null && cats.contains(i.category()));
        }
        if (q.featured() != null) {
            s = s.filter(i -> i.featured() == q.featured());
        }
        if (q.archived() != null) {
            s = s.filter(i -> i.archived() == q.archived());
        }
        if (q.withinDays() != null) {
            LocalDate from = today.minusDays(q.withinDays());
            s = s.filter(i -> i.publishedAt() != null && !i.publishedAt().isBefore(from));
        }
        if ("news".equals(q.type())) {
            s = s.sorted(Comparator.comparing(ContentItem::publishedAt, Comparator.nullsLast(Comparator.reverseOrder())));
        }
        if (q.limit() != null) {
            s = s.limit(q.limit());
        }
        return s.toList();
    }

    public ContentItem get(String type, String slug) {
        LocalDate today = LocalDate.now(clock);
        return repository.findOne(type, slug)
                .filter(i -> visible(i, today))
                .map(i -> decorate(i, today))
                .orElseThrow(() -> cn.huayunzhilian.site.common.ApiException.notFound(
                        "CONTENT_NOT_FOUND", "内容不存在或已下线"));
    }

    static boolean visible(ContentItem i, LocalDate today) {
        if (("case".equals(i.type()) || "customer".equals(i.type())) && !i.authorized()) {
            return false;
        }
        if ("certificate".equals(i.type()) && i.expiresAt() != null && i.expiresAt().isBefore(today)) {
            return false;
        }
        return true;
    }

    static ContentItem decorate(ContentItem i, LocalDate today) {
        if (!"certificate".equals(i.type())) {
            return i;
        }
        if (i.expiresAt() == null) {
            return i.withStatus("valid");
        }
        long days = ChronoUnit.DAYS.between(today, i.expiresAt());
        return i.withStatus(days <= EXPIRING_DAYS ? "expiring" : "valid");
    }
}
