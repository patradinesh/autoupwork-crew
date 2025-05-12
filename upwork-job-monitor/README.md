# Upwork Job Monitor

This project is designed to monitor Upwork for new DevOps-related job postings and send notifications to users when such jobs are available.

## Project Structure

```
upwork-job-monitor
├── src
│   ├── main.py          # Entry point of the application
│   ├── login.py         # Handles user authentication with Upwork
│   ├── job_monitor.py    # Monitors for new job postings
│   ├── notification.py   # Sends notifications for new jobs
│   └── utils
│       ├── __init__.py  # Initializes the utils package
│       └── config.py    # Manages configuration settings
├── config
│   └── settings.json    # Configuration settings for the application
├── requirements.txt      # Lists project dependencies
├── .env.example          # Example of environment variables
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/upwork-job-monitor.git
   cd upwork-job-monitor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your settings:
   - Copy the `.env.example` to `.env` and fill in your Upwork API credentials and other necessary environment variables.
   - Edit `config/settings.json` to set your notification preferences and other configurations.

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. The application will log in to your Upwork profile and start monitoring for new DevOps-related job postings. Notifications will be sent based on your configured preferences.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.