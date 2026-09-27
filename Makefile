FRONTEND_DIR := frontend/main-app
DEVICE_DIR   := backend/device-service
AI_DIR       := backend/ai-service

.PHONY: help up down install install-frontend install-device install-ai \
        dev dev-frontend dev-device dev-ai \
        build build-frontend build-device start-frontend start-device lint \
        qdrant-up qdrant-down qdrant-logs clear-vertical-db reindex \
        migration-run migration-revert migration-show migration-generate

help:
	@echo "Run everything:"
	@echo "  make up                   start Qdrant and all three services"
	@echo "  make down                 stop Qdrant"
	@echo ""
	@echo "Install:"
	@echo "  make install              install dependencies for all services"
	@echo "  make install-frontend     pnpm install in frontend"
	@echo "  make install-device       pnpm install in device-service"
	@echo "  make install-ai           uv sync in ai-service"
	@echo ""
	@echo "Development:"
	@echo "  make dev                  run all three services in parallel"
	@echo "  make dev-frontend         Next.js (pnpm dev)"
	@echo "  make dev-device           device-service (pnpm start:dev)"
	@echo "  make dev-ai               ai-service (uv run packman-ai-service)"
	@echo ""
	@echo "Build and production:"
	@echo "  make build                build frontend and device-service"
	@echo "  make start-frontend       next start"
	@echo "  make start-device         node dist/main.js"
	@echo "  make lint                 eslint in frontend"
	@echo ""
	@echo "Qdrant:"
	@echo "  make qdrant-up            docker compose up -d"
	@echo "  make qdrant-down          docker compose down"
	@echo "  make qdrant-logs          follow Qdrant logs"
	@echo "  make clear-vertical-db    clear the vertical DB"
	@echo "  make reindex              re-index all devices with the current pipeline"
	@echo ""
	@echo "device-service migrations (TypeORM):"
	@echo "  make migration-run"
	@echo "  make migration-revert"
	@echo "  make migration-show"
	@echo "  make migration-generate NAME=src/migrations/Name"

up: qdrant-up
	@$(MAKE) -j3 --no-print-directory dev-frontend dev-device dev-ai

down: qdrant-down

install: install-frontend install-device install-ai

install-frontend:
	cd $(FRONTEND_DIR) && pnpm install

install-device:
	cd $(DEVICE_DIR) && pnpm install

install-ai:
	cd $(AI_DIR) && uv sync

dev:
	@$(MAKE) -j3 --no-print-directory dev-frontend dev-device dev-ai

dev-frontend:
	cd $(FRONTEND_DIR) && pnpm dev

dev-device:
	cd $(DEVICE_DIR) && pnpm start:dev

dev-ai:
	cd $(AI_DIR) && uv run packman-ai-service

build: build-frontend build-device

build-frontend:
	cd $(FRONTEND_DIR) && pnpm build

build-device:
	cd $(DEVICE_DIR) && pnpm build

start-frontend:
	cd $(FRONTEND_DIR) && pnpm start

start-device:
	cd $(DEVICE_DIR) && pnpm start

lint:
	cd $(FRONTEND_DIR) && pnpm lint

qdrant-up:
	cd $(AI_DIR) && docker compose up -d
	@echo "Dashboard: http://localhost:6333/dashboard"

qdrant-down:
	cd $(AI_DIR) && docker compose down

qdrant-logs:
	cd $(AI_DIR) && docker compose logs -f qdrant

clear-vertical-db:
	cd $(AI_DIR) && uv run packman-clear-vertical-db

reindex:
	cd $(AI_DIR) && uv run packman-reindex-devices

migration-run:
	cd $(DEVICE_DIR) && pnpm migration:run

migration-revert:
	cd $(DEVICE_DIR) && pnpm migration:revert

migration-show:
	cd $(DEVICE_DIR) && pnpm migration:show

migration-generate:
	@test -n "$(NAME)" || (echo "NAME is required, for example: make migration-generate NAME=src/migrations/AddDevice" && exit 1)
	cd $(DEVICE_DIR) && pnpm migration:generate $(NAME)

.DEFAULT_GOAL := help
