package cn.huayunzhilian.site.common;

import cn.huayunzhilian.site.admin.AdminTokenInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    private final HyzlProperties props;
    private final AdminTokenInterceptor adminInterceptor;

    public WebConfig(HyzlProperties props, AdminTokenInterceptor adminInterceptor) {
        this.props = props;
        this.adminInterceptor = adminInterceptor;
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins(props.cors().allowedOrigins().toArray(String[]::new))
                .allowedMethods("GET", "POST")
                .maxAge(3600);
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(adminInterceptor).addPathPatterns("/admin/**");
    }
}
