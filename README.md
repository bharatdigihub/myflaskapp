# Flask PostgreSQL App

A simple Flask application that connects to a PostgreSQL database hosted on Render.com.

## Deployment on Render.com

1. Fork or clone this repository
2. Create a new Web Service on Render.com
   - Connect your GitHub repository
   - Select Python environment
   - The build command and start command are already configured in `render.yaml`

3. Set up PostgreSQL
   - Create a new PostgreSQL database on Render.com
   - The environment variables will be automatically configured via `render.yaml`

4. Deploy
   - Render will automatically deploy your app
   - Any push to the main branch will trigger a new deployment

## Environment Variables

The following environment variables are required:

- `DB_HOST` - PostgreSQL host
- `DB_PORT` - PostgreSQL port (default: 5432)
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name

## Local Development

1. Create a `.env` file with your database credentials
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Docker Development

```bash
docker compose up --build
```

The app will be available at `http://localhost:5000`