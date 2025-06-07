# VivaTerra Cameroun CRM

This repository contains a minimal customer relationship management (CRM) application built with Flask.

## Features

- Manage client records (add, list, delete)
- Uses SQLite for data storage
- Simple REST style API

## Quick start

```bash
pip install -r requirements.txt
python -m crm.app  # starts the development server
```

Running tests:

```bash
pytest
```

The application will create `crm.db` automatically on first run.

