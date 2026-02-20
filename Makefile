# ============================================================
#  HarshitOS — Personal Multi-Agent System
# ============================================================
#
#  Development:
#    make dev              Start frontend + backend
#    make frontend         Vite dev server
#    make backend          FastAPI server
#    make voice-server     LiveKit agent worker
#
#  CLI:
#    make cli              Interactive text chat
#    make voice            Interactive voice chat (terminal mic)
#    make ask Q="question" One-shot query
#
#  Pipeline:
#    make ingest           Index new/changed content
#    make reindex          Force reindex everything
#    make status           Show what would be indexed
#    make clear            Clear index state
#
#  Testing:
#    make test             Run all tests
#    make test-core        Test core/ module only
#    make test-agents      Test agents/ module only
#    make test-voice       Test voice/ module only
#    make test-pipeline    Test pipeline/ module only
#    make test-agent-api   Curl test against running backend
#
#  Auth:
#    make auth-gmail       OAuth flow for Gmail
#    make auth-outlook     OAuth flow for Outlook
#
#  Build & Deploy:
#    make build            Build frontend for production
#    make deploy           Build + commit + push
#    make setup            Install all dependencies
#
# ============================================================

.PHONY: dev frontend backend voice-server cli voice ask \
        ingest reindex status clear \
        test test-core test-agents test-voice test-pipeline test-agent-api \
        auth-gmail auth-outlook \
        build deploy setup help

PYTHON := python3
PYTHONPATH_SET := PYTHONPATH=.

# ── Development ───────────────────────────────────────────────

dev: ## Start frontend + backend in parallel
	@echo "Starting HarshitOS dev environment..."
	@make -j2 frontend backend

frontend: ## Start Vite dev server
	npx vite --port 5173

backend: ## Start FastAPI backend
	$(PYTHONPATH_SET) uvicorn backend.main:app --reload --port 8000

voice-server: ## Start LiveKit agent worker
	$(PYTHONPATH_SET) $(PYTHON) -m voice.livekit_agent

# ── CLI ───────────────────────────────────────────────────────

cli: ## Interactive text chat
	$(PYTHONPATH_SET) $(PYTHON) -m cli.main chat

voice: ## Interactive voice mode (terminal mic/speaker)
	$(PYTHONPATH_SET) $(PYTHON) -m cli.main voice

ask: ## One-shot query: make ask Q="What does Harshit do?"
	$(PYTHONPATH_SET) $(PYTHON) -m cli.main ask "$(Q)"

# ── Pipeline ──────────────────────────────────────────────────

ingest: ## Index new/changed content
	$(PYTHONPATH_SET) $(PYTHON) -m pipeline.ingest

reindex: ## Force reindex ALL documents
	$(PYTHONPATH_SET) $(PYTHON) -m pipeline.ingest --force

status: ## Show what would be indexed (dry run)
	$(PYTHONPATH_SET) $(PYTHON) -m pipeline.ingest --status

clear: ## Clear index state
	$(PYTHONPATH_SET) $(PYTHON) -m pipeline.ingest --clear

# ── Testing ───────────────────────────────────────────────────

test: ## Run all tests
	$(PYTHONPATH_SET) $(PYTHON) -m pytest tests/ -v

test-core: ## Test core/ module
	$(PYTHONPATH_SET) $(PYTHON) -m pytest tests/test_core.py -v

test-agents: ## Test agents/ module
	$(PYTHONPATH_SET) $(PYTHON) -m pytest tests/test_agents.py -v

test-voice: ## Test voice/ module
	$(PYTHONPATH_SET) $(PYTHON) -m pytest tests/test_voice.py -v

test-pipeline: ## Test pipeline/ module
	$(PYTHONPATH_SET) $(PYTHON) -m pytest tests/test_pipeline.py -v

test-agent-api: ## Curl test against running backend
	@curl -s -X POST http://localhost:8000/api/chat \
		-H "Content-Type: application/json" \
		-d '{"query": "What does Harshit do?"}' | $(PYTHON) -m json.tool

# ── Auth ──────────────────────────────────────────────────────

auth-gmail: ## Run Gmail OAuth flow
	$(PYTHONPATH_SET) $(PYTHON) -m cli.main auth gmail

auth-outlook: ## Run Outlook OAuth flow
	$(PYTHONPATH_SET) $(PYTHON) -m cli.main auth outlook

# ── Build & Deploy ────────────────────────────────────────────

build: ## Build frontend for production
	npm run build

deploy: build ## Build, commit, push (triggers Vercel + Render)
	@echo ""
	@echo "Deploying to production..."
	git add -A
	@if git diff --cached --quiet; then \
		echo "No changes to deploy."; \
	else \
		git commit -m "deploy: $$(date '+%Y-%m-%d %H:%M')"; \
		git push; \
		echo ""; \
		echo "Pushed — Vercel + Render will auto-deploy."; \
	fi

# ── Setup ─────────────────────────────────────────────────────

setup: ## Install all dependencies
	npm install
	pip install -r backend/requirements.txt
	pip install -r pipeline/requirements.txt
	pip install pytest pytest-asyncio  # test deps
	@mkdir -p data
	@echo ""
	@echo "Dependencies installed."
	@echo "  Set API keys in .env.local (see .env.example)"
	@echo "  Run 'make dev' to start developing"
	@echo "  Run 'make test' to verify scaffold"

# ── Help ──────────────────────────────────────────────────────

help: ## Show all commands
	@echo "HarshitOS Agent System Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
