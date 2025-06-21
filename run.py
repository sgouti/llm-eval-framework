import subprocess
import os
import sys

def main():
    try:
        # Add the project root directory to PYTHONPATH
        project_root = os.path.dirname(os.path.abspath(__file__))
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

        subprocess.run(["streamlit", "run", "src/main.py"], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()