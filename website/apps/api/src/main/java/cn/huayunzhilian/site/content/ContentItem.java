package cn.huayunzhilian.site.content;

import java.time.LocalDate;
import tools.jackson.databind.JsonNode;

/** 一条已发布内容（content_item 表一行）。data 为结构化正文。 */
public record ContentItem(
        String type,
        String slug,
        String title,
        String summary,
        String category,
        int sort,
        boolean featured,
        LocalDate publishedAt,
        LocalDate expiresAt,
        boolean authorized,
        boolean archived,
        String status,
        JsonNode data) {

    public ContentItem withStatus(String newStatus) {
        return new ContentItem(type, slug, title, summary, category, sort, featured, publishedAt, expiresAt,
                authorized, archived, newStatus, data);
    }
}
