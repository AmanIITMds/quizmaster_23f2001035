# Quiz Master App - V1 (MAD 1 PROJECT)
#Description:
It is a multi-user app (one requires an administrator and other users) that acts as an exam preparation site for multiple courses. it comprise of :**Admin** and **User**. built using Html,CSS, Jinja2 templates , Flask and Sqlite. This application provides a platform for attempting quiz and tracking the progress.
### Admin Login
- **Admin Authentication**: A login/register form with fields email and password.
- **Admin Dashboard**:
  - Create, edit, and delete subjects.
  - Create, edit, and delete chapters under subjects.
  - Create quizzes under chapters, specifying date and duration.
  - Manage questions in quizzes (MCQs with one correct option).
  - Search chapters, subjects, and quizzes.
  - View summary charts.
### User Login
- **User Authentication**: A login/register form with fields email and password.
- **User Dashboard**:
  - Attempt quizzes of interest.
  - Record quiz scores.
  - Display score of quiz attempts.
  - View summary charts.
## Features Breakdown

### Admin Features
1. **Subject Management**:
   - Add, edit, delete subjects.
2. **Chapter Management**:
   - Add, edit, delete chapters within subjects.
3. **Quiz Management**:
   - Add, edit, delete quizzes.
   - Add, delete MCQ questions within quizzes.
4. **Search Functionality**:
   - Search chapters, subjects, or quizzes for efficient management.
5. **Analytics**:
   - Summary charts for data insights.
### User Features
1. **Quiz Interaction**:
   - Attempt any quiz available in the system.
2. **Score Tracking**:
   - Record scores for every quiz attempt.
3. **Analytics**:
   - Summary charts for performance tracking.
## Technologies Used
  - Flask framework - for development of the application.
  - Jinja2- for dynamic templating and HTML generation. 
  - Bootstrap- for styling and designing purpose. 
  - Flask-SQLAlchemy and sqlite3- for database operations.
  - Matplotlib - for generating the the admin_summary and user_summary.

## DB schema:
![db_schema](https://github.com/user-attachments/assets/67833c04-21f2-4f9b-b4a8-6cb364cbaa5f)   

## WIREFRAME :
![Home](https://github.com/user-attachments/assets/f5d8c6ab-e8b5-4f11-8d2f-f4596008ddfa)

![Adminlogin](https://github.com/user-attachments/assets/9c721a83-84b0-4036-a769-758e5f0d24e5)

![Userlogin](https://github.com/user-attachments/assets/1effa3f9-197f-4fbb-9b90-ef0be9c3c563)

![Register](https://github.com/user-attachments/assets/6fedaa20-f0fa-4d66-ac5b-9b9e0a3094e3)

![Admin_dashboard](https://github.com/user-attachments/assets/10c40993-092e-4caf-82fa-5011f75d0eaf)

![Admin_summary](https://github.com/user-attachments/assets/8c624463-aea8-4436-b0a9-fee3011002ce)

![quizmanagement](https://github.com/user-attachments/assets/216e5cf0-2958-4d71-8607-44d44c7543ad)

![scores](https://github.com/user-attachments/assets/5870281d-73be-4271-9fdd-524088a0d60d)

![user_summary](https://github.com/user-attachments/assets/cf9f81f2-dacb-4c19-b872-c1757535c92d)

![userdashboard](https://github.com/user-attachments/assets/9b48ff71-1bfa-4b23-b23b-e5b158b26e87)
