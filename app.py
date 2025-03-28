from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'secret_key_here'
db = SQLAlchemy(app)
migrate= Migrate (app,db)

#----------------------------models-----------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.String(20))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapters = db.relationship('Chapter', back_populates='subject', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', back_populates='chapter')
    subject = db.relationship('Subject', back_populates='chapters')
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    chapter = db.relationship('Chapter', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', lazy=True)  

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    quiz = db.relationship('Quiz', back_populates='questions')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(20))
    user = db.relationship('User', backref='scores', lazy=True)
    quiz = db.relationship('Quiz', backref='scores', lazy=True)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.String(200), nullable=False)

ADMIN_CREDENTIALS = {'email': 'admin@quizmaster.com', 'password': 'admin123'}

@app.after_request
def add_header(response):
    """
    Add headers to force no caching.
    """
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

#--------------------login and register endpoints---------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        dob = request.form.get('dob')
        qualification = request.form.get('qualification')

        if not email or not password or not full_name or not dob or not qualification:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))


        hashed_password = generate_password_hash(password) 
        new_user = User(email=email, password=hashed_password, full_name=full_name, dob=dob, qualification=qualification)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('userlogin'))  

    return render_template('register.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['email'] = user.email
            session['fullname'] = user.full_name  
            flash("Login successful!", "success")
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials, please try again!", "danger")

    return render_template('userlogin.html')
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_CREDENTIALS['email'] and password == ADMIN_CREDENTIALS['password']:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid Admin Credentials!', 'danger')
    return render_template('adminlogin.html')

#-----------------------------admin,dashboard, user dashboard------------------------------
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))

    if request.method == 'POST':
        subject_name = request.form.get('subject_name')
        description = request.form.get('description')
        if subject_name and description:
            new_subject = Subject(name=subject_name, description=description)
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

    all_subjects = Subject.query.all()
    all_chapters = Chapter.query.all()
    subject_data = []

    for subject in all_subjects:
        chapters = Chapter.query.filter_by(subject_id=subject.id).all()
        chapter_ids = [chapter.id for chapter in chapters]
        total_questions = Question.query.join(Quiz).filter(Quiz.chapter_id.in_(chapter_ids)).count()
        subject_data.append({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'chapters': [chapter.name for chapter in chapters],
            'question_count': total_questions
        })

    chapter_question_counts = {chapter.id: Question.query.join(Quiz).filter(Quiz.chapter_id == chapter.id).count() for chapter in all_chapters}

    return render_template(
        'admin_dashboard.html', 
        all_subjects=all_subjects, 
        all_chapters=all_chapters,
        subject_data=subject_data,
        chapter_question_counts=chapter_question_counts
    )

@app.route('/user_dashboard')
def user_dashboard():
    quizzes = Quiz.query.all()


    for quiz in quizzes:
        quiz.question_count = Question.query.filter_by(quiz_id=quiz.id).count()

    return render_template('user_dashboard.html', quizzes=quizzes)

#------------------------search button for admin part---------------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')  # Get the search query from the URL parameters
    if query:
        # Search quizzes
        quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
        
        # Search subjects
        subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()
        
        # Search users (if needed)
        users = User.query.filter(User.full_name.ilike(f'%{query}%') | User.email.ilike(f'%{query}%')).all()

        return render_template(
            'search_results.html',
            query=query,
            quizzes=quizzes,
            subjects=subjects,
            users=users
        )
    else:
        return redirect(url_for('admin_dashboard')) 


#-------------------------------------quiz,subject and chapter endpoints----------------------------------------

@app.route('/quizmanagement')
def quizmanagement():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))
    
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.options(db.joinedload(Quiz.questions)).all()
    questions = Question.query.all()
    
    return render_template('quizmanagement.html', 
                           all_subjects=subjects, 
                           all_chapters=chapters, 
                           all_quizzes=quizzes,
                           questions=questions)



