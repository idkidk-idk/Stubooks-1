from flask import Flask, session, request, url_for, render_template, redirect
import sqlite3
app = Flask(__name__, static_url_path="", static_folder='static')
db= sqlite3.connect('stubooks1', check_same_thread=False)
cursor= db.cursor()


def _insert(fname, email, comments, ratings):
    print(fname, email, comments, ratings, sep=',')
    params = {'fname':fname, 'email':email, 'comments':comments, 'ratings':ratings}
    cursor = db.cursor()
    cursor.execute("insert into guestbook values (:fname, :email, :comments, :ratings)", params)
    cursor.close()
    db.commit()


def _userinsert(firstname, lastname, username, email, password, selectcourse, gender):
    print(firstname, lastname, username, email, password, selectcourse, gender, sep=',')
    params = {'firstname':firstname, 'lastname':lastname, 'username':username, 'email':email, 'password':password, 'selectcourse':selectcourse, 'gender':gender}
    cursor= db.cursor()
    cursor.execute("insert into user values (:firstname, :lastname, :username, :email, :password, :selectcourse, :gender)", params)
    cursor.close()
    db.commit()


def _usercomments(username, book_id, comments, rating ):
    print(username, book_id, comments, rating, sep=' , ')
    params = {'username':username, 'book_id':book_id, 'comments':comments, 'rating':rating}
    cursor = db.cursor()
    cursor.execute("insert into content values (:username, :book_id, :comments, :rating)", params)
    cursor.close()
    db.commit()


def _userlike(book_id, like):
    print(book_id, like, sep=' , ')
    params = {'book_id':book_id,'like':like}
    cursor = db.cursor()
    cursor.execute("insert into likes values (:book_id, like)", params)
    cursor.close()
    db.commit()
    print("done")


@app.route('/')
def index():
    query = "select book_id, book_name from book where book_id='B12';"
    cur = db.execute(query)
    entries = cur.fetchall()
    cur.close()
    print(entries)

    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('index.html', entries=entries, rv=rv, username=session['username'])
    else:
        return render_template('index.html', entries=entries, rv=rv )


@app.route('/about')
def about():
    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('about.html',  rv=rv, username=session['username'])
    else:
        return render_template('about.html', rv=rv )



@app.route('/contact')
def contact():
    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('contact.html',  rv=rv, username=session['username'])
    else:
        return render_template('contact.html', rv=rv )



@app.route('/faqs')
def faqs():
    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('faqs.html',  rv=rv, username=session['username'])
    else:
        return render_template('faqs.html', rv=rv )



@app.route('/register', methods={'POST','GET'})
def signup():

    if request.method == "POST":
        _userinsert(request.form['firstname'], request.form['lastname'], request.form['username'], request.form['email'], request.form['password'], request.form['selectcourse'], request.form['gender'])
    print("hi")
    return render_template('login.html')


@app.route('/login', methods={'POST','GET'})
def login():

    if request.method == 'POST':
        query = "select * from user where username='" + request.form['username']
        query = query + "' and password='" + request.form['password']+"';"
        print(query)
        cur = db.execute(query)
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 1:
            session['username'] = request.form['username']
            session['password'] = rv[0][0]
            session['logged_in'] = True
            print("done")
            return redirect('/')
        else:
            render_template('login.html', msg="Incorrect username or password")
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('username')
    session.pop('password')
    return redirect('/')


@app.route('/coursesEIC', methods={'POST','GET'})
def courses():
    query = "select link, module_name from module where course_id='C001';"
    cur = db.execute(query)
    entries = cur.fetchall()
    cur.close()
    print(entries)
    print("hello")
    query1 = "select link, module_name from module where course_id='C002';"
    cur = db.execute(query1)
    entries1 = cur.fetchall()
    cur.close()
    print(entries1)
    print("hello")
    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('coursesEIC.html',  rv=rv, username=session['username'],entries=entries, entries1 = entries1)
    else:
        return render_template('coursesEIC.html', rv=rv,entries=entries, entries1 = entries1 )



@app.route('/guest', methods={'POST','GET'})
def guest():
    if request.method == "POST":
        _insert(request.form['fname'], request.form['email'], request.form['comments'], request.form['ratings'])

    query = "select * from guestbook"
    cur = db.execute(query)
    entries = cur.fetchall()
    cur.close()
    print(entries)
    username = session.get("username")
    query1 = "select firstname from user where username ='" + str(username) + "'"
    print(query1)
    cur = db.execute(query1)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query1)
    if session.get("username"):
        return render_template('guest.html',  rv=rv, username=session['username'],entries=entries)
    else:
        return render_template('guest.html', rv=rv,entries=entries)


@app.route('/data_ind')
def data_ind():
    print("hello")
    query = "select* from book where module_id=1;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)

    query1 = "select link, module_name from module where course_id='C001';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)

    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/remote_hs')
def remote_hs():
    print("hello")
    query = "select* from book where module_id=2;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C001';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/analysis_desn')
def analysis_desn():
    print("hello")
    query = "select* from book where module_id=3;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C001';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/analysis_desn2')
def analysis_desn2():
    print("hello")
    query = "select* from book where module_id=6;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C002';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )

@app.route('/web_dev')
def web_dev():
    print("hello")
    query = "select* from book where module_id=4;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C001';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/is_research')
def is_research():
    print("hello")
    query = "select* from book where module_id=5;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C002';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/decision_ss')
def decision_ss():
    print("hello")
    query = "select* from book where module_id=7;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C002';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/db_design')
def db_design():
    print("hello")
    query = "select* from book where module_id= 7;"
    cur = db.execute(query)
    rv2 = cur.fetchall()
    cur.close()
    print(rv2)
    query1 = "select link, module_name from module where course_id='C002';"
    cur = db.execute(query1)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)
    if session.get("username"):
        return render_template('booksall.html',  rv=rv, username=session['username'], entries1=rv1, entries=rv2)
    else:
        return render_template('booksall.html', rv=rv, entries1=rv1, entries=rv2 )


@app.route('/stubooks/book.html', methods={'POST','GET'})
def book():

    book_id = request.args.get("id")
    print(book_id)
    query = "select book_id, book_name, book_type, publish_date, author_name, pub_name, link from book, author, publisher where book.author_id= author.author_id and book.pub_id= publisher.pub_id and book_id='" +  str(book_id) + "'"
    print(query)
    cur = db.execute(query)
    rv1 = cur.fetchall()
    cur.close()
    print(rv1)
    if request.method == 'POST' and session.get('logged_in'):
        _usercomments(session['username'],book_id, request.form['comments'], request.form['rating'] )

    query1 = "select username, comments, rating from content where book_id ='" + str(book_id) + "'"
    print(query1)
    cur = db.execute(query1)
    rvcomments = cur.fetchall()
    print(rvcomments)
    cur.close()

    username = session.get("username")
    query2 = "select firstname from user where username ='" + str(username) + "'"
    print(query2)
    cur = db.execute(query2)
    rv = cur.fetchall()
    print(rv)
    cur.close()
    print(query2)

    if session.get("username"):
        return render_template('book.html', entries=rv1, passcomments=rvcomments, username=session['username'], rv=rv)
    else:
        return render_template('book.html', entries=rv1, passcomments=rvcomments, rv=rv )


app.secret_key="what"

if __name__ == '__main__':
    app.run(debug=True)
