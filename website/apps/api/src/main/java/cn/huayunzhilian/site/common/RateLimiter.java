package cn.huayunzhilian.site.common;

import java.time.Duration;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

/**
 * 进程内滑动窗口限流（K-05 §2 限流策略）。
 * 单实例足够本地与小规模部署；多副本部署时替换为 Redis 实现（见 website/docs/adr/0003）。
 */
@Component
public class RateLimiter {
    private final Map<String, Deque<Long>> windows = new ConcurrentHashMap<>();

    /** 超过阈值时抛出 429。 */
    public void check(String bucket, String key, int limit, Duration window) {
        if (!tryAcquire(bucket, key, limit, window)) {
            throw new ApiException(HttpStatus.TOO_MANY_REQUESTS, "RATE_LIMITED", "请求过于频繁，请稍后再试");
        }
    }

    public boolean tryAcquire(String bucket, String key, int limit, Duration window) {
        long now = System.currentTimeMillis();
        long from = now - window.toMillis();
        Deque<Long> q = windows.computeIfAbsent(bucket + ":" + key, k -> new ArrayDeque<>());
        synchronized (q) {
            while (!q.isEmpty() && q.peekFirst() < from) {
                q.pollFirst();
            }
            if (q.size() >= limit) {
                return false;
            }
            q.addLast(now);
            return true;
        }
    }

    /** 测试用：清空计数。 */
    public void reset() {
        windows.clear();
    }
}
