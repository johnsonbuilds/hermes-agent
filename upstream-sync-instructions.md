# Upstream Sync Instructions (上游同步指南)

本文件既是当前 fork 相对 upstream 的差异清单，也是后续同步 upstream repo 时的操作指南。

## 核心原则

- 下文"差异点"章节中的"新增文件"和"修改文件"共同构成需要保留的 fork 差异点清单。
- 后续同步 upstream 最新代码时，必须显式核对并保留下文"差异点"章节中记录的差异点，避免在冲突解决、批量覆盖或清理过程中误删本 fork 的既有定制行为。
- 如果后续本 fork 引入了新的差异点，必须持续准确记录到本文件，保持这里始终是最新、完整和准确的差异来源。

## 当前差异点 (Differences)

分为：新增文件和修改文件两类，每类下面按文件路径列出，同一个文件下的不同差异点分别列出，不要混在一起写。

### 新增文件 (New Files)

- `.clawcloud.env.example`: ClawCloud 环境配置示例文件。

- `clawcloud-config.yaml.example`: ClawCloud CLI 配置示例文件。

- `gateway/getclawcloud.py`: 新增 Gateway 就绪通知模块，封装 `AGENT_GATEWAY_READY_NOTIFY_URL` 对应的 GET 通知逻辑。

- `skills/creative/wavespeed/SKILL.md`: 新增wavespeed内置skill.

- `skills/governance/skill-health-check/SKILL.md`: 新增skill-health-check内置skill.

### 修改文件 (Modified Files)

- `gateway/run.py`

 1. 实现了主程序就绪后的通知逻辑。在 Gateway 启动完成调用notify_gateway_ready发送一个 GET 请求到该 URL；

 2. 修复了 Gateway 直接读取 `config.yaml` 时未展开 `${ENV_VAR}` 的问题。特别修复了 `_load_gateway_config()` 在命中 `read_raw_config()` 快路径时跳过展开的 bug，确保所有路径都经过 `_expand_env_vars` 处理，避免 `model.default` 等字段将字面量占位符传入运行时。

 3. 更改 `_gateway_provider_error_reply()` 中的 rate-limit 提示语：将 "⏱️ The model provider is rate-limiting requests. Please wait a moment and try again." 改为指向 `https://hermesagentcloud.com/home?openByoKey=true` 的自定义文案。

- `gateway/authz_mixin.py`:承接并实现了 Telegram Bootstrap 逻辑（原位于 `gateway/run.py`，随 upstream 重构迁移至此）。当没有任何白名单配置时，自动授权第一个与 Bot 通信的用户为 Owner，并将其 ID 写入 `.env`。

- `gateway/pairing.py`: 在 `PairingStore` 中暴露了 `approve_user` 方法，支持程序化自动授权。

- `docker/stage2-hook.sh`: 

1. s6-overlay 的 stage2 启动钩子。首启动 seed 配置时使用 clawcloud 的 env/config example 文件（`.clawcloud.env.example` / `clawcloud-config.yaml.example`），而非 upstream 的 `.env.example` / `cli-config.yaml.example`。
2. add `reconcile_files` before gateway start, ensure deterministic ownership reconciliation for /opt/data runtime files
3. modify `seed_one`,deterministic write and enforce ownership explicitly

- `docker/main-wrapper.sh`: s6-overlay 容器主程序包装脚本。无参数（默认）启动时执行 `hermes gateway`（而非裸 `hermes`），保留 fork 以 gateway 为默认启动项的契约。

- `docker/entrypoint.sh`: 已随 upstream 迁移为 s6-overlay 的废弃转发 shim（实际逻辑移至 `docker/stage2-hook.sh`）。clawcloud 配置注入逻辑现位于 `docker/stage2-hook.sh`。

- `Dockerfile`: pip install 只包含必须的依赖项（slim extras: messaging/cron/cli/pty/mcp/acp/dingtalk/feishu，不使用 `[all]`）。已随 upstream 迁移到 s6-overlay：`ENTRYPOINT [ \"/init\", \".../main-wrapper.sh\" ]`，gateway 默认启动项的实现移至 `docker/main-wrapper.sh`。

- `tests/gateway/test_config.py`: 新增 Gateway 配置环境变量展开测试，覆盖 `model.*` 字段和 `_resolve_gateway_model()` 返回值。

- `tests/gateway/test_status_command.py`: 新增 Telegram home channel onboarding 回归测试，覆盖环境变量缺失但运行时 `GatewayConfig` 已存在 home channel 时不应发送 `/sethome` 提示。

- `README.md,README.zh-CN.md`: 更改为hermesagentcloud版本，后续不用随upstream同步

- `tools/skills_hub.py`: GitHubSource-DEFAULT_TAPS添加johnsonbuilds/awesome-hermes-skills。
