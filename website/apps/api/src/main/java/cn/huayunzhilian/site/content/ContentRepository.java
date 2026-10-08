package cn.huayunzhilian.site.content;

import java.sql.Date;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;
import tools.jackson.databind.json.JsonMapper;

@Repository
public class ContentRepository {
    private static final String COLUMNS = "content_type, slug, title, summary, category, sort_order, featured, "
            + "published_at, expires_at, authorized, archived, body_json";

    private final JdbcClient jdbc;
    private final JsonMapper json;

    public ContentRepository(JdbcClient jdbc, JsonMapper json) {
        this.jdbc = jdbc;
        this.json = json;
    }

    public List<ContentItem> findPublished(String type) {
        return jdbc.sql("SELECT " + COLUMNS + " FROM content_item WHERE content_type = :type AND status = 'published' "
                        + "AND locale = 'zh' ORDER BY sort_order, id")
                .param("type", type)
                .query(this::map)
                .list();
    }

    public List<ContentItem> findAllPublished() {
        return jdbc.sql("SELECT " + COLUMNS + " FROM content_item WHERE status = 'published' AND locale = 'zh' "
                        + "ORDER BY content_type, sort_order, id")
                .query(this::map)
                .list();
    }

    public Optional<ContentItem> findOne(String type, String slug) {
        return jdbc.sql("SELECT " + COLUMNS + " FROM content_item WHERE content_type = :type AND slug = :slug "
                        + "AND status = 'published' AND locale = 'zh'")
                .param("type", type)
                .param("slug", slug)
                .query(this::map)
                .optional();
    }

    private ContentItem map(ResultSet rs, int row) throws SQLException {
        Date pub = rs.getDate("published_at");
        Date exp = rs.getDate("expires_at");
        return new ContentItem(
                rs.getString("content_type"), rs.getString("slug"), rs.getString("title"), rs.getString("summary"),
                rs.getString("category"), rs.getInt("sort_order"), rs.getBoolean("featured"),
                pub == null ? null : pub.toLocalDate(), exp == null ? null : exp.toLocalDate(),
                rs.getBoolean("authorized"), rs.getBoolean("archived"), null,
                json.readTree(rs.getString("body_json")));
    }
}
