# Autonomous Multi-Agent AI Salon Platform

## Project Goal
A fully-local, serverless, open-source intelligent salon management system leveraging continuous learning AI agents optimized for Indian market needs, inspired by Respark, Zylu, Plai.io, and AdCreative.ai plus advanced RL-driven UX.

---

## Architecture Highlights
- Modular **multi-agent** design (Scheduler, CRM, Marketing, Inventory, Voice, Chat, Analytics, Ads, etc)
- Orchestrated by Supervisor agents using ZeroMQ messaging
- **Reinforcement Learning** driven optimization of UI, pricing, scheduling, marketing
- Continuous self-learning pipelines with autonomous data ingestion and model retraining
- Integrated **Google APIs** (MyBusiness, Maps, Ads) for bookings and promotions
- **Meta APIs** (Facebook, Instagram, Ads) for social reach
- WhatsApp cloud API for messaging, invoicing, catalogs
- Local LLM for conversational experience in natural Indian voice
- **Role-based API security**, data encryption, and compliance features

---

## Core Modules
...

## Modules and Responsibilities

### Scheduler Agent
- Handles appointment booking, calendar management
- Optimized using RL to maximize occupancy, reduce idle time and no-shows

### Customer Service (Chatbot & Voice)
- Voice+chat reception in natural Indian accent
- Handles FAQs, bookings, follow-ups
- Adaptive personality driven by RL + LLM tuning

### Marketing & Campaigns
- Personalized offers, segmentation
- AI-generated content, images (adcreative.ai inspired)
- Multichannel dispatch: WhatsApp, SMS, email

### Ads Manager Agent
- Integrates with Google, Meta Ads API
- Generates targeted ads, optimizes spending
- Analyzes ROI and retargeting

### CRM & Loyalty
- Centralizes profiles, memberships, referrals
- Collects sentiment, automates loyalty rewards

### Inventory & Staff
- Monitors product stock, staff presence
- Suggests reorder/promo deals

### Analytics & Dashboards
- Real-time KPIs, RL reward progress
- Explainability insights

---

## Self-Learning Pipeline
- Event + scenario simulation inputs
- Reward shaping per agent goals
- RL + LLM model training (continuous + periodic)
- Performance monitoring and rollback
- Data privacy preserved via federated + synthetic data options

---

## Deployment
- Docker Compose + K8s manifests inside `/ai_salon_devops/`
- Secure secrets, TLS, encrypted storage
- Incremental updates via CI/CD

---

## API Integrations
- Google My Business, Maps, Ads
- Facebook & Instagram 
- WhatsApp Cloud
- Modular wrappers in `/root/`

---

## Security
- Role-based JWT auth
- TLS encryption everywhere
- Audit logs and anomaly detection

---

## Extensibility
- Add special agents / plugins
- Extend RL reward schemes
- Fine-tune to new markets

---

## Getting Started
1. Clone repo
2. Setup .env secrets/API keys
3. Deploy Docker Compose or Kubernetes
4. Access dashboards, APIs, voice/chat


