# ============================================================
#  HarshitOS Portfolio — Pipeline Commands
# ============================================================
#
#  make dev         Start frontend + backend locally
#  make frontend    Start Vite dev server
#  make backend     Start FastAPI server
#
#  make ingest      Index new/changed content into knowledge graph
#  make reindex     Force reindex ALL content
#  make status      Show what would be indexed (dry run)
#  make clear       Clear index state (next ingest reindexes all)
#
#  make build       Build frontend for production
#  make deploy      Build → commit → push (triggers Vercel + Render)
#
#  make prompt      Edit the agent system prompt
#  make test-agent  Send a test query to the local backend
# ============================================================

.PHONY: dev frontend backend ingest reindex status clear build deploy prompt test-agent setup help

# ── Development ───────────────────────────────────────────────

dev: ## Start frontend + backend in parallel
	@echo "Starting HarshitOS dev environment..."
	@make -j2 frontend backend

frontend: ## Start Vite dev server
	npx vite --port 5173

backend: ## Start FastAPI backend
	PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

# ── Pipeline: Data Ingestion ──────────────────────────────────

ingest: ## Index new/changed content into the knowledge graph
	PYTHONPATH=. python3 -m pipeline.ingest

reindex: ## Force reindex ALL documents
	PYTHONPATH=. python3 -m pipeline.ingest --force

status: ## Show what would be indexed (dry run)
	PYTHONPATH=. python3 -m pipeline.ingest --status

clear: ## Clear index state (next ingest reindexes everything)
	PYTHONPATH=. python3 -m pipeline.ingest --clear

# ── Build & Deploy ────────────────────────────────────────────

build: ## Build frontend for production
	npm run build

deploy: build ## Build, commit, and push (triggers Vercel + Render)
	@echo ""
	@echo "Deploying to production..."
	git add -A
	@if git diff --cached --quiet; then \
		echo "No changes to deploy."; \
	else \
		git commit -m "deploy: $$(date '+%Y-%m-%d %H:%M')"; \
		git push; \
		echo ""; \
		echo "✓ Pushed to GitHub — Vercel + Render will auto-deploy."; \
	fi

# ── Pipeline: Prompt Engineering ──────────────────────────────

prompt: ## Open the agent system prompt for editing
	@echo "System prompt: pipeline/prompts/system.md"
	@echo "Extraction prompt: pipeline/prompts/extraction.md"
	@echo "Query prompt: pipeline/prompts/query.md"
	@echo ""
	@echo "Edit these files, then run 'make deploy' to push changes."

# ── Testing ───────────────────────────────────────────────────

test-agent: ## Send a test query to the local backend
	@curl -s -X POST http://localhost:8000/api/chat \
		-H "Content-Type: application/json" \
		-d '{"query": "What does Harshit do?"}' | python3 -m json.tool

# ── Setup ─────────────────────────────────────────────────────

setup: ## Install all dependencies (frontend + backend + pipeline)
	npm install
	pip install -r backend/requirements.txt
	pip install -r pipeline/requirements.txt
	@echo ""
	@echo "✓ Dependencies installed."
	@echo "  → Set GROQ_API_KEY in .env.local"
	@echo "  → Run 'make dev' to start developing"

# ── Help ──────────────────────────────────────────────────────

help: ## Show this help
	@echo "HarshitOS Portfolio Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
