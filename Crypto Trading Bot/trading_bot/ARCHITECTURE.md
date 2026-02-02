# Architecture Documentation

## Overview

The trading bot follows a layered architecture with clear separation of concerns, making it maintainable, testable, and extensible.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer (cli.py)                   │
│  - Argument parsing                                      │
│  - User interaction                                      │
│  - Credential management                                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Business Logic Layer                        │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │   OrderManager (orders.py)                      │    │
│  │   - Order placement orchestration               │    │
│  │   - Output formatting                           │    │
│  │   - Order status management                     │    │
│  └────────────────────┬───────────────────────────┘    │
│                       │                                  │
│  ┌────────────────────┴───────────────────────────┐    │
│  │   OrderValidator (validators.py)                │    │
│  │   - Input validation                            │    │
│  │   - Parameter sanitization                      │    │
│  │   - Business rule enforcement                   │    │
│  └─────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│            API Client Layer (client.py)                  │
│  - HTTP communication                                    │
│  - Authentication (HMAC-SHA256)                         │
│  - Request signing                                       │
│  - Response parsing                                      │
│  - Error handling                                        │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│           External Service (Binance API)                 │
│           https://testnet.binancefuture.com              │
└─────────────────────────────────────────────────────────┘

         Cross-cutting Concerns:
         ┌────────────────────────┐
         │  Logging (logging_config.py)
         │  - File logging
         │  - Console logging
         │  - Log rotation
         └────────────────────────┘
```

## Layer Descriptions

### 1. CLI Layer (`cli.py`)

**Responsibilities**:
- Parse command-line arguments
- Load environment configuration
- Handle user input/output
- Coordinate application flow
- Handle top-level exceptions

**Key Functions**:
- `create_parser()`: Configure argparse with all options
- `load_credentials()`: Load API keys from environment
- `validate_args()`: Pre-validate CLI arguments
- `test_connection()`: Test API connectivity
- `main()`: Application entry point

**Design Patterns**:
- Command Pattern: Each CLI command maps to a specific action
- Facade Pattern: Simplifies interaction with underlying layers

### 2. Business Logic Layer

#### OrderManager (`bot/orders.py`)

**Responsibilities**:
- Orchestrate order placement workflow
- Format output for users
- Manage order lifecycle
- Track order status

**Key Methods**:
- `place_order()`: Main order placement workflow
- `_print_order_summary()`: Display order details
- `_print_order_response()`: Display API response
- `get_order_status()`: Query order status
- `cancel_order()`: Cancel pending orders

**Design Patterns**:
- Facade Pattern: Simplifies order operations
- Template Method: Common order flow with variants

#### OrderValidator (`bot/validators.py`)

**Responsibilities**:
- Validate all input parameters
- Sanitize and normalize inputs
- Enforce business rules
- Provide clear error messages

**Key Methods**:
- `validate_symbol()`: Symbol format validation
- `validate_side()`: BUY/SELL validation
- `validate_order_type()`: MARKET/LIMIT validation
- `validate_quantity()`: Quantity validation
- `validate_price()`: Price validation
- `validate_order_params()`: Combined validation

**Design Patterns**:
- Strategy Pattern: Different validation strategies per parameter
- Chain of Responsibility: Sequential validation steps

### 3. API Client Layer (`bot/client.py`)

**Responsibilities**:
- HTTP communication with Binance API
- Request authentication and signing
- Response parsing
- Network error handling
- API error translation

**Key Methods**:
- `__init__()`: Initialize with credentials
- `_generate_signature()`: HMAC-SHA256 signing
- `_request()`: Generic HTTP request handler
- `test_connectivity()`: Test API connection
- `place_order()`: Place order via API
- `get_order()`: Query order status
- `cancel_order()`: Cancel order

**Design Patterns**:
- Adapter Pattern: Adapts Binance API to application interface
- Singleton Pattern: Single client instance per session

### 4. Logging Configuration (`bot/logging_config.py`)

**Responsibilities**:
- Configure Python logging
- Create log files with timestamps
- Set appropriate log levels
- Format log messages

**Key Functions**:
- `setup_logging()`: Initialize logging system
- `get_logger()`: Get logger instance

**Design Patterns**:
- Singleton Pattern: Single logging configuration
- Factory Pattern: Logger creation

## Data Flow

### Successful Order Placement Flow

```
1. User Input
   ↓
2. CLI Parsing (cli.py)
   - Parse arguments
   - Load credentials
   ↓
3. Validation (validators.py)
   - Validate symbol
   - Validate side
   - Validate type
   - Validate quantity
   - Validate price
   ↓
4. Order Manager (orders.py)
   - Print order summary
   - Prepare order request
   ↓
5. API Client (client.py)
   - Add timestamp
   - Generate signature
   - Make HTTP request
   ↓
6. Binance API
   - Process order
   - Return response
   ↓
7. Response Processing
   - Parse response
   - Print formatted output
   - Log results
   ↓
8. User Output
   - Order confirmation
   - Order details
   - Success message
```

### Error Handling Flow

```
Error Detection
   ↓
Exception Raised
   ↓
Caught at Appropriate Layer
   ↓
Logged with Details
   ↓
User-Friendly Error Message
   ↓
