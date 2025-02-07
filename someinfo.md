# README

## 环境变量ENV_CONFIG

* 示例

``` json
{
    "SERVER":{
        "nacos_host":"",
        "nacos_service_name":"",
        "nacos_group_name":"",
        "server_host":"",
        "server_port":""
    }
}
```

* 具体意义

- config_name: 配置名称: 正式环境='SERVER',测试环境='TEST',本地环境='LOCAL',海外环境='ABROAD'
  - nacos_host: nacos 地址
  - nacos_service_name: nacos 配置服务名称
  - nacos_group_name: nacos 配置组名称
  - server_host: 服务地址
  - server_port: 服务端口


## API接口

### 健康检查调用

``` shell
GET /translate-api/xxxx/health 

curl -X GET 'http://0.0.0.0:7860/health'

```
### 翻译接口

``` shell
 POST /translate-api/google/translate
curl -X POST \
  'http://0.0.0.0:7860/translate' \
  -H 'Content-Type: application/json' \
  -d '{
        "msgId": "1",
        "srcContent": "",
        "taskId": "",
        "nameList": "",
        "languageFrom": "",
        "languageTo": "en",
        "srcDecryptedContent": "我是中国人，你是哪国人？",
        "serverMsgId": "1212",
        "num": 100
    }'

```

## 本地编译测试

``` shell
docker build --no-cache --compress -t goo_translate .
docker run -p 7860:7860 -m 2g -e DEBUG=false goo_translate
```



## 语言代码

```java
public enum Language {

    AF("af", "Afrikaans"),
    SQ("sq", "Albanian"),
    AM("am", "Amharic"),
    AR("ar", "Arabic"),
    HY("hy", "Armenian"),
    AZ("az", "Azerbaijani"),
    EU("eu", "Basque"),
    BE("be", "Belarusian"),
    BN("bn", "Bengali"),
    BS("bs", "Bosnian"),
    BG("bg", "Bulgarian"),
    CA("ca", "Catalan"),
    CEB("ceb", "Cebuano"),
    NY("ny", "Chichewa"),
    ZH_CH("zh_cn", "Chinese Simplified"),
    ZH_TW("zh_tw", "Chinese Traditional"),
    CO("co", "Corsican"),
    HR("hr", "Croatian"),
    CS("cs", "Czech"),
    DA("da", "Danish"),
    NL("nl", "Dutch"),
    EN("en", "English"),
    EO("eo", "Esperanto"),
    ET("et", "Estonian"),
    TL("tl", "Filipino"),
    FI("fi", "Finnish"),
    FR("fr", "French"),
    FY("fy", "Frisian"),
    GL("gl", "Galician"),
    KA("ka", "Georgian"),
    DE("de", "German"),
    EL("el", "Greek"),
    QU("gu", "Gujarati"),
    HT("ht", "Haitian Creole"),
    HA("ha", "Hausa"),
    HAW("haw", "Hawaiian"),
    IW("iw", "Hebrew"),
    HI("hi", "Hindi"),
    HMN("hmn", "Hmong"),
    HU("hu", "Hungarian"),
    IS("is", "Icelandic"),
    IG("ig", "Igbo"),
    ID("id", "Indonesian"),
    GA("ga", "Irish"),
    IT("it", "Italian"),
    JA("ja", "Japanese"),
    JW("jw", "Javanese"),
    KN("kn", "Kannada"),
    KK("kk", "Kazakh"),
    KM("km", "Khmer"),
    KO("ko", "Korean"),
    KU("ku", "Kurdish (Kurmanji)"),
    KY("ky", "Kyrgyz"),
    LO("lo", "Lao"),
    LA("la", "Latin"),
    LV("lv", "Latvian"),
    LT("lt", "Lithuanian"),
    LB("lb", "Luxembourgish"),
    MK("mk", "Macedonian"),
    MG("mg", "Malagasy"),
    MS("ms", "Malay"),
    ML("ml", "Malayalam"),
    MT("mt", "Maltese"),
    MI("mi", "Maori"),
    MR("mr", "Marathi"),
    MN("mn", "Mongolian"),
    MY("my", "Myanmar (Burmese)"),
    NE("ne", "Nepali"),
    NO("no", "Norwegian"),
    PS("ps", "Pashto"),
    FA("fa", "Persian"),
    PL("pl", "Polish"),
    PT("pt", "Portuguese"),
    MA("ma", "Punjabi"),
    RO("ro", "Romanian"),
    RU("ru", "Russian"),
    SM("sm", "Samoan"),
    GD("gd", "Scots Gaelic"),
    SR("sr", "Serbian"),
    ST("st", "Sesotho"),
    SN("sn", "Shona"),
    SD("sd", "Sindhi"),
    SI("si", "Sinhala"),
    SK("sk", "Slovak"),
    SL("sl", "Slovenian"),
    SO("so", "Somali"),
    ES("es", "Spanish"),
    SU("su", "Sundanese"),
    SW("sw", "Swahili"),
    SV("sv", "Swedish"),
    TG("tg", "Tajik"),
    TA("ta", "Tamil"),
    TE("te", "Telugu"),
    TH("th", "Thai"),
    TR("tr", "Turkish"),
    UK("uk", "Ukrainian"),
    UR("ur", "Urdu"),
    UZ("uz", "Uzbek"),
    VI("vi", "Vietnamese"),
    CY("cy", "Welsh"),
    XH("xh", "Xhosa"),
    YI("yi", "Yiddish"),
    YO("yo", "Yoruba"),
    ZU("zu", "Zulu");

    private final String languageCode;
    private final String languageName;

    Language(String languageCode, String languageName) {
        this.languageCode = languageCode;
        this.languageName = languageName;
    }

    public String getLanguageName() {
        return languageName;
    }
    public String getLanguageCode() {
        return languageCode;
    }
}

```