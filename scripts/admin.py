import json
import subprocess

users = json.loads(subprocess.check_output(["airflow", "users", "list", "--output", "json"], text=True))
if not any(user["username"] == "estudiante" for user in users):
    subprocess.run(["airflow", "users", "create", "--username", "estudiante", "--password", "examen-local",
                    "--firstname", "Estudiante", "--lastname", "Local", "--role", "Admin", "--email", "estudiante@example.invalid"], check=True)
