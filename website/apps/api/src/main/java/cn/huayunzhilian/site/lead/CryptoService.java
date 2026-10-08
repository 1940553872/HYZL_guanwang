package cn.huayunzhilian.site.lead;

import cn.huayunzhilian.site.common.HyzlProperties;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Base64;
import java.util.HexFormat;
import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.stereotype.Service;

/**
 * 个人信息字段加密（K-05 §5）：SM4-GCM 加密存储，HMAC-SHA256 哈希用于去重检索。
 * 密钥来自配置；生产环境由 KMS 注入，不得使用默认值。
 */
@Service
public class CryptoService {
    private static final int IV_LEN = 12;
    private static final int TAG_BITS = 128;

    static {
        if (Security.getProvider(BouncyCastleProvider.PROVIDER_NAME) == null) {
            Security.addProvider(new BouncyCastleProvider());
        }
    }

    private final SecretKeySpec sm4Key;
    private final SecretKeySpec hmacKey;
    private final SecureRandom random = new SecureRandom();

    public CryptoService(HyzlProperties props) {
        byte[] key = Base64.getDecoder().decode(props.crypto().sm4Key());
        if (key.length != 16) {
            throw new IllegalStateException("hyzl.crypto.sm4-key 必须是 16 字节（Base64 编码）");
        }
        this.sm4Key = new SecretKeySpec(key, "SM4");
        this.hmacKey = new SecretKeySpec(props.crypto().hmacKey().getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    }

    public String encrypt(String plain) {
        if (plain == null) {
            return null;
        }
        try {
            byte[] iv = new byte[IV_LEN];
            random.nextBytes(iv);
            Cipher c = Cipher.getInstance("SM4/GCM/NoPadding", BouncyCastleProvider.PROVIDER_NAME);
            c.init(Cipher.ENCRYPT_MODE, sm4Key, new GCMParameterSpec(TAG_BITS, iv));
            byte[] ct = c.doFinal(plain.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(ByteBuffer.allocate(iv.length + ct.length).put(iv).put(ct).array());
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException("加密失败", e);
        }
    }

    public String decrypt(String encoded) {
        if (encoded == null) {
            return null;
        }
        try {
            byte[] all = Base64.getDecoder().decode(encoded);
            Cipher c = Cipher.getInstance("SM4/GCM/NoPadding", BouncyCastleProvider.PROVIDER_NAME);
            c.init(Cipher.DECRYPT_MODE, sm4Key, new GCMParameterSpec(TAG_BITS, all, 0, IV_LEN));
            return new String(c.doFinal(all, IV_LEN, all.length - IV_LEN), StandardCharsets.UTF_8);
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException("解密失败", e);
        }
    }

    public String hash(String value) {
        if (value == null) {
            return null;
        }
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            mac.init(hmacKey);
            return HexFormat.of().formatHex(mac.doFinal(value.getBytes(StandardCharsets.UTF_8)));
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException("哈希失败", e);
        }
    }
}
