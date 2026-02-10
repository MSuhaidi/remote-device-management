# syntax=docker/dockerfile:1.4
FROM oven/bun

ARG VITE_BACKEND_URL
ARG VITE_API_TOKEN
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ENV VITE_API_TOKEN=$VITE_API_TOKEN

WORKDIR /app

# Copy package.json and bun.lockb to leverage Docker cache
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Build the SvelteKit application
RUN bun run build

# Expose the default port for vite preview
EXPOSE 4173

# Command to run the production preview server
# --host 0.0.0.0 makes it accessible from outside the container
CMD ["bun", "run", "preview", "--host", "0.0.0.0", "--port", "4173"]
