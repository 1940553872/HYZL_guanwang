package cn.huayunzhilian.site.content;

/** 列表查询参数。 */
public record ContentQuery(String type, String category, Boolean featured, Boolean archived, Integer withinDays,
                           Integer limit) {}
