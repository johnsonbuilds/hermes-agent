# Upstream Sync Instructions (上游同步指南)

本文件既是当前 fork 相对 upstream 的差异清单，也是后续同步 upstream repo 时的操作指南。

## 核心原则

- 下文"差异点"章节中的"新增文件"和"修改文件"共同构成需要保留的 fork 差异点清单。
- 后续同步 upstream 最新代码时，必须显式核对并保留下文"差异点"章节中记录的差异点，避免在冲突解决、批量覆盖或清理过程中误删本 fork 的既有定制行为。
- 如果后续本 fork 引入了新的差异点，必须持续准确记录到本文件，保持这里始终是最新、完整和准确的差异来源。

## 当前差异点 (Differences)

> 注（2026-10-08）：原 Telegram Bootstrap 定制（`gateway/authz_mixin.py` 首用户自动授权 + `gateway/pairing.py` 的 `approve_user` 公开方法）已按需求移除，两文件恢复上游原样，后续同步无需保留。

分为：新增文件和修改文件两类，每类下面按文件路径列出，同一个文件下的不同差异点分别列出，不要混在一起写。

### 新增文件 (New Files)

- `.clawcloud.env.example`: ClawCloud 环境配置示例文件。

- `clawcloud-config.yaml.example`: ClawCloud CLI 配置示例文件。

- `gateway/getclawcloud.py`: 新增 Gateway 就绪通知模块，封装 `AGENT_GATEWAY_READY_NOTIFY_URL` 对应的 GET 通知逻辑。

- `skills/creative/wavespeed/SKILL.md`: 新增wavespeed内置skill.

- `skills/governance/skill-health-check/SKILL.md`: 新增skill-health-check内置skill.

### 修改文件 (Modified Files)

- `gateway/run_startup.py`（原 `gateway/run.py` 的通知逻辑，随 upstream 将 run.py 拆分为 facade + `run_*.py` 后迁移至此）

  1. 实现了主程序就绪后的通知逻辑。在 Gateway 启动完成（`Press Ctrl+C to stop` 之后）调用 `notify_gateway_ready()` 发送一个 GET 请求到 `AGENT_GATEWAY_READY_NOTIFY_URL`（见 `gateway/getclawcloud.py`）；

  注：2026-10-08 同步后，以下原 `gateway/run.py` 定制不再需要独立保留：(a) `_load_gateway_config()` 的 `${ENV_VAR}` 展开已由 upstream 通过 `load_user_config_effective()` + `gateway/config_loader.py` 原生实现；(b) 旧的 `home_channel = self.config.get_home_channel(...)` 一行是未被使用的死代码，已丢弃。

- `locales/en.yaml`, `locales/zh.yaml`（原 `gateway/run.py::_gateway_provider_error_reply()` 的 rate-limit 文案，随 upstream 改为 i18n key 后迁移至此）

  1. 更改 `gateway.errors.rate_limited` 为指向 `https://hermesagentcloud.com/home?openByoKey=true` 的自定义引流文案（en 保留英文原文案结构，zh 提供对应中文翻译）。

- `docker/stage2-hook.sh`: 

1. s6-overlay 的 stage2 启动钩子。首启动 seed 配置时使用 clawcloud 的 env/config example 文件（`.clawcloud.env.example` / `clawcloud-config.yaml.example`），而非 upstream 的 `.env.example` / `cli-config.yaml.example`。
2. add `reconcile_files` before gateway start, ensure deterministic ownership reconciliation for /opt/data runtime files
3. modify `seed_one`,deterministic write and enforce ownership explicitly
4. 浏览器部分采用上游新方案（读取 `/etc/hermes/agent-browser-executable-path` 的 baked-path 并 export `AGENT_BROWSER_EXECUTABLE_PATH`），不再保留 fork 旧的 Playwright 目录扫描逻辑；`reconcile_files` 与 clawcloud seed 保留。

- `docker/main-wrapper.sh`: s6-overlay 容器主程序包装脚本。无参数（默认）启动时执行 `hermes gateway`（而非裸 `hermes`），保留 fork 以 gateway 为默认启动项的契约。

- `docker/entrypoint.sh`: 已随 upstream 迁移为 s6-overlay 的废弃转发 shim（实际逻辑移至 `docker/stage2-hook.sh`）。clawcloud 配置注入逻辑现位于 `docker/stage2-hook.sh`。

- `Dockerfile`: pip install 只包含必须的依赖项（slim extras，不使用 `--extra all` / `--all-extras`，避免 `[rl]`/`[yc-bench]` 重依赖；旧 `cli` extra 已不存在故丢弃，当前为 messaging/cron/pty/mcp/acp/dingtalk/feishu + upstream 在 Docker 内必需的 otlp/anthropic/bedrock/azure-identity/matrix/google-chat， via `python3 -m pm.build_env`）。已随 upstream 迁移到 s6-overlay + dispatcher：上游 `ENTRYPOINT` 现为 `entrypoint-dispatch.sh`（PID1 时 exec `/init .../main-wrapper.sh`，兼顾 Fly/`--init` 回退），不再需要 fork 旧的 `ENTRYPOINT ["/init", ".../main-wrapper.sh"]`；gateway 默认启动项的契约仍由 `docker/main-wrapper.sh` 保证。

- `tests/`：按 2026-10-08 决策，测试文件冲突一律取上游，不再保留 fork 回归测试。原 `tests/gateway/test_config.py` 的 env 展开测试已由 upstream 原生覆盖；原 `tests/gateway/test_status_command.py` 的 2 个 Telegram home channel onboarding 测试已丢弃。

- `README.md,README.zh-CN.md`: 更改为hermesagentcloud版本，后续不用随upstream同步

- `.python-version`: 保持 fork 的 `3.12`（除非上游有明确最低版本要求），后续同步不跟随 upstream 的版本 bump。

- `tools/skills_hub_github.py`（原 `tools/skills_hub.py` 的 `GitHubSource.DEFAULT_TAPS`，随 upstream 将 skills_hub 拆分为 facade + `skills_hub_*` siblings 后迁移至此）: `DEFAULT_TAPS` 添加 `johnsonbuilds/awesome-hermes-skills`（`creative/` 路径）。
