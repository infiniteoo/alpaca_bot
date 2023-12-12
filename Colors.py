class Colors:
    @staticmethod
    def red(text):
        return f"\033[91m{text}\033[0m"  # Red color

    @staticmethod
    def green(text):
        return f"\033[92m{text}\033[0m"  # Green color

    @staticmethod
    def yellow(text):
        return f"\033[93m{text}\033[0m"  # Yellow color

    @staticmethod
    def blue(text):
        return f"\033[94m{text}\033[0m"  # Blue color

    @staticmethod
    def magenta(text):
        return f"\033[95m{text}\033[0m"  # Magenta color

    @staticmethod
    def cyan(text):
        return f"\033[96m{text}\033[0m"  # Cyan color

    @staticmethod
    def white(text):
        return f"\033[97m{text}\033[0m"  # White color

    @staticmethod
    def reset(text):
        return f"\033[0m{text}\033[0m"  # Reset color

# Example usage:
error_message = "An error occurred"
print(Colors.red(error_message))
