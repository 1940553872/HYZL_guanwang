package cn.huayunzhilian.site;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

/** 华云智联官网 V2.0 内容与业务服务（design_document/K-05）。 */
@SpringBootApplication
@ConfigurationPropertiesScan
public class SiteApplication {
    public static void main(String[] args) {
        SpringApplication.run(SiteApplication.class, args);
    }
}
