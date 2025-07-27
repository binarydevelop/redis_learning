# Redis Cache Implementation Flow Diagram

## 🚀 Application Startup Flow

```mermaid
graph TD
    A[Application Start] --> B[Load Environment Variables]
    B --> C[Initialize Redis Singleton]
    C --> D{Redis Connection Type}
    
    D -->|Sync| E[Create redis.Redis Client]
    D -->|Async| F[Create aioredis Client]
    
    E --> G[Test Connection with ping()]
    F --> H[Test Connection with await ping()]
    
    G --> I{Connection Success?}
    H --> I
    
    I -->|Yes| J[✅ Redis Connected]
    I -->|No| K[❌ Connection Failed]
    
    J --> L[Setup Mock Data]
    K --> M[Exit Application]
```

## 📊 Mock Data Setup Flow

```mermaid
graph TD
    A[Setup Mock Data] --> B{Setup Method}
    
    B -->|Sync| C[set_redis_with_mock_data]
    B -->|Threaded| D[set_redis_with_mock_data_async]
    B -->|Async| E[set_redis_with_mock_data_async_aioredis]
    
    C --> F[Generate 1000 User Records]
    D --> F
    E --> F
    
    F --> G[Process in Batches]
    G --> H[Set Key-Value Pairs in Redis]
    
    H --> I{Progress Feedback}
    I -->|Sync| J[Blocking Progress]
    I -->|Threaded| K[Background Progress]
    I -->|Async| L[Async Progress with Pipeline]
    
    J --> M[✅ Setup Complete]
    K --> M
    L --> M
```

## 🎮 User Interaction Flow

```mermaid
graph TD
    A[User Input] --> B[Enter User ID]
    B --> C{Input Validation}
    
    C -->|Valid| D[Query Redis Cache]
    C -->|'q'| E[Exit Application]
    C -->|Invalid| F[Error Message]
    
    D --> G{Cache Hit?}
    
    G -->|Yes| H[Return Cached Data]
    G -->|No| I[Cache Miss - Simulate DB Fetch]
    
    H --> J[Display: "Found in cache: user-X = value"]
    I --> K[Wait 2 seconds]
    K --> L[Generate New User Data]
    L --> M[Store in Redis Cache]
    M --> N[Display: "Stored: user-X = value"]
    
    J --> O[Continue Loop]
    N --> O
    F --> O
    O --> A
```

## 🔄 Cache-Aside Pattern Flow

```mermaid
graph TD
    A[Request User Data] --> B[Check Redis Cache]
    B --> C{Data in Cache?}
    
    C -->|Yes| D[Return Cached Data]
    C -->|No| E[Cache Miss]
    
    E --> F[Simulate Database Query]
    F --> G[Generate User Data]
    G --> H[Store in Redis Cache]
    H --> I[Return Data to User]
    
    D --> J[Fast Response]
    I --> J
```

## ⚡ Async vs Sync Performance Comparison

```mermaid
graph LR
    subgraph "Sync Implementation"
        A1[Blocking Redis Operations] --> A2[Sequential Processing]
        A2 --> A3[Thread-based Background Tasks]
        A3 --> A4[Blocking User Input]
    end
    
    subgraph "Async Implementation"
        B1[Non-blocking Redis Operations] --> B2[Concurrent Processing]
        B2 --> B3[Event Loop Based]
        B3 --> B4[Non-blocking User Input]
    end
    
    A4 --> C[Performance: Good]
    B4 --> D[Performance: Excellent]
```

## 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph "Application Layer"
        A[main.py / main_async.py]
        B[User Interface]
    end
    
    subgraph "Business Logic Layer"
        C[simulator/simulate_cache_db_flow.py]
        D[Cache-Aside Pattern]
        E[Data Generation]
    end
    
    subgraph "Configuration Layer"
        F[config/redis.py]
        G[Redis Singleton]
        H[Connection Management]
    end
    
    subgraph "Infrastructure Layer"
        I[Redis Server]
        J[Environment Variables]
    end
    
    A --> C
    B --> C
    C --> F
    F --> I
    F --> J
```

## 📈 Data Flow Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant A as Application
    participant C as Cache Layer
    participant D as Database (Simulated)
    
    U->>A: Start Application
    A->>C: Initialize Redis Connection
    C->>A: Connection Established
    A->>C: Setup Mock Data (1000 records)
    C->>A: Setup Complete
    
    loop User Interaction
        U->>A: Enter User ID
        A->>C: Check Cache
        alt Cache Hit
            C->>A: Return Cached Data
            A->>U: Display Result
        else Cache Miss
            A->>D: Simulate DB Query (2s delay)
            D->>A: Return New Data
            A->>C: Store in Cache
            A->>U: Display Result
        end
    end
```

## 🔧 Key Components

### **Sync Implementation:**
- `main.py` - Synchronous main application
- `redis.Redis` - Blocking Redis client
- Threading for background tasks
- Sequential data processing

### **Async Implementation:**
- `main_async.py` - Asynchronous main application
- `aioredis` - Non-blocking Redis client
- `asyncio` for concurrency
- Pipeline operations for batch processing

### **Shared Components:**
- `config/redis.py` - Redis connection management
- `simulator/simulate_cache_db_flow.py` - Business logic
- Environment-based configuration
- Singleton pattern for Redis client

## 🎯 Performance Characteristics

| Operation | Sync Version | Async Version |
|-----------|-------------|---------------|
| **Initial Setup** | Blocking (5-10s) | Non-blocking (2-3s) |
| **Cache Hit** | ~1ms | ~1ms |
| **Cache Miss** | ~2s (blocking) | ~2s (non-blocking) |
| **Batch Operations** | Sequential | Pipeline |
| **User Input** | Blocking | Non-blocking |
| **Memory Usage** | Higher (threads) | Lower (event loop) |