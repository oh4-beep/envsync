import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def init():
    from .config import init_config
    from .vault import FirestoreVault
    from .config import config_exists

    if config_exists():
        typer.echo("⚠️  Config already exists. Overwrite?")
        confirm = typer.confirm("Continue?")
        if not confirm:
            raise typer.Exit()

    project_name = typer.prompt("Project name")
    service_account_path = typer.prompt("Service account path")

    try:
        vault = FirestoreVault(service_account_path)
        doc = vault.db.collection("envsync").document(project_name).get()
        if doc.exists:
            typer.echo(f"⚠️  Project '{project_name}' already exists in Firestore.")
            confirm = typer.confirm("Use it anyway?")
            if not confirm:
                raise typer.Exit()
    except Exception as e:
        typer.echo(f"❌ Could not connect to Firebase: {e}", err=True)
        raise typer.Exit(1)

    init_config(project_name, service_account_path)
    typer.echo(f"✅ Config saved! Run 'envsync keygen' to generate your secret key.")


@app.command()
def keygen():
    from .crypto import generate_key

    key = generate_key()
    typer.echo(f"🔑 Your secret key: {key}")
    typer.echo("⚠️  Store this key securely! You will need it to encrypt/decrypt your .env file.")

@app.command()
def push(key: str = typer.Option(..., "--key", help="Your Fernet secret key")):
    from .config import load_config
    from .vault import FirestoreVault
    from .crypto import encrypt_file
    config = load_config()
    vault = FirestoreVault(config["service_account_path"])
    try:
        encrypted_data = encrypt_file(".env", key)
    except Exception as e:
        typer.echo(f"❌ Error encrypting .env file: {e}", err=True)
        raise typer.Exit(1)
    vault.push(config["project_id"], encrypted_data)
    typer.echo("✅ .env file encrypted and pushed to Firestore!")

@app.command()
def pull(key: str = typer.Option(..., "--key", help="Your Fernet secret key")):
    from .config import load_config
    from .vault import FirestoreVault
    from .crypto import decrypt_data
    config = load_config()
    vault = FirestoreVault(config["service_account_path"])
    try:
        encrypted_data = vault.pull(config["project_id"])
    except Exception as e:
        typer.echo(f"❌ Error pulling .env file: {e}", err=True)
        raise typer.Exit(1)
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
    except Exception as e:
        typer.echo(f"❌ Wrong key — could not decrypt.", err=True)
        raise typer.Exit(1)
    if Path(".env").exists():
        confirm = typer.confirm(".env already exists. Overwrite?")
        if not confirm:
            raise typer.Exit()
    with open(".env", "w") as f:
        f.write(decrypted_data)
    typer.echo("✅ .env file pulled and decrypted!")

@app.command()
def status():
    # envsync status, shows config and whether a remote env exists
    from .config import load_config
    from .vault import FirestoreVault
    config = load_config()
    vault = FirestoreVault(config["service_account_path"])
    try:    
        vault.pull(config["project_id"])
        typer.echo("✅ Remote .env exists in Firestore.")
    except Exception as e:
        typer.echo("⚠️  No remote .env found in Firestore.")
    typer.echo(f"Project ID: {config['project_id']}")
    typer.echo(f"Service Account Path: {config['service_account_path']}")

if __name__ == "__main__":
    app()