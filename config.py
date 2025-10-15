# config.py - Centralized configuration for the StudySage project

# Model configuration
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

# Text limits for different modes
ONLINE_MODE_MAX_CHARS = 4000
ONLINE_MODE_MAX_WORDS = 800
OFFLINE_MODE_MAX_CHARS = 100000
OFFLINE_MODE_MAX_WORDS = 20000

# Output directory
OUTPUT_DIR = "output"