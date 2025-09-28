# API Setup Guide

## Quick Start

1. **Start the Local Server:**

   ```bash
   cd pyserver
   myenv\Scripts\activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Or use the start script:**

   ```bash
   cd pyserver
   python start_server.py
   ```

3. **Test the API:**
   - Open http://localhost:8000/docs in your browser
   - This will show the FastAPI interactive documentation

## API Endpoints

### User Management

- `GET /users` - Get all users
- `POST /users` - Create regular user
- `POST /users/google` - Create/get Google user
- `GET /users/check/{email}` - Check if user exists

### Resume Management

- `GET /resumes` - Get all resumes
- `POST /resumes` - Create resume
- `GET /resumes/{resume_id}` - Get resume by ID
- `GET /resumes/user/{user_id}` - Get user's resumes
- `PUT /resumes/{resume_id}` - Update resume
- `DELETE /resumes/{resume_id}` - Delete resume

### Job Management

- `GET /jobs` - Get all jobs
- `POST /jobs` - Create job
- `GET /jobs/{job_id}` - Get job by ID

### Applications

- `GET /applications` - Get all applications
- `POST /applications` - Create application

## Database Setup

The server will automatically create tables when it starts. Make sure your `.env` file has the correct `DATABASE_URL`.

## Switching Between Local and Production

In `client/src/config/api.js`, change the `BASE_URL`:

- Local: `http://localhost:8000`
- Production: `https://your-hr-rosy.vercel.app`

## Troubleshooting

1. **Port 8000 already in use:**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

   Then update `client/src/config/api.js` to use port 8001.

2. **Database connection issues:**

   - Check your `.env` file
   - Make sure PostgreSQL is running
   - Verify DATABASE_URL format

3. **CORS issues:**
   - The server is configured to allow CORS from `http://localhost:5173`
   - Make sure your React app is running on the correct port
