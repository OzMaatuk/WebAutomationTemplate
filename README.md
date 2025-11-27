# Web Automation Template with Playwright

## Overview
A production-ready web automation framework template using Python and Playwright. This template provides a solid foundation for building web automation applications with best practices, proper error handling, and comprehensive testing support.

### Design Patterns
- **Page Object Model (POM)**: Encapsulates page-specific logic
- **Facade Pattern**: Simplifies complex interactions
- **MVC Pattern**: Separates concerns for maintainability
- **Singleton Pattern**: Efficient configuration management

## Features
- ✅ Type-safe with comprehensive type hints
- ✅ Robust error handling with custom exceptions
- ✅ Automatic screenshot capture on failures
- ✅ Retry logic for flaky operations
- ✅ Context manager support for resource cleanup
- ✅ Environment variable configuration
- ✅ Rotating log files
- ✅ Comprehensive test fixtures
- ✅ Docker support

## Directory Structure
```
├── controller/          # Workflow orchestration
│   ├── controller.py   # Main controller
│   └── facade.py       # High-level operations facade
├── pages/              # Page Object Model
│   ├── base_page.py   # Base class with common functionality
│   ├── login_page.py  # Login page object
│   ├── feed_page.py   # Feed/listing page object
│   └── item_page.py   # Individual item page object
├── tests/              # Test suite
│   ├── conftest.py    # Pytest fixtures
│   └── test_*.py      # Test modules
├── utils/              # Utilities
│   ├── exceptions.py  # Custom exceptions
│   └── retry.py       # Retry decorators
├── constants/          # Configuration constants
│   └── settings.py    # Settings singleton
├── main.py            # Application entry point
├── driver.py          # Playwright driver setup
├── logger.py          # Logging configuration
├── config.ini         # Application configuration
└── .env.example       # Environment variables template
```

## Installation

### Prerequisites
- Python 3.12 or higher
- pip

### Setup
1. Clone the repository and navigate to the project directory

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```sh
   playwright install chromium
   ```

4. Configure environment variables:
   ```sh
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. Update `config.ini` with your site-specific settings

## Configuration

### Environment Variables (.env)
```env
BASE_URL=https://your-site.com
APP_USERNAME=your_username
APP_PASSWORD=your_password
LOG_LEVEL=INFO
```

### Config File (config.ini)
```ini
[Settings]
base_url = https://example-site.com
browser_type = chromium
headless = True
timeout = 30000
log_level = INFO
screenshot_dir = screenshots
report_dir = reports
```

## Usage

### Running the Application
```sh
python main.py
```

### Running Tests
```sh
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_login.py

# Run with verbose output
pytest -v
```

### Docker
```sh
# Build image
docker build -t web-automation .

# Run container
docker run --env-file .env web-automation
```

## Customization

### Adding New Page Objects
1. Create a new file in `pages/` directory
2. Inherit from `BasePage`
3. Implement page-specific methods

Example:
```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    
    def my_action(self):
        self.safe_click("button#submit")
```

### Updating Selectors
Update constants in `constants/` directory:
- `login_constants.py` - Login page selectors
- `feed_constants.py` - Feed page selectors
- `item_constants.py` - Item page selectors

### Custom Workflow
Modify `controller/controller.py` to implement your specific automation workflow.

## Best Practices
- Use environment variables for sensitive data
- Implement explicit waits instead of sleep()
- Take screenshots on failures for debugging
- Use type hints for better IDE support
- Write tests for critical functionality
- Keep page objects focused and single-purpose

## Troubleshooting

### Common Issues
1. **Element not found**: Update selectors in constants files
2. **Timeout errors**: Increase timeout in config.ini
3. **Login failures**: Verify credentials in .env file
4. **Browser not found**: Run `playwright install chromium`

### Debug Mode
Set `headless = False` in config.ini to see browser actions.

## Contributing
This is a template project. Fork and customize for your specific needs.

## License
MIT License - Feel free to use for any purpose.