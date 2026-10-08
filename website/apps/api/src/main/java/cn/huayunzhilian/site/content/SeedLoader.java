package cn.huayunzhilian.site.content;

import cn.huayunzhilian.site.common.HyzlProperties;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Date;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HexFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;
import org.springframework.transaction.support.TransactionTemplate;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.json.JsonMapper;

/**
 * 启动时导入 classpath:seed/*.json（由 website/tools/build_content.py 从素材库生成）。
 * mode=auto 时比较种子文件哈希，内容有变化则整体替换 content_item；always 每次启动都导入；never 不导入
 * （当前版本无后台编辑，内容以种子为准）。
 */
@Component
public class SeedLoader implements ApplicationRunner {
    private static final Logger log = LoggerFactory.getLogger(SeedLoader.class);

    private final JdbcClient jdbc;
    private final JsonMapper json;
    private final HyzlProperties props;
    private final TransactionTemplate tx;

    public SeedLoader(JdbcClient jdbc, JsonMapper json, HyzlProperties props, TransactionTemplate tx) {
        this.jdbc = jdbc;
        this.json = json;
        this.props = props;
        this.tx = tx;
    }

    @Override
    public void run(ApplicationArguments args) throws IOException {
        if ("never".equalsIgnoreCase(props.seed().mode())) {
            return;
        }
        Resource[] files = new PathMatchingResourcePatternResolver().getResources("classpath*:seed/*.json");
        Arrays.sort(files, Comparator.comparing(Resource::getFilename));
        MessageDigest digest = sha256();
        for (Resource r : files) {
            try (InputStream in = r.getInputStream()) {
                digest.update(in.readAllBytes());
            }
        }
        String hash = HexFormat.of().formatHex(digest.digest());
        String current = jdbc.sql("SELECT meta_value FROM content_meta WHERE meta_key = 'seed_hash'")
                .query(String.class).optional().orElse("");
        if (hash.equals(current) && !"always".equalsIgnoreCase(props.seed().mode())) {
            log.info("内容种子未变化，跳过导入");
            return;
        }
        tx.executeWithoutResult(status -> importAll(files, hash));
    }

    private void importAll(Resource[] files, String hash) {
        jdbc.sql("DELETE FROM content_item").update();
        int count = 0;
        for (Resource r : files) {
            if (r.getFilename() == null || r.getFilename().startsWith("_")) {
                continue;
            }
            try (InputStream in = r.getInputStream()) {
                JsonNode arr = json.readTree(new String(in.readAllBytes(), StandardCharsets.UTF_8));
                for (JsonNode n : arr) {
                    insert(n);
                    count++;
                }
            } catch (IOException e) {
                throw new IllegalStateException("读取种子失败：" + r.getFilename(), e);
            }
        }
        jdbc.sql("DELETE FROM content_meta WHERE meta_key = 'seed_hash'").update();
        jdbc.sql("INSERT INTO content_meta (meta_key, meta_value) VALUES ('seed_hash', :v)").param("v", hash).update();
        log.info("已导入内容种子 {} 条", count);
    }

    private void insert(JsonNode n) {
        jdbc.sql("""
                INSERT INTO content_item (content_type, slug, title, summary, category, sort_order, featured,
                    published_at, expires_at, authorized, archived, body_json)
                VALUES (:type, :slug, :title, :summary, :category, :sort, :featured, :pub, :exp, :auth, :arch, :body)
                """)
                .param("type", n.path("type").asString())
                .param("slug", n.path("slug").asString())
                .param("title", n.path("title").asString())
                .param("summary", text(n, "summary"))
                .param("category", text(n, "category"))
                .param("sort", n.path("sort").asInt(0))
                .param("featured", n.path("featured").asBoolean(false))
                .param("pub", date(n, "publishedAt"))
                .param("exp", date(n, "expiresAt"))
                .param("auth", n.path("authorized").asBoolean(true))
                .param("arch", n.path("archived").asBoolean(false))
                .param("body", json.writeValueAsString(n.path("data")))
                .update();
    }

    private static String text(JsonNode n, String field) {
        JsonNode v = n.get(field);
        return v == null || v.isNull() ? null : v.asString();
    }

    private static Date date(JsonNode n, String field) {
        String v = text(n, field);
        return v == null || v.isBlank() ? null : Date.valueOf(LocalDate.parse(v));
    }

    private static MessageDigest sha256() {
        try {
            return MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }
}