@app.route('/add_subject', methods=['POST'])
def add_subject():
    subject_name = request.form.get('subject_name')
    description = request.form.get('description')

    if not subject_name:
        flash('Please enter a subject name', 'danger')
        return redirect(url_for('admin_dashboard'))  

    # Check if the subject already exists before adding
    existing_subject = Subject.query.filter_by(name=subject_name).first()
    if existing_subject:
        flash(f'Subject "{subject_name}" already exists!', 'danger')
        return redirect(url_for('admin_dashboard'))  # Redirect if subject exists

    # If not exists, add the new subject
    new_subject = Subject(name=subject_name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    flash('Subject added successfully!', 'success')

    return redirect(url_for('admin_dashboard'))  


@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!', 'success')
    else:
        flash('Subject not found', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_subject/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        new_name = request.form.get('subject_name')
        new_description = request.form.get('description')
        subject.name = new_name
        subject.description = new_description
        db.session.commit()
        flash('Subject updated successfully!', 'success')
    else:
        flash('Subject not found', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_chapter/<int:chapter_id>', methods=['POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        new_name = request.form.get('chapter_name')
        new_description = request.form.get('description')
        chapter.name = new_name
        chapter.description = new_description
        db.session.commit()
        flash('Subject updated successfully!', 'success')
    else:
        flash('Subject not found', 'danger')
    return redirect(url_for('admin_dashboard'))



@app.route('/add_chapter/<int:subject_id>', methods=['POST'])
def add_chapter(subject_id):
    chapter_name = request.form.get('chapter_name')
    description = request.form.get('description')

    if not chapter_name or not description:
        flash('Please provide Chapter Name and Description.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Check if chapter already exists under the same subject
    existing_chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject_id).first()
    if existing_chapter:
        flash(f'Chapter "{chapter_name}" already exists in this subject!', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Add new chapter
    new_chapter = Chapter(name=chapter_name, description=description, subject_id=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    
    flash(f'Chapter "{chapter_name}" added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash("Chapter not found!", "danger")
        return redirect(url_for('quizmanagement'))

    try:
        
        default_chapter_id = 1  
        Quiz.query.filter_by(chapter_id=chapter_id).update({"chapter_id": default_chapter_id})

        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting chapter: {str(e)}", "danger")

    return redirect(url_for('quizmanagement'))


@app.route('/view_quiz/<int:quiz_id>')
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Extract chapter name properly if it's an object
    chapter_name = quiz.chapter.name if hasattr(quiz.chapter, 'name') else str(quiz.chapter)
    subject_name = quiz.chapter.subject.name if hasattr(quiz.chapter, 'subject') else "Unknown"
    # Calculate the number of questions
    num_questions = len(quiz.questions) if quiz.questions else 0
    print(f"Quiz Details: {quiz.id}, Chapter: {chapter_name}, Questions: {num_questions}, subject:{subject_name}")

    return render_template('view_quiz.html', quiz=quiz, chapter_name=chapter_name, num_questions=num_questions,subject_name=subject_name)


@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    quiz_name = request.form.get('quiz_name')
    quiz_duration = request.form.get('quiz_duration')
    chapter_id = request.form.get('chapter_id')

    if not all([quiz_name, quiz_duration, chapter_id]):
        flash("All fields are required!", "danger")
        return redirect(url_for('quizmanagement'))

    # Find the chapter
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash("Invalid chapter selected!", "danger")
        return redirect(url_for('quizmanagement'))

    new_quiz = Quiz(
        name=quiz_name,  
        duration=quiz_duration, 
        chapter_id=chapter_id
    )

    try:
        db.session.add(new_quiz)
        db.session.commit()
        flash("Quiz added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding quiz: {str(e)}", "danger")

    return redirect(url_for('quizmanagement'))

@app.route('/start_quiz/<int:quiz_id>/<int:q_no>', methods=['GET', 'POST'])
def start_quiz(quiz_id, q_no):
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    
    # If no more questions, go to summary
    if q_no > total_questions:
        calculate_score(quiz_id)
        return redirect(url_for('scores'))

    question = Question.query.filter_by(quiz_id=quiz_id).offset(q_no - 1).first()
    options_list = [question.option1, question.option2, question.option3, question.option4] if question else []

    if request.method == 'POST':
        selected_option = request.form.get('answer')
        action = request.form.get('action')
        
        if not selected_option:
            flash("Please select an option before proceeding.", "danger")
            return redirect(url_for('start_quiz', quiz_id=quiz_id, q_no=q_no))

        # Save user's answer
        answer_entry = UserAnswer(quiz_id=quiz_id, question_id=question.id, selected_option=selected_option)
        db.session.add(answer_entry)
        db.session.commit()

        if q_no == total_questions:
            # Last question - calculate score and save it
            calculate_score(quiz_id)
            flash("Quiz completed successfully! Check your score below.", "success")
            return redirect(url_for('scores'))
        else:
            # More questions to go
            return redirect(url_for('start_quiz', quiz_id=quiz_id, q_no=q_no + 1))

    return render_template('start_quiz.html', 
                           quiz_id=quiz_id, 
                           question_no=q_no, 
                           question=question, 
                           options_list=options_list, 
                           total_questions=total_questions, 
                           duration=10)


def calculate_score(quiz_id):
    if 'user_id' not in session:
        return
        
    user_id = session['user_id']
    
    # Get all questions for this quiz
    all_questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Get answers for this quiz - we'll filter by the quiz_id since answers are saved in the current session
    user_answers = UserAnswer.query.filter(UserAnswer.quiz_id == quiz_id).all()
    
    # Calculate score
    correct_answers = 0
    for question in all_questions:
        for answer in user_answers:
            if answer.question_id == question.id:
                # Check if the answer matches correct option
                question_option_field = f"option{question.correct_option}"
                correct_option_text = getattr(question, question_option_field)
                if answer.selected_option == correct_option_text:
                    correct_answers += 1
                break
    
    # Add timestamp
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Always create a new score record for each quiz attempt
    score = Score(user_id=user_id, quiz_id=quiz_id, score=correct_answers, timestamp=current_time)
    db.session.add(score)
    db.session.commit()
    
    return correct_answers

@app.route('/edit_quiz/<int:quiz_id>', methods=['POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found!", "danger")
        return redirect(url_for('quizmanagement'))

    quiz_name = request.form.get('quiz_name')
    chapter_id = request.form.get('chapter_id')
    quiz_duration = request.form.get('quiz_duration')

    if not quiz_name:
        flash("Quiz name is required!", "danger")
        return redirect(url_for('quizmanagement'))

    quiz.name = quiz_name
    if chapter_id:
        quiz.chapter_id = chapter_id
    if quiz_duration:
        quiz.duration = quiz_duration

    try:
        db.session.commit()
        flash("Quiz updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating quiz: {str(e)}", "danger")

    return redirect(url_for('quizmanagement'))


@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    Question.query.filter_by(quiz_id=quiz_id).delete()
    if not quiz:
        flash("Quiz not found!", "danger")
        return redirect(url_for('quizmanagement'))

    try:
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting quiz: {str(e)}", "danger")

    return redirect(url_for('quizmanagement'))


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_id = session['user_id']
    quiz_id = request.form['quiz_id']  
    quiz = Quiz.query.get(quiz_id)
    correct_answers = 0

    # Assuming questions are submitted with their IDs and selected options
    for question_id, selected_option in request.form.items():
        if question_id.startswith('question_'):
            question_id = int(question_id.replace('question_', ''))
            question = Question.query.get(question_id)
            if question.correct_option == int(selected_option):
                correct_answers += 1

    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if a score already exists for this user and quiz
    existing_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    if existing_score:
        # Update existing score if it's higher
        if correct_answers > existing_score.score:
            existing_score.score = correct_answers
            existing_score.timestamp = current_time
            db.session.commit()
    else:
        # Create new score record
        score = Score(user_id=user_id, quiz_id=quiz_id, score=correct_answers, timestamp=current_time)
        db.session.add(score)
        db.session.commit()

    flash(f"Quiz submitted successfully! Your score: {correct_answers}", "success")
    return redirect(url_for('scores'))

#---------------------------------------------question endpoints(add/delete/edit)-----------------------------------
@app.route('/add_question', methods=['POST'])
def add_question():
    question_text = request.form['questionTitle']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    correct_option = int(request.form['correctOption'])
    quiz_id = int(request.form['quiz_id'])
    chapter_id = request.form.get('chapter_id')  # Get chapterid from the form
    
    # Ensure chapter_id is not None
    if not chapter_id:
        chapter_id = 1  # default value
    else:
        chapter_id = int(chapter_id)

    new_question = Question(
        question_text=question_text,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option,
        quiz_id=quiz_id,
        chapter_id=chapter_id  # Include chapterid
    )

    db.session.add(new_question)
    db.session.commit()
    
    flash('Question added successfully!', 'success')
    return redirect(url_for('quizmanagement'))



@app.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted successfully!", "success")
    else:
        flash("Question not found!", "danger")
    return redirect(url_for('quizmanagement'))

@app.route('/edit_question/<int:question_id>', methods=['POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    new_text = request.form.get("questionTitle")

    if new_text:
        question.question_text = new_text
        db.session.commit()
        flash("Question updated successfully!", "success")

    return redirect(request.referrer)  

#-----------------------------------------------scores endpoints-----------------------------------------------------
@app.route('/scores')
def scores():
    if 'user_id' not in session:
        return redirect(url_for('userlogin')) 

    user_id = session['user_id']
    user_scores = db.session.query(Score, Quiz)\
        .join(Quiz)\
        .filter(Score.user_id == user_id)\
        .order_by(Score.timestamp.desc())\
        .all()
    
    # data for template
    score_data = []
    for score, quiz in user_scores:
        question_count = Question.query.filter_by(quiz_id=quiz.id).count()
        percentage = (score.score / question_count * 100) if question_count > 0 else 0
        score_data.append({
            'score': score,
            'quiz': quiz,
            'question_count': question_count,
            'percentage': round(percentage, 2)
        })

    return render_template('scores.html', scores=score_data)

@app.route('/reset_scores', methods=['POST'])
def reset_scores():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    
    user_id = session['user_id']
    
    try:
        # Delete all UserAnswer entries for this user
        UserAnswer.query.filter(UserAnswer.quiz_id.in_(
            db.session.query(Score.quiz_id).filter_by(user_id=user_id)
        )).delete(synchronize_session=False)
        
        # Delete all score
        Score.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        flash("All your quiz scores have been reset successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error resetting scores: {str(e)}", "danger")
    
    return redirect(url_for('scores'))

#---------------------------------------------------------summary endpoints------------------------------------------
@app.route('/admin_summary')
def admin_summary():
    try:
        # Ensure 'static' directory exists
        if not os.path.exists("static"):
            os.makedirs("static")
        
        print("✅ Static directory checked or created.")  

        # **Pie Chart Data**
        subjects = Subject.query.all()
        subject_names = []
        attempt_counts = []

        for subject in subjects:
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()
            attempts = sum(db.session.query(Score).filter(Score.quiz_id == quiz.id).count() for quiz in quizzes)

            print(f"📊 Subject: {subject.name}, Attempts: {attempts}")  

            if attempts > 0:
                subject_names.append(subject.name)
                attempt_counts.append(attempts)

        if subject_names:  # Generate Pie Chart only if data exists
            plt.figure(figsize=(8, 6))
            plt.pie(attempt_counts, labels=subject_names, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen', 'orange', 'salmon'])
            plt.title("Quiz Attempts by Subject")
            plt.savefig('static/pie_chart_attempts.png')
            plt.close()
            print("✅ Pie chart saved!")  
        else:
            print("⚠️ No data for pie chart!")  

        # Bar Chart Data
        subject_scores = {}

        for subject in subjects:
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()
            max_score = max((db.session.query(Score.score).filter(Score.quiz_id == quiz.id).scalar() or 0) for quiz in quizzes)

            print(f"📈 Subject: {subject.name}, Max Score: {max_score}")  # Debugging print

            if max_score > 0:
                subject_scores[subject.name] = max_score

        if subject_scores:
            plt.figure(figsize=(8, 6))
            plt.bar(subject_scores.keys(), subject_scores.values(), color=['skyblue', 'lightgreen', 'orange', 'salmon'])
            plt.xlabel("Subjects")
            plt.ylabel("Top Scores")
            plt.title("Top Scores by Subject")
            plt.xticks(rotation=45)
            plt.savefig('static/bar_chart_scores.png')
            plt.close()
            print("✅ Bar chart saved!")  
        else:
            print("⚠️ No data for bar chart!")  

        return render_template('admin_summary.html')

    except Exception as e:
        print(f"❌ Error: {e}")  
        return render_template('admin_summary.html', error=str(e))




@app.route("/user_summary")
def user_summary():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))

    user_id = session["user_id"]
    
    # Fetch scores grouped by chapter
    scores = (
        db.session.query(Chapter.name, db.func.sum(Score.score))
        .join(Quiz, Chapter.id == Quiz.chapter_id)
        .join(Score, Quiz.id == Score.quiz_id)
        .filter(Score.user_id == user_id)
        .group_by(Chapter.name)
        .all()
    )

    if not scores:
        return render_template("user_summary.html", error="No quiz data available!")

    
    chapters, scores_list = zip(*scores)

    # Generate bar chart
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    plt.figure(figsize=(8, 5))
    plt.bar(chapters, scores_list, color='blue')
    plt.xlabel("Chapters")
    plt.ylabel("Total Marks")
    plt.title("Chapter-wise Quiz Scores")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    chart_path = os.path.join(static_folder, "user_summary_chart.png")
    plt.savefig(chart_path)
    plt.close()

    return render_template("user_summary.html", chart_url=url_for("static", filename="user_summary_chart.png"))


#----------------------------------------------------logout endpoint---------------------------------------------------------


@app.route('/logout')
def logout():
    session.clear()
    flash('logged out successfully')
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()
    
    # Pre-existing user credentials
    if not User.query.filter_by(email='user@quizmaster.com').first():
        pre_existing_user = User(
            email='user@quizmaster.com',
            password=generate_password_hash('user123'),
            full_name='Aman',
            qualification='BS Data Science',
            dob='31-12-2005')
        db.session.add(pre_existing_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)








