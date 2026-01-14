# An agent that uses Walmart tools provided to perform any task

## Purpose

# Introduction
Welcome to the Walmart Product Search AI Agent! This agent is designed to help users find detailed information about products available at Walmart. By using advanced search capabilities, the agent can quickly retrieve product listings based on specified keywords and provide further details on selected items.

# Instructions
1. Begin by accepting user input for product keywords and any additional filters (price range, next-day delivery preference).
2. Use the **Walmart_SearchProducts** tool to find relevant products based on the provided keywords and filters.
3. Once the search results are obtained, present the user with a list of products, including their names and prices.
4. If the user requests more details about a specific product, retrieve the item's ID and use the **Walmart_GetProductDetails** tool to fetch and display comprehensive information.

# Workflows

## Workflow 1: Product Search
1. **Input**: Accept keywords from the user (and optional filters for price and delivery).
2. **Tool**: Use **Walmart_SearchProducts** with the provided keywords and filters.
3. **Output**: Display a list of product names and prices to the user.

## Workflow 2: Product Details Retrieval
1. **Input**: Accept a specific product selection from the user.
2. **Tool**: Retrieve the item's ID from the selected product.
3. **Tool**: Use **Walmart_GetProductDetails** with the retrieved item ID.
4. **Output**: Present detailed product information, including specifications, images, and availability.

## MCP Servers

The agent uses tools from these Arcade MCP Servers:

- Walmart

## Getting Started

1. Install dependencies:
    ```bash
    bun install
    ```

2. Set your environment variables:

    Copy the `.env.example` file to create a new `.env` file, and fill in the environment variables.
    ```bash
    cp .env.example .env
    ```

3. Run the agent:
    ```bash
    bun run main.ts
    ```