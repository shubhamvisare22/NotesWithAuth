# NotesWithAuth

API Documentation Link : https://documenter.getpostman.com/view/28016390/2s9YC7SWnA

**NoteApp Project Overview:**

- Successfully implemented required functionality:
  1. Created user registration with token assignment for CRUD operations on user's notes.
  2. Developed necessary API endpoints:
     - Register user: http://127.0.0.1:8000/api/v1/register
     - Create note: http://127.0.0.1:8000/api/v1/create-note
     - List notes: http://127.0.0.1:8000/api/v1/list-note
     - Retrieve note: http://127.0.0.1:8000/api/v1/retrieve-note/{{id}}
     - Update note: http://127.0.0.1:8000/api/v1/update-note/{{id}}
     - Delete note: http://127.0.0.1:8000/api/v1/delete-note/{{id}}
     - Patch note: http://127.0.0.1:8000/api/v1/patch-note/{{id}}
     - Sort notes: http://127.0.0.1:8000/api/v1/list-note?sort={{created_at/updated_at}}

- Note Properties:
  - id (int)
  - title (string)
  - content (string)
  - created_at (string: timestamp)
  - updated_at (string: timestamp)

- Additional Information:
  - Token-based authentication for user access, obtained during registration.
  - Technologies used: Python, Django, Django REST Framework, Default DB (SQLite3).

- Project Flow:
  1. User registers with a username and password to receive a token.
  2. Token must be included in headers with Authorization key for CRUD operations.
  3. Endpoint documentation available on here (https://documenter.getpostman.com/view/28016390/2s9YC7SWnA) for easy project setup.

**Note:** AWS services like Lambda and DynamoDB were not used due to lack of expertise; however, all project requirements were fulfilled.
