# Upstream Sync Instructions (上游同步指南)

本文件既是当前 fork 相对 upstream 的差异清单，也是后续同步 upstream repo 时的操作指南。

## 核心原则

- 下文“差异点”章节中的“新增文件”和“修改文件”共同构成需要保留的 fork 差异点清单。
- 后续同步 upstream 最新代码时，必须显式核对并保留下文“差异点”章节中记录的差异点，避免在冲突解决、批量覆盖或清理过程中误删本 fork 的既有定制行为。
- 如果后续本 fork 引入了新的差异点，必须持续准确记录到本文件，保持这里始终是最新、完整和准确的差异来源。

## 当前差异点 (Differences)

分为：新增文件和修改文件两类，每类下面按文件路径列出，同一个文件下的不同差异点分别列出，不要混在一起写。

### 新增文件 (New Files)

- `.clawcloud.env.example`: ClawCloud 环境配置示例文件。

- `clawcloud-config.yaml.example`: ClawCloud CLI 配置示例文件。

- `gateway/getclawcloud.py`: 新增 Gateway 就绪通知模块，封装 `AGENT_GATEWAY_READY_NOTIFY_URL` 对应的 GET 通知逻辑。

### 修改文件 (Modified Files)

- `gateway/run.py`: 
 - 实现了 Telegram Bootstrap 逻辑。当没有任何白名单配置时，自动授权第一个与 Bot 通信的用户为 Owner，并将其 ID 写入 `.env`；
 - 实现了主程序就绪后的通知逻辑。在 Gateway 启动完成调用notify_gateway_ready发送一个 GET 请求到该 URL；
 - 修复了 Gateway 直接读取 `config.yaml` 时未展开 `${ENV_VAR}` 的问题，改为复用配置环境变量展开逻辑`_expand_env_vars`，避免 `model.default` / `model.provider` / `model.base_url` / `model.api_key` 将字面量占位符传入运行时。

- `gateway/pairing.py`: 在 `PairingStore` 中暴露了 `approve_user` 方法，支持程序化自动授权。

- `docker/stage2-hook.sh`: s6-overlay 的 stage2 启动钩子。首启动 seed 配置时使用 clawcloud 的 env/config example 文件（`.clawcloud.env.example` / `clawcloud-config.yaml.example`），而非 upstream 的 `.env.example` / `cli-config.yaml.example`。

- `docker/main-wrapper.sh`: s6-overlay 容器主程序包装脚本。无参数（默认）启动时执行 `hermes gateway`（而非裸 `hermes`），保留 fork 以 gateway 为默认启动项的契约。

- `docker/entrypoint.sh`: 已随 upstream 迁移为 s6-overlay 的废弃转发 shim（实际逻辑移至 `docker/stage2-hook.sh`）。clawcloud 配置注入逻辑现位于 `docker/stage2-hook.sh`。

- `Dockerfile`: pip install 只包含必须的依赖项（slim extras: messaging/cron/cli/pty/mcp/acp/dingtalk/feishu，不使用 `[all]`）。已随 upstream 迁移到 s6-overlay：`ENTRYPOINT [ "/init", ".../main-wrapper.sh" ]`，gateway 默认启动项的实现移至 `docker/main-wrapper.sh`。

- `tests/gateway/test_config.py`: 新增 Gateway 配置环境变量展开测试，覆盖 `model.*` 字段和 `_resolve_gateway_model()` 返回值。