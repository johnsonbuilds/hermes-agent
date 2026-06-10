# Upstream Sync Instructions (上游同步指南)

本文件既是当前 fork 相对 upstream 的差异清单，也是后续同步 upstream repo 时的操作指南。

## 核心原则

- 下文“差异点”章节中的“新增文件”和“修改文件”共同构成需要保留的 fork 差异点清单。
- 后续同步 upstream 最新代码时，必须显式核对并保留下文“差异点”章节中记录的差异点，避免在冲突解决、批量覆盖或清理过程中误删本 fork 的既有定制行为。
- 如果后续本 fork 引入了新的差异点，必须持续补充记录到本文件，保持这里始终是最新、完整的差异来源。

## 当前差异点 (Differences)

### 新增文件 (New Files)
- `.clawcloud.env.example`: ClawCloud 环境配置示例文件。
- `clawcloud-config.yaml.example`: ClawCloud CLI 配置示例文件。

### 修改文件 (Modified Files)
- `gateway/run.py`: 实现了 Telegram Bootstrap 逻辑。当没有任何白名单配置时，自动授权第一个与 Bot 通信的用户为 Owner，并将其 ID 写入 `.env`；实现了主程序就绪后的通知逻辑。当环境变量 `AGENT_GATEWAY_READY_NOTIFY_URL` 被设置时，在 Gateway 启动完成（连接到平台并启动后台任务后）发送一个 GET 请求到该 URL。
- `gateway/pairing.py`: 在 `PairingStore` 中暴露了 `approve_user` 方法，支持程序化自动授权。
- `.github/workflows/docker-publish.yml`: 修改了 Docker 发布工作流（可能包含特定的镜像名称或推送逻辑）。
- `docker/entrypoint.sh`: 使用clawcloud的env,config example文件。
- `Dockerfile`: pip install 只包含必须的依赖项, 使用gateway做为默认启动项。