Appropriate Exit Code
```

## Key Design Decisions

### 1. Direct REST API vs Library

**Decision**: Use direct REST API calls with `requests`

**Rationale**:
- More control over requests
- Better for learning API mechanics
- Fewer dependencies
- Easier debugging
- Assignment allows either approach

**Trade-offs**:
- More code to write
- Manual signature generation
- No built-in WebSocket support

### 2. Environment Variables for Credentials

**Decision**: Use environment variables for API credentials

**Rationale**:
- Security best practice
- No credentials in code
- Easy CI/CD integration
- Follows 12-factor app principles

**Implementation**:
```python
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
```

### 3. Modular Structure

**Decision**: Separate concerns into distinct modules

**Rationale**:
- Single Responsibility Principle
- Easier testing
- Better maintainability
- Clear code organization
- Facilitates team collaboration

**Structure**:
```
bot/
  client.py      # API communication only
  orders.py      # Business logic only
  validators.py  # Validation only
  logging_config.py  # Logging only
```

### 4. Comprehensive Logging

**Decision**: Log all operations to file with DEBUG level

**Rationale**:
- Assignment requirement
- Debugging assistance
- Audit trail
- Performance monitoring
- Issue reproduction

**Implementation**:
- File: DEBUG level (everything)
- Console: WARNING level (errors only)
- Separate log file per session

### 5. Type Hints Throughout

**Decision**: Use type hints for all functions

**Rationale**:
- Better IDE support
- Self-documenting code
- Catch type errors early
- Improve code quality

**Example**:
```python
def validate_symbol(symbol: str) -> str:
    """Validate trading symbol"""
```

## Error Handling Strategy

### Error Categories

1. **Validation Errors**
   - Caught at validation layer
   - Clear user messages
   - Exit code: 1

2. **Configuration Errors**
   - Missing credentials
   - Invalid configuration
   - Exit code: 1

3. **API Errors**
   - Authentication failures
   - Insufficient balance
   - Rate limits
   - Exit code: 1

4. **Network Errors**
   - Connection timeouts
   - DNS failures
   - Exit code: 1

5. **Unexpected Errors**
   - Caught at top level
   - Full stack trace logged
   - Exit code: 1

### Error Handling Pattern

```python
try:
    # Operation
    result = perform_operation()
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    print(f"User message: {e}")
    sys.exit(1)
except Exception as e:
    logger.exception("Unexpected error")
    print(f"Unexpected error: {e}")
    sys.exit(1)
```

## Security Considerations

### 1. Credential Management
- Never log API secrets
- Use environment variables
- No credentials in code
- No credentials in git

### 2. API Communication
- HTTPS only
- Request signing (HMAC-SHA256)
- Timestamp validation
- Signature verification

### 3. Input Validation
- All inputs validated
- SQL injection prevention (N/A)
- Command injection prevention
- Parameter sanitization

### 4. Error Messages
- No sensitive data in errors
- Generic error messages to users
- Detailed logging for debugging

## Scalability Considerations

### Current Design
- Single-threaded
- Synchronous operations
- One order at a time

### Future Enhancements
- Async/await for concurrent orders
- WebSocket for real-time data
- Order queue management
- Rate limiting implementation

## Testing Strategy

### Unit Testing (Future)
```python
# Example structure
tests/
  test_validators.py
  test_client.py
  test_orders.py
```

### Integration Testing
- Test with Binance testnet
- Verify order placement
- Check log output
- Validate error handling

### Manual Testing
- See TESTING.md for comprehensive guide

## Performance Metrics

### Expected Performance
- Order placement: < 5 seconds
- API response time: < 2 seconds
- Memory usage: < 50 MB
- Log file size: < 50 KB per order

### Bottlenecks
- Network latency (primary)
- API rate limits (100/minute)
- Disk I/O for logging (minimal)

## Extensibility Points

### Adding New Order Types
1. Update `validators.py` with new type
2. Add handling in `client.py`
3. Update CLI options
4. Add tests

### Adding New Features
1. Create new module in `bot/`
2. Import in `__init__.py`
3. Use in `cli.py`
4. Update documentation

### Supporting Other Exchanges
1. Create new client class
2. Implement exchange-specific API
3. Maintain same interface
4. Use polymorphism

## Dependencies

### Core Dependencies
- `requests`: HTTP client (minimal, stable)

### Standard Library
- `argparse`: CLI parsing
- `logging`: Logging system
- `hmac`: Signature generation
- `hashlib`: SHA256 hashing
- `time`: Timestamps
- `os`: Environment variables

### Dependency Management
- Minimal dependencies principle
- Only production-ready libraries
- Regular security updates
- Version pinning in requirements.txt

## Monitoring and Observability

### Logging Levels
- **DEBUG**: All operations, API calls, validations
- **INFO**: Major operations, order placements
- **WARNING**: Potential issues, ignored errors
- **ERROR**: Failed operations, API errors

### Metrics to Monitor
- Order success rate
- API response times
- Error frequencies
- Order volumes

## Compliance

### Assignment Requirements
✅ Python 3.x  
✅ Market and Limit orders  
✅ BUY and SELL sides  
✅ CLI with validation  
✅ Clear output  
✅ Structured code  
✅ Logging  
✅ Exception handling  
✅ README with instructions  
✅ requirements.txt  

### Best Practices
✅ Type hints  
✅ Docstrings  
✅ Error handling  
✅ Input validation  
✅ Security considerations  
✅ Code organization  
✅ Documentation  

---

**Architecture Version**: 1.0  
**Last Updated**: January 30, 2024  
**Author**: Trading Bot Team
