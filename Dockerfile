# Multi-stage build for goldcheck.

# syntax=docker/dockerfile:1

# Build stage
FROM rust:1.85 AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/goldcheck /usr/local/bin/goldcheck
ENTRYPOINT ["goldcheck"]
