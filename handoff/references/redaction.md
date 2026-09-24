# 脱敏规范

## 必须脱敏的类别

| 类别 | 示例 | 替换为 |
|---|---|---|
| API key / token | `sk-abc123…` | `[REDACTED:API_KEY]` |
| 密码 / 密钥 | 数据库密码、SSH 私钥 | `[REDACTED:SECRET]` |
| 连接串中的凭证 | `postgres://user:pass@host` | `postgres://[REDACTED]@host` |
| 个人身份信息 | 真实姓名、邮箱、手机号、身份证号 | `[REDACTED:PII]` |

## 两条铁律

1. **脱敏不等于删信息。** 必须留下指路信息，让下一个 agent 能恢复工作：
    - ✅ `API key 见项目根目录 .env 的 OPENAI_API_KEY`
    - ✅ `数据库密码在团队 1Password 的 "staging-db" 条目`

2. **占位符要带类别。** 统一用 `[REDACTED:类别]` 格式，
   便于下一个 agent 识别此处原本是什么、去哪里找。

## 保存前最后一遍扫描

对全文检索以下模式，确认无漏网：
`key`、`token`、`secret`、`password`、`Bearer `、
`-----BEGIN`、形如邮箱/手机号的字符串、含 `:@` 的连接串。
