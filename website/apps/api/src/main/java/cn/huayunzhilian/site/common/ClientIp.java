package cn.huayunzhilian.site.common;

import jakarta.servlet.http.HttpServletRequest;

/**
 * 客户端 IP。代理头（X-Forwarded-For）由 server.forward-headers-strategy=framework 统一处理，
 * 因此这里只取 getRemoteAddr()；API 服务只应暴露在网关 / 前端服务之后（K-07 §1）。
 */
public final class ClientIp {
    private ClientIp() {}

    public static String of(HttpServletRequest request) {
        return request.getRemoteAddr();
    }
}
