-- Migration 001: Initial schema
-- Creates the marketing_data table with all spend channels and revenue

CREATE TABLE IF NOT EXISTS marketing_data (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tv_spend    REAL NOT NULL,
    digital_spend REAL NOT NULL,
    radio_spend REAL NOT NULL,
    print_spend REAL NOT NULL,
    revenue     REAL NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);