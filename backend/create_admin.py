import typer
from sqlalchemy.orm import Session

from app.crud.crud_user import crud_user
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserType

app = typer.Typer()


def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    display_name: str = None,
):
    db = SessionLocal()
    try:
        user_in = UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            user_type=UserType.ADMIN,
            is_superuser=True,
        )
        user = crud_user.create(db, obj_in=user_in)
        typer.echo(f"Successfully created admin user: {user.email}")
    except ValueError as e:
        typer.echo(f"Error: {str(e)}")
    finally:
        db.close()


@app.command()
def create_admin(
    email: str = typer.Option(..., help="Admin user's email"),
    password: str = typer.Option(..., help="Admin user's password"),
    first_name: str = typer.Option(..., help="Admin user's first name"),
    last_name: str = typer.Option(..., help="Admin user's last name"),
    display_name: str = typer.Option(None, help="Admin user's display name (optional)"),
):
    """Create a new admin user."""
    create_admin_user(email, password, first_name, last_name, display_name)


if __name__ == "__main__":
    app()
