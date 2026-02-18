Eventa — Design Doc (v0.1)
Overview

Eventa is a local, event-driven personal AI system.
It ingests multimodal messages (text, audio, images), infers user intent using an LLM, and executes deterministic actions (food logging, recommendations, todos, workouts).

Discord is used as the primary UI. All intelligence runs locally.

Goals

Local-first, privacy-preserving
Event-driven, loosely coupled services
Multimodal (text, audio, image)
Deterministic tool execution
Long-term memory & personalization

Discord
  ↓
Ingress (Bot)
  ↓
Event Bus (NATS)
  ↓
ASR 
  ↓
LLM Router
  ↓
Tool Services
  ↓
Storage (DB + Vector)

Core Components
1. Ingress Service

Receives Discord messages (text/audio/image)
Normalizes input into events
Publishes to event bus

2. Event Bus

NATS + JetStream
Subject-based routing
Message persistence & replay


5. Tool Services

Food logger
Food recommender
Todo manager
Workout tracker
Pure, deterministic logic

6. Storage
Postgres / SQLite: structured data

Language 
Python
Payload - protobuf

{
  "event_id": "uuid",
  "user_id": "arnab",
  "modality": "text|audio|image",
  "payload": {},
  "metadata": {}
}
