package cn.huayunzhilian.site.common;

import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;

/** 业务异常，统一转换为 K-05 §2 的错误体。 */
public class ApiException extends RuntimeException {
    private final HttpStatus status;
    private final String code;
    private final List<Map<String, String>> details;

    public ApiException(HttpStatus status, String code, String message) {
        this(status, code, message, List.of());
    }

    public ApiException(HttpStatus status, String code, String message, List<Map<String, String>> details) {
        super(message);
        this.status = status;
        this.code = code;
        this.details = details;
    }

    public static ApiException notFound(String code, String message) {
        return new ApiException(HttpStatus.NOT_FOUND, code, message);
    }

    public static ApiException badRequest(String field, String rule, String message) {
        return new ApiException(HttpStatus.BAD_REQUEST, "VALIDATION_FAILED", message,
                List.of(Map.of("field", field, "rule", rule)));
    }

    public HttpStatus status() { return status; }
    public String code() { return code; }
    public List<Map<String, String>> details() { return details; }
}
