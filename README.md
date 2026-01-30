# 🪝 Webhook Repo

> A Flask-based webhook receiver service that ingests GitHub events and persists them into a MongoDB Atlas cluster.

- This repository represents the backend ingestion layer of the system.
- It receives webhook POST requests from the `action-repo`.
- Validates and extracts relevant event data.
- Stores structured logs in a MongoDB Atlas cluster.
- The service is deployed on Render, with sensitive configuration handled via environment variables.

## Table of Contents

1. [Tech Stack and Prerequisites](#1-tech-stack-and-prerequisites)
2. [API Endpoints](#2-api-endpoints)
3. [Environment Configuration](#3-environment-configuration)
4. [Deployment](#4-deployment)

## 1. Tech Stack and Prerequisites

**Backend:** Python, Flask\
**Database:** MongoDB Atlas\
**Deployment:** Render\
**Prerequisites:** Git, MongoDB Atlas account, Python 3.11

## 2. API Endpoints

**1. Store GitHub Events:**
```
POST <RenderWebServiceURL>/webhook/receiver
```
- Receives GitHub webhook payloads
- Extracts relevant metadata
- Inserts records into MongoDB

## 3. Environment Configuration

Sensitive credentials are stored as environment variables:
```
MONGODB_URI=your_mongodb_atlas_connection_string
```
These are configured directly in Render’s environment settings.

##  4. Deployment

- The application is deployed on Render
- Automatic redeploys occur on push to the main branch
- MongoDB Atlas is used as a managed cloud database

