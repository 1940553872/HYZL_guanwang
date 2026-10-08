package cn.huayunzhilian.site.admin;

import cn.huayunzhilian.site.common.ApiException;
import cn.huayunzhilian.site.common.HyzlProperties;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

/**
 * 后台接口令牌校验（当前版本的简化鉴权）。生产环境按 K-05 §5 替换为 OIDC 单点登录 + RBAC。
 */
@Component
public class AdminTokenInterceptor implements HandlerInterceptor {
    private final HyzlProperties props;

    public AdminTokenInterceptor(HyzlProperties props) {
        this.props = props;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String token = props.admin().token();
        if (token == null || token.isBlank()) {
            throw new ApiException(HttpStatus.FORBIDDEN, "ADMIN_DISABLED", "后台接口未启用（未配置 HYZL_ADMIN_TOKEN）");
        }
        String header = request.getHeader("Authorization");
        String given = header != null && header.startsWith("Bearer ") ? header.substring(7) : "";
        if (!MessageDigest.isEqual(token.getBytes(StandardCharsets.UTF_8), given.getBytes(StandardCharsets.UTF_8))) {
            throw new ApiException(HttpStatus.UNAUTHORIZED, "UNAUTHORIZED", "未登录或令牌无效");
        }
        request.setAttribute("actor", "admin-token");
        return true;
    }
}
