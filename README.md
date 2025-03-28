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
##Technologies Used
  - Flask framework was used for developing the application.
  - Jinja2 was used for templating and HTML generation. 
  - Bootstrap 5 was used for styling and designing purpose. 
  - Flask-SQLAlchemy and sqlite3 were used for database operations.
  - Matplotlib is used for generating the the admin_summary and user_summary.
   
