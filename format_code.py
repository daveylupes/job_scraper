import subprocess


def format_code():
    try:
        subprocess.run(["black", "."], check=True)
        print("Code formatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while formatting the code: {e}")


if __name__ == "__main__":
    format_code()
