package cn.huayunzhilian.site.common;

import java.util.List;
import java.util.Map;

/** 统一错误体：{ code, message, requestId, details }。 */
public record ApiError(String code, String message, String requestId, List<Map<String, String>> details) {}
