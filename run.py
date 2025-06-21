import subprocess

def main():
    try:
        subprocess.run(["streamlit", "run", "src/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()