package cn.huayunzhilian.site.lead;

import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/** 预约演示 / 联系 / 合作线索（K-05 §2.2）。 */
public record LeadRequest(
        @Pattern(regexp = "demo|contact|partner|job", message = "线索类型不正确") String type,
        @NotBlank(message = "请填写姓名") @Size(max = 50, message = "姓名不超过50个字") String name,
        @NotBlank(message = "请填写公司名称") @Size(max = 100, message = "公司名称不超过100个字") String company,
        @Size(max = 50, message = "职位不超过50个字") String title,
        @Size(max = 30, message = "手机号格式不正确") String phone,
        @Email(message = "邮箱格式不正确") @Size(max = 120, message = "邮箱过长") String email,
        @Size(max = 100, message = "关注产品过长") String productInterest,
        @Size(max = 500, message = "需求描述不超过500个字") String scenario,
        @Pattern(regexp = "zh|en", message = "语言参数不正确") String locale,
        @Size(max = 255) String sourcePage,
        @Size(max = 100) String utmSource,
        @Size(max = 100) String utmMedium,
        @Size(max = 100) String utmCampaign,
        @AssertTrue(message = "请阅读并同意隐私政策") boolean consent,
        @Size(max = 20) String consentVersion,
        @Size(max = 0, message = "请求异常") String website) {
    // website 为蜜罐字段：真实用户看不到、不会填写
}
