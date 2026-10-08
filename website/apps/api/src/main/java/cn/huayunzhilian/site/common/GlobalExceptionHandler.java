package cn.huayunzhilian.site.common;

import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.resource.NoResourceFoundException;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ApiException.class)
    ResponseEntity<ApiError> handle(ApiException e) {
        return ResponseEntity.status(e.status()).body(new ApiError(e.code(), e.getMessage(), requestId(), e.details()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ApiError> handle(MethodArgumentNotValidException e) {
        List<Map<String, String>> details = e.getBindingResult().getFieldErrors().stream()
                .map(f -> Map.of("field", f.getField(), "rule", String.valueOf(f.getCode()), "message",
                        String.valueOf(f.getDefaultMessage())))
                .toList();
        String message = details.isEmpty() ? "参数校验失败" : details.get(0).get("message");
        return ResponseEntity.badRequest().body(new ApiError("VALIDATION_FAILED", message, requestId(), details));
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    ResponseEntity<ApiError> handle(HttpMessageNotReadableException e) {
        return ResponseEntity.badRequest().body(new ApiError("BAD_REQUEST", "请求体格式错误", requestId(), List.of()));
    }

    @ExceptionHandler(NoResourceFoundException.class)
    ResponseEntity<ApiError> handle(NoResourceFoundException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiError("NOT_FOUND", "资源不存在", requestId(), List.of()));
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<ApiError> handle(Exception e) {
        log.error("unhandled error", e);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new ApiError("INTERNAL_ERROR", "服务暂时不可用，请稍后重试", requestId(), List.of()));
    }

    private static String requestId() {
        return MDC.get(RequestIdFilter.MDC_KEY);
    }
}